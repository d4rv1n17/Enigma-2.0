# -*- coding: utf-8 -*-
"""Install / update / uninstall logic for the Enigma Cube setup (no GUI).

Windows-only parts (registry, shortcuts, closing the running app) are no-ops
elsewhere, so the file logic can be tested on any OS.
"""

import io
import json
import os
import shutil
import subprocess
import sys
import zipfile

APP_NAME = "Enigma Cube"
APP_EXE = "EnigmaCube.exe"
PUBLISHER = "Enigma Studio"
UNINSTALL_EXE = "uninstall.exe"
MANIFEST = "install_manifest.txt"
REG_KEY = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\EnigmaCube"
# Inno Setup installer used by version 2.2 (removed silently when updating)
OLD_INNO_KEY = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\{80FBE274-847C-44D6-992B-830503FB751A}_is1"
DATA_DIR_NAME = "EnigmaTimer"

IS_WIN = sys.platform.startswith("win")
NO_WINDOW = 0x08000000 if IS_WIN else 0


def resource(name):
    """Path of a file bundled with the setup (PyInstaller) or next to this script."""
    base = getattr(sys, "_MEIPASS", None)
    if base and os.path.exists(os.path.join(base, name)):
        return os.path.join(base, name)
    here = os.path.dirname(os.path.abspath(__file__))
    for cand in (os.path.join(here, name), os.path.join(here, "build", name),
                 os.path.join(here, "..", "assets", name)):
        if os.path.exists(cand):
            return cand
    return os.path.join(here, name)


def payload_info(path=None):
    """(version, total_uncompressed_bytes) of the bundled program."""
    path = path or resource("payload.zip")
    version = "?"
    total = 0
    with zipfile.ZipFile(path) as z:
        for info in z.infolist():
            total += info.file_size
        if "payload.json" in z.namelist():
            version = json.loads(z.read("payload.json").decode("utf-8")).get("version", "?")
    return version, total


def default_install_dir():
    base = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
    return os.path.join(base, "Programs", APP_NAME)


def data_dir():
    base = os.environ.get("APPDATA") or os.path.expanduser("~")
    return os.path.join(base, DATA_DIR_NAME)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

def _winreg():
    if not IS_WIN:
        return None
    import winreg  # noqa: WPS433 - Windows only
    return winreg


def existing_install():
    """{'dir':..., 'version':..., 'inno_uninstall':...} or None."""
    wr = _winreg()
    if wr is None:
        return None
    found = {}
    try:
        with wr.OpenKey(wr.HKEY_CURRENT_USER, REG_KEY) as k:
            found["dir"] = wr.QueryValueEx(k, "InstallLocation")[0]
            found["version"] = wr.QueryValueEx(k, "DisplayVersion")[0]
    except OSError:
        pass
    for hive in (wr.HKEY_CURRENT_USER, wr.HKEY_LOCAL_MACHINE):
        for view in (0, getattr(wr, "KEY_WOW64_32KEY", 0), getattr(wr, "KEY_WOW64_64KEY", 0)):
            try:
                with wr.OpenKey(hive, OLD_INNO_KEY, 0, wr.KEY_READ | view) as k:
                    found.setdefault("dir", wr.QueryValueEx(k, "InstallLocation")[0].rstrip("\\"))
                    found.setdefault("version", wr.QueryValueEx(k, "DisplayVersion")[0])
                    try:
                        found["inno_uninstall"] = wr.QueryValueEx(k, "UninstallString")[0]
                    except OSError:
                        pass
            except OSError:
                continue
    return found or None


def write_registry(install_dir, version, size_bytes):
    wr = _winreg()
    if wr is None:
        return
    with wr.CreateKey(wr.HKEY_CURRENT_USER, REG_KEY) as k:
        uninst = os.path.join(install_dir, UNINSTALL_EXE)
        values = {
            "DisplayName": APP_NAME,
            "DisplayVersion": version,
            "Publisher": PUBLISHER,
            "DisplayIcon": os.path.join(install_dir, APP_EXE),
            "InstallLocation": install_dir,
            "UninstallString": '"%s" --uninstall' % uninst,
            "QuietUninstallString": '"%s" --uninstall --quiet' % uninst,
        }
        for name, val in values.items():
            wr.SetValueEx(k, name, 0, wr.REG_SZ, val)
        wr.SetValueEx(k, "EstimatedSize", 0, wr.REG_DWORD, int(size_bytes // 1024))
        wr.SetValueEx(k, "NoModify", 0, wr.REG_DWORD, 1)
        wr.SetValueEx(k, "NoRepair", 0, wr.REG_DWORD, 1)


def remove_registry():
    wr = _winreg()
    if wr is None:
        return
    try:
        wr.DeleteKey(wr.HKEY_CURRENT_USER, REG_KEY)
    except OSError:
        pass


# ---------------------------------------------------------------------------
# Shortcuts and processes
# ---------------------------------------------------------------------------

def _powershell(script):
    if not IS_WIN:
        return
    subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script],
                   creationflags=NO_WINDOW, check=False)


def _ps_quote(s):
    return "'" + s.replace("'", "''") + "'"


