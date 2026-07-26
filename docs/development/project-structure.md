# Project structure

```text
r2editor/
├── main.py                    application entry point and composition root
├── main_window_builder.py     construction of main pages and editor panels
├── window_controller.py       navigation and window presentation state
├── application_lifecycle.py   application close checks
├── app_settings.py            settings UI and persistence
├── components/                shared widgets, syntax highlighting and helpers
├── config/                    styles, icons, fonts and constants
├── dashboard/                 home page and recent projects
├── data_manager/              project model and data-oriented features
├── dialogs/                   reusable dialogs
├── doors/                     external DOORS process connection
├── file_browser/              filesystem tree and file operations
├── text_editor/               editor, documents, tabs, completion and outline
├── ui/                        generated PyQt UI modules and resources
├── tests/                     automated unit tests
└── docs/                      architecture and developer documentation
```

## Data manager subpackages

| Package | Purpose |
|---|---|
| `a2l/` | A2L parsing and normalization |
| `coverage/` | Requirement-reference scanning and coverage calculations |
| `doors/` | Parsing and handling downloaded DOORS data |
| `forms/` | Data-manager dialogs and editing forms |
| `html_report/` | HTML report validation |
| `nodes/` | `QStandardItem`-based project data nodes |
| `projects/` | Project lifecycle and JSON persistence |
| `requirements/` | Requirement loading, serialization, comparison and export |
| `view/` | Tree rendering, layouts, filters and view actions |

## Generated files

Files named `ui/*_ui.py` are generated representations of Qt Designer `.ui`
files. Prefer editing the `.ui` source and regenerating its Python module when
making layout changes.

