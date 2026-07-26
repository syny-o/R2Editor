# Local setup

R2Editor is a Windows-oriented Python/PyQt5 desktop application.

## Runtime dependencies

Imports in the current source tree require at least:

- PyQt5
- pywinstyles
- qtawesome
- openpyxl

The repository does not currently contain a pinned dependency file. Install the
packages into a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install PyQt5 pywinstyles qtawesome openpyxl
```

Start the application from the repository root:

```powershell
python main.py
```

Running from the root is important because UI resources and `app_config.ini`
are accessed using relative paths.

## Configuration

User-facing settings are stored in `app_config.ini` through `QSettings`.
Currently supported groups include:

- `project/recent`
- `general/autosave`
- `appearance/theme`
- `editor/format_code_when_save`
- `doors/doors_app_path`
- `doors/doors_database_path`
- `doors/doors_user_name`

Do not commit machine-specific paths or credentials.

