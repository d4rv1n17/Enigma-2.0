"""Print GitHub release notes for a version, taken from the README changelog."""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def changelog(version):
    with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as f:
        lines = f.read().splitlines()
    out, inside = [], False
    for line in lines:
        if line.startswith("### "):
            if inside:
                break
            inside = line[4:].split(":")[0].strip() == version
            continue
        if inside:
            out.append(line)
    return "\n".join(out).strip()


def main():
    version = sys.argv[1]
    notes = changelog(version) or "See README.md for details."
    print("""## Download

**[EnigmaCube-Setup-%(v)s.exe](https://github.com/%(repo)s/releases/download/v%(v)s/EnigmaCube-Setup-%(v)s.exe)** \
(Windows 10/11, 64-bit)

1. Download the installer above and run it.
2. If Windows SmartScreen appears, click **More info → Run anyway** (the app is not code-signed).
3. Choose the folder and shortcuts, then click **Install** (or **Update** if an older version is installed).

Скачайте установщик выше, запустите его и нажмите «Установить». Если появится окно SmartScreen, \
нажмите «Подробнее → Выполнить в любом случае».

## What's new in %(v)s

%(notes)s
""" % {"v": version, "notes": notes,
       "repo": os.environ.get("GITHUB_REPOSITORY", "d4rv1n17/Enigma-2.0")})


if __name__ == "__main__":
    main()
