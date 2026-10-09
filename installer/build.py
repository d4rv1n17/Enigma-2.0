# -*- coding: utf-8 -*-
"""Builds Output/EnigmaCube-Setup-<version>.exe (run on Windows).

Steps:
  1. the app             -> dist/EnigmaCube/            (PyInstaller, one folder)
  2. the uninstaller     -> dist/EnigmaCube/uninstall.exe (setup_app.py without payload)
  3. payload.zip         <- dist/EnigmaCube + payload.json
  4. the setup           -> Output/EnigmaCube-Setup-<version>.exe (setup_app.py + payload)
"""

import json
import os
import re
import shutil
import subprocess
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INST = os.path.join(ROOT, "installer")
BUILD = os.path.join(ROOT, "build")
SEP = os.pathsep  # PyInstaller --add-data separator


def version():
    with open(os.path.join(ROOT, "enigma_timer", "__init__.py")) as f:
        return re.search(r'VERSION\s*=\s*"([^"]+)"', f.read()).group(1)


def version_file(ver):
    nums = [int(x) for x in re.findall(r"\d+", ver)][:4]
    nums += [0] * (4 - len(nums))
    t = tuple(nums)
    dotted = ".".join(str(n) for n in nums)
    text = """VSVersionInfo(
  ffi=FixedFileInfo(filevers=%(t)s, prodvers=%(t)s, mask=0x3f, flags=0x0,
                    OS=0x40004, fileType=0x1, subtype=0x0, date=(0, 0)),
  kids=[
    StringFileInfo([StringTable('040904B0', [
      StringStruct('CompanyName', 'Enigma Studio'),
      StringStruct('FileDescription', 'Enigma Cube Timer'),
      StringStruct('FileVersion', '%(d)s'),
      StringStruct('InternalName', 'EnigmaCube'),
      StringStruct('OriginalFilename', 'EnigmaCube.exe'),
      StringStruct('ProductName', 'Enigma Cube'),
      StringStruct('ProductVersion', '%(d)s')])]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
""" % {"t": repr(t), "d": dotted}
    path = os.path.join(BUILD, "version_info.txt")
    with open(path, "w") as f:
        f.write(text)
    return path


def pyinstaller(*args):
    cmd = [sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean",
           "--workpath", os.path.join(BUILD, "work"), "--specpath", BUILD] + list(args)
    print(">", " ".join(cmd), flush=True)
    subprocess.check_call(cmd, cwd=ROOT)


def main():
    ver = version()
    os.makedirs(BUILD, exist_ok=True)
    vfile = version_file(ver)
    icon = os.path.join(ROOT, "assets", "app.ico")
    assets = os.path.join(ROOT, "assets")
    small_icon = os.path.join(ROOT, "assets", "icon.png")

    print("\n[1/4] Enigma Cube %s" % ver, flush=True)
    app_dist = os.path.join(ROOT, "dist")
    pyinstaller("--onedir", "--windowed", "--name", "EnigmaCube", "--icon", icon,
                "--add-data", assets + SEP + "assets", "--version-file", vfile,
                "--distpath", app_dist, os.path.join(ROOT, "main.py"))
    app_dir = os.path.join(app_dist, "EnigmaCube")

    print("\n[2/4] Uninstaller", flush=True)
    uninst_dist = os.path.join(BUILD, "uninst")
    pyinstaller("--onefile", "--windowed", "--name", "uninstall", "--icon", icon,
                "--add-data", small_icon + SEP + ".", "--distpath", uninst_dist,
                os.path.join(INST, "setup_app.py"))
    shutil.copy2(os.path.join(uninst_dist, "uninstall.exe"), os.path.join(app_dir, "uninstall.exe"))

    print("\n[3/4] Payload", flush=True)
    payload = os.path.join(BUILD, "payload.zip")
    with zipfile.ZipFile(payload, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for base, _dirs, files in os.walk(app_dir):
            for name in files:
                full = os.path.join(base, name)
                z.write(full, os.path.relpath(full, app_dir).replace(os.sep, "/"))
        z.writestr("payload.json", json.dumps({"version": ver}))

    print("\n[4/4] Setup", flush=True)
    out = os.path.join(ROOT, "Output")
    pyinstaller("--onefile", "--windowed", "--name", "EnigmaCube-Setup-%s" % ver, "--icon", icon,
                "--add-data", payload + SEP + ".", "--add-data", small_icon + SEP + ".",
                "--version-file", vfile, "--distpath", out, os.path.join(INST, "setup_app.py"))
    result = os.path.join(out, "EnigmaCube-Setup-%s.exe" % ver)
    print("\nDone: %s (%.1f MB)" % (result, os.path.getsize(result) / 1048576.0))


if __name__ == "__main__":
    main()
