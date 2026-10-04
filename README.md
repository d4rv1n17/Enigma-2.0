# Enigma Cube Timer 2.2

A speedcubing timer for Windows, built with Python and PyQt5. It works fully offline.

Enigma Cube generates WCA-style scrambles and shows a preview of each one. It times solves like a Stackmat and tracks your averages and personal bests.

## Features

- **14 WCA events:** 2x2–7x7, Pyraminx, Skewb, Megaminx, Clock, Square-1, OH, 3BLD and FMC.
- **Scramble preview:** cube nets for 2x2–7x7 and drawings for Pyraminx, Skewb and Square-1. The previews are rendered offline.
- **Stackmat-style timer:**
  - Hold Space until the time turns green, then release to start.
  - Optional 15-second WCA inspection with beeps at 8 and 12 s.
  - Automatic +2 and DNF penalties.
- **WCA statistics:**
  - Current and best single, mo3, ao5, ao12, ao50 and ao100.
  - Session mean and standard deviation.
  - A breakdown of any average, with trimmed times in brackets.
- **Charts:** progress (singles, ao5, ao12) and the distribution of your times.
- **PB notifications** for new best singles and averages.
- **Sessions:** unlimited sessions per event, csTimer import and CSV export.
- **Minimal dark UI:**
  - Focus mode hides everything but the time while you solve.
  - Minimal mode (**M**) shows only the scramble and the timer.
  - English and Russian interface.

## Requirements

- Windows 10 or 11 (64-bit)
- About 100 MB of disk space
- A screen of 1280×720 or larger
- No internet connection needed

## Install

1. Download `EnigmaCube-Setup-2.2.exe` and run it.
2. If Windows shows **"Windows protected your PC"**, click **More info → Run anyway**. Windows shows this for new apps that don't have a paid code-signing certificate.
3. Follow the wizard and leave **"Launch Enigma Cube"** checked at the end.

The installer has these properties:
- It doesn't need administrator rights.
- It adds a Start-menu shortcut and, if you choose, a desktop shortcut.
- You can uninstall the app from **Settings → Apps**.
- Your solves are stored in `%APPDATA%\EnigmaTimer` and are kept when you update or uninstall.

## Keyboard shortcuts

| Key | Action |
|---|---|
| Space | Hold until the time turns green, then release to start |
| Any key / click | Stop the timer |
| Esc | Cancel inspection |
| Ctrl+1 / Ctrl+2 / Ctrl+3 | Mark the last solve OK / +2 / DNF |
| Ctrl+Z | Delete the last solve |
| N | New scramble |
| M | Minimal mode |
| Ctrl+E | Enter a time manually (`12.34`, `1:05.20`, `1234`, `DNF`, `14.00+`) |
| Ctrl+, | Settings |

You can also start the timer with the mouse: press and release on the time.

## Building from source

**Run it during development:**

```
pip install -r requirements.txt
python main.py
```

**Build the installer on Windows:**

1. Install Python 3.8+ from [python.org](https://www.python.org/downloads/). Tick **"Add python.exe to PATH"** during setup.
2. Double-click **`build_installer.bat`**. The script:
   - installs PyQt5, PyInstaller and Pillow;
   - builds the app;
   - installs Inno Setup via winget if it's missing;
   - creates the installer.
3. When it finishes, the `Output` folder opens with `EnigmaCube-Setup-2.2.exe` inside.

**Build on GitHub Actions:** every push to `main` builds the installer automatically. Download it from **Actions → Build Windows installer → EnigmaCube-Setup**. If you push a tag such as `v2.2`, the installer is also attached to a GitHub Release.

**Run the tests:**

```
python -m unittest discover -s tests
```

**Release a new version:** update the version number in three places:
- `enigma_timer/__init__.py`
- `installer/EnigmaCube.iss` (`MyAppVersion`)
- `installer/version_info.txt`

Don't change the `AppId` in the `.iss` file. The installer uses it to recognise an update.

## Project structure

```
main.py                  entry point
enigma_timer/
  scramble.py            scramble generators
  cube.py                NxN cube simulator for previews
  puzzles.py             Pyraminx, Skewb and Square-1 simulators for previews
  stats.py               solves, WCA averages, formatting
  storage.py             persistence, csTimer import, CSV export
  window.py              main window and timer state machine
  widgets.py             timer display, preview, charts
  dialogs.py             settings, solve details, about
  theme.py, i18n.py      styling and translations
assets/                  logo and icons (app.ico for the exe)
installer/               Inno Setup script, wizard images, exe version info
build_installer.bat      one-click installer build
.github/workflows/       automatic installer build on GitHub
tests/test_core.py       unit tests
```

## Changelog

### 2.2: minimal redesign
- The UI has no borders or outlines. Cards are a shade lighter than the background, and the right column is now a single card.
- Buttons are quiet text that appears on hover. Yellow is used only where it means something: the selected event, PBs and penalties.
- Events in the header are now text tabs with a yellow underline.
- The scramble no longer sits in a box. The timer uses a lighter font, and there is more spacing.
- New minimal mode (**M**).
- The title bar is dark on Windows 10 and 11.
- The distribution chart now uses horizontal bars and appears after 5 solves.

### 2.1
- New Enigma Cube logo, window icon and exe icon. The UI colours are taken from the logo.
- Scramble previews for Pyraminx, Skewb and Square-1.
- New events: OH, 3BLD (with random `Rw Uw` orientation) and FMC (`R' U' F … R' U' F`).
- A distribution tab next to the progress chart.
- The installer is now built with one click, and the interface language follows the system.
- Fixed a Square-1 model bug that could produce scrambles you couldn't do on a real puzzle.

### 2.0: full rewrite
The app was rewritten from the original prototype. These bugs in the old version were fixed:
- 5x5 stopped generating new scrambles after a solve.
- Pyraminx, Skewb and Megaminx scrambles contained cube moves such as D and F.
- ao5 and ao12 were plain means without trimming and reset every 5 or 12 solves.
- The UI froze on every scramble because of network requests to google.com and an image server.
- The timer started when Space was pressed instead of when it was released.
- Images were loaded relative to the current folder, so the app crashed when launched from elsewhere.
