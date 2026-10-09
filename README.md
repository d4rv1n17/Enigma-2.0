# Enigma Cube Timer 3.0

A speedcubing timer for Windows, built with Python and PyQt5. It works fully offline.

Enigma Cube generates WCA-style scrambles and shows a preview of each one. It times solves like a Stackmat and tracks your averages and personal bests.

## Features

### Training (new in 3.0)
- **Learning path in 7 steps:**
  1. Notation
  2. Beginner method
  3. 2-look OLL
  4. 2-look PLL
  5. F2L
  6. Full OLL
  7. Full PLL
- **Algorithm database:** 7 beginner algorithms, F2L 41, OLL 57, PLL 21, plus the 2-look subsets. Algorithms come from speedcubedb.com, cubingcheatsheet.com and ruwix.com, and each one is checked by the tests with a cube simulator.
- **Case pictures:** OLL patterns, PLL with arrows and F2L in 3D, all generated from the algorithms themselves.
- **Spaced-repetition trainer:**
  - Recognise the case, solve it on your cube, reveal the algorithm and rate yourself (1–3).
  - Cases move through Leitner boxes: review now, then after 1 day, 3, 7, 16 and 35 days.
  - New cases are introduced 4 at a time.
- **Multi-window mode:** open Training in its own window (**⧉**) next to the timer. Pin it on top of other windows if you like.

### Timer and statistics

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

1. Download `EnigmaCube-Setup-3.0.exe` and run it.
2. If Windows shows **"Windows protected your PC"**, click **More info → Run anyway**. Windows shows this for new apps that don't have a paid code-signing certificate.
3. Choose the folder and shortcuts, then click **Install**. If an older version is installed, the button says **Update**.

The installer has these properties:
- It has its own design and follows the Windows language (RU/EN), which you can switch at the top right.
- It doesn't need administrator rights.
- It updates an existing installation in place, including 2.2 installs made with the old Inno Setup installer.
- You can uninstall the app from **Settings → Apps**. You can also delete your solves when you uninstall.
- Your solves are stored in `%APPDATA%\EnigmaTimer` and are kept when you update.

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

In the trainer: **Space** reveals the algorithm, **1 / 2 / 3** rates it (forgot / hard / knew it), **Esc** goes back.

You can also start the timer with the mouse: press and release on the time.

## Building from source

**Run it during development:**

```
pip install -r requirements.txt
python main.py
```

**Build the installer on Windows:**

1. Install Python 3.8+ from [python.org](https://www.python.org/downloads/). Tick **"Add python.exe to PATH"** during setup.
2. Double-click **`build_installer.bat`**. It installs PyQt5 and PyInstaller and runs `installer/build.py`, which:
   - builds the app;
   - builds the uninstaller;
   - packs the app;
   - creates the setup.
3. When it finishes, the `Output` folder opens with `EnigmaCube-Setup-3.0.exe` inside.

**Build on GitHub Actions:** every push and pull request builds the installer automatically. Download it from **Actions → Build Windows installer → EnigmaCube-Setup**. If you push a tag such as `v3.0`, the installer is also attached to a GitHub Release.

**Run the tests:**

```
python -m unittest discover -s tests
```

**Release a new version:** change `VERSION` in `enigma_timer/__init__.py`. The build script uses this number everywhere.

## Project structure

```
main.py                  entry point
enigma_timer/
  scramble.py            scramble generators
  cube.py                NxN cube simulator for previews
  fast3.py               fast 3x3 simulator for the training section
  algs.py                algorithm database (beginner, F2L, OLL, PLL)
  learn.py               learning path and spaced repetition
  lessons.py             lesson texts (EN/RU)
  caseview.py            case pictures (OLL, PLL arrows, F2L 3D)
  training.py            Training section and separate Training windows
  puzzles.py             Pyraminx, Skewb and Square-1 simulators for previews
  stats.py               solves, WCA averages, formatting
  storage.py             persistence, csTimer import, CSV export
  window.py              main window and timer state machine
  widgets.py             timer display, preview, charts
  dialogs.py             settings, solve details, about
  theme.py, i18n.py      styling and translations
assets/                  logo and icons (app.ico for the exe)
installer/               custom setup: setup_app.py (window), setup_core.py (logic), build.py
build_installer.bat      one-click installer build
.github/workflows/       automatic installer build on GitHub
tests/                   unit tests (scrambles, stats, every algorithm, setup logic)
```

## Changelog

### 3.0: Training
- A new **Training** section with a learning path, lessons, 140+ verified CFOP algorithms and a spaced-repetition trainer.
- **Multi-window mode:** Training can be opened in separate windows next to the timer.
- A new custom installer replaces Inno Setup. It installs, updates and uninstalls the app, and switches between RU and EN.
- The 3x3 simulator now supports `x y z`, `M E S` and wide moves (`r`, `Rw`).

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
