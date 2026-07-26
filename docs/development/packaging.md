# Packaging

The existing packaging command builds a windowed Windows executable with
PyInstaller:

```powershell
pyinstaller -w --icon=R2Editor.ico --name=R2Editor main.py
```

Install PyInstaller into the active virtual environment first:

```powershell
python -m pip install pyinstaller
```

The generated application is placed below `dist/R2Editor/` or as a single
executable depending on the selected PyInstaller mode.

Before distributing a build, verify that these runtime resources are included:

- `app_config.ini` or appropriate default configuration;
- Qt Designer/UI resources required at runtime;
- `ui/icons/`;
- `ui/fonts/`;
- `doors_downloader.dxl` when DOORS integration is required.

The current repository contains only a command reminder in `pyinstaller.txt`;
it does not yet contain a versioned `.spec` file. A `.spec` file is preferable
once resource inclusion and release packaging need to be reproducible.