def create_shortcuts(install_dir, desktop):
    target = os.path.join(install_dir, APP_EXE)
    lines = [
        "$sh = New-Object -ComObject WScript.Shell",
        "$targets = @([Environment]::GetFolderPath('Programs'))",
    ]
    if desktop:
        lines.append("$targets += [Environment]::GetFolderPath('Desktop')")
    lines += [
        "foreach ($d in $targets) {",
        "  $s = $sh.CreateShortcut((Join-Path $d %s))" % _ps_quote(APP_NAME + ".lnk"),
        "  $s.TargetPath = %s" % _ps_quote(target),
        "  $s.WorkingDirectory = %s" % _ps_quote(install_dir),
        "  $s.IconLocation = %s" % _ps_quote(target + ",0"),
        "  $s.Save()",
        "}",
    ]
    _powershell("; ".join(lines))


def remove_shortcuts():
    script = ("foreach ($d in @([Environment]::GetFolderPath('Programs'), "
              "[Environment]::GetFolderPath('Desktop'))) { "
              "$p = Join-Path $d %s; if (Test-Path $p) { Remove-Item $p -Force } }"
              % _ps_quote(APP_NAME + ".lnk"))
    _powershell(script)


def close_running_app():
    if not IS_WIN:
        return
    subprocess.run(["taskkill", "/IM", APP_EXE, "/F"], creationflags=NO_WINDOW,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)


def run_old_uninstaller(cmd):
    """Silently remove the old Inno Setup installation (keeps user data)."""
    if not IS_WIN or not cmd:
        return
    exe = cmd.strip().strip('"')
    if not os.path.exists(exe):
        return
    subprocess.run([exe, "/VERYSILENT", "/SUPPRESSMSGBOXES", "/NORESTART"],
                   creationflags=NO_WINDOW, check=False)


def launch_app(install_dir):
    exe = os.path.join(install_dir, APP_EXE)
    if os.path.exists(exe):
        subprocess.Popen([exe], cwd=install_dir, close_fds=True)


# ---------------------------------------------------------------------------
# Files
# ---------------------------------------------------------------------------

def normalise_dir(path):
    """Never install straight into a shared folder: add "Enigma Cube" to it."""
    path = os.path.abspath(os.path.expanduser(path.strip().strip('"')))
    if os.path.basename(path.rstrip("\\/")).lower() != APP_NAME.lower():
        if os.path.isdir(path) and os.listdir(path) and not os.path.exists(
                os.path.join(path, APP_EXE)):
            path = os.path.join(path, APP_NAME)
    return path


def read_manifest(install_dir):
    p = os.path.join(install_dir, MANIFEST)
    if not os.path.exists(p):
        return []
    with io.open(p, "r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f if line.strip()]


def remove_installed_files(install_dir, progress=None):
    """Delete only files this setup installed (listed in the manifest)."""
    files = read_manifest(install_dir)
    total = max(1, len(files))
    for i, rel in enumerate(files):
        p = os.path.join(install_dir, rel)
        try:
            if os.path.isfile(p):
                os.remove(p)
        except OSError:
            pass
        if progress:
            progress(i + 1, total, rel)
    # remove now-empty folders, deepest first
    dirs = sorted(set(os.path.dirname(os.path.join(install_dir, r)) for r in files),
                  key=len, reverse=True)
    for d in dirs:
        while d.startswith(install_dir) and d != install_dir:
            try:
                os.rmdir(d)
            except OSError:
                break
            d = os.path.dirname(d)
    try:
        os.remove(os.path.join(install_dir, MANIFEST))
    except OSError:
        pass


def install_files(payload_path, install_dir, self_exe=None, progress=None):
    """Extract the program, copy the uninstaller, write the manifest."""
    if os.path.isdir(install_dir):
        remove_installed_files(install_dir)
    else:
        os.makedirs(install_dir)
    written = []
    with zipfile.ZipFile(payload_path) as z:
        members = [m for m in z.infolist() if not m.is_dir() and m.filename != "payload.json"]
        total = max(1, len(members))
        for i, m in enumerate(members):
            rel = m.filename.replace("/", os.sep)
            dest = os.path.join(install_dir, rel)
            if not os.path.abspath(dest).startswith(os.path.abspath(install_dir)):
                continue  # never write outside the install folder
            d = os.path.dirname(dest)
            if not os.path.isdir(d):
                os.makedirs(d)
            with z.open(m) as src, open(dest, "wb") as out:
                shutil.copyfileobj(src, out)
            written.append(rel)
            if progress:
                progress(i + 1, total, rel)
    if self_exe and os.path.exists(self_exe):
        shutil.copy2(self_exe, os.path.join(install_dir, UNINSTALL_EXE))
        written.append(UNINSTALL_EXE)
    with io.open(os.path.join(install_dir, MANIFEST), "w", encoding="utf-8") as f:
        f.write("\n".join(written) + "\n")
    return written


def install(payload_path, install_dir, desktop_shortcut=True, self_exe=None, progress=None,
            existing=None):
    version, size = payload_info(payload_path)
    if existing and existing.get("inno_uninstall"):
        run_old_uninstaller(existing["inno_uninstall"])
    close_running_app()
    install_files(payload_path, install_dir, self_exe, progress)
    create_shortcuts(install_dir, desktop_shortcut)
    write_registry(install_dir, version, size)
    return version


def uninstall(install_dir, delete_data=False, progress=None):
    close_running_app()
    remove_installed_files(install_dir, progress)
    try:
        os.rmdir(install_dir)
    except OSError:
        pass
    remove_shortcuts()
    remove_registry()
    if delete_data and os.path.isdir(data_dir()):
        shutil.rmtree(data_dir(), ignore_errors=True)
