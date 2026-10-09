"""Install / update / uninstall file logic of the custom setup."""

import json
import os
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "installer"))

import setup_core as core  # noqa: E402


def make_payload(folder, files, version="9.9"):
    path = os.path.join(folder, "payload.zip")
    with zipfile.ZipFile(path, "w") as z:
        for name, data in files.items():
            z.writestr(name, data)
        z.writestr("payload.json", json.dumps({"version": version}))
    return path


class SetupCoreTest(unittest.TestCase):
    def test_install_update_uninstall(self):
        tmp = tempfile.mkdtemp()
        target = os.path.join(tmp, "Programs", "Enigma Cube")
        p1 = make_payload(tmp, {"EnigmaCube.exe": b"v1", "_internal/a.dll": b"a",
                                "_internal/old.dll": b"o"})
        self.assertEqual(core.payload_info(p1)[0], "9.9")
        core.install(p1, target, desktop_shortcut=False)
        self.assertTrue(os.path.exists(os.path.join(target, "_internal", "old.dll")))
        # the user keeps a file of their own in the folder
        with open(os.path.join(target, "notes.txt"), "w") as f:
            f.write("mine")
        os.remove(p1)
        p2 = make_payload(tmp, {"EnigmaCube.exe": b"v2", "_internal/a.dll": b"a2"}, "10.0")
        core.install(p2, target, desktop_shortcut=False)
        with open(os.path.join(target, "EnigmaCube.exe"), "rb") as f:
            self.assertEqual(f.read(), b"v2")
        self.assertFalse(os.path.exists(os.path.join(target, "_internal", "old.dll")))
        self.assertTrue(os.path.exists(os.path.join(target, "notes.txt")))
        core.uninstall(target)
        self.assertFalse(os.path.exists(os.path.join(target, "EnigmaCube.exe")))
        self.assertFalse(os.path.exists(os.path.join(target, "_internal")))
        self.assertTrue(os.path.exists(os.path.join(target, "notes.txt")))  # not ours

    def test_zip_slip_is_ignored(self):
        tmp = tempfile.mkdtemp()
        p = make_payload(tmp, {"../evil.txt": b"x", "EnigmaCube.exe": b"v"})
        target = os.path.join(tmp, "app")
        core.install_files(p, target)
        self.assertFalse(os.path.exists(os.path.join(tmp, "evil.txt")))

    def test_never_installs_into_a_shared_folder(self):
        tmp = tempfile.mkdtemp()
        with open(os.path.join(tmp, "other.txt"), "w") as f:
            f.write("x")
        self.assertEqual(core.normalise_dir(tmp), os.path.join(tmp, "Enigma Cube"))
        empty = os.path.join(tmp, "empty")
        os.makedirs(empty)
        self.assertEqual(core.normalise_dir(empty), empty)


if __name__ == "__main__":
    unittest.main()
