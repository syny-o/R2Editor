# Architecture overview

R2Editor is a Windows desktop application built with Python and PyQt5. It
combines a script editor with management of requirement, condition, DSpace and
A2L data.

The application starts in `main.py`. `MainWindow` acts as the composition root:
it creates the application-level controllers and delegates construction of the
main pages to `MainWindowBuilder`.

## Main areas

| Area | Responsibility |
|---|---|
| `main.py`, root modules | Application startup, composition and lifecycle |
| `dashboard/` | Home page and recent projects |
| `file_browser/` | Project directory navigation and file operations |
| `text_editor/` | Documents, tabs, editing, completion and outline |
| `data_manager/` | Project data tree, requirements, coverage, reports, DOORS and A2L |
| `components/` | Reusable widgets, highlighters and small utilities |
| `config/` | Icons, fonts, styles, settings application and constants |
| `dialogs/` | Shared dialogs |
| `ui/` | Generated PyQt UI classes and static UI resources |

## Application composition

`MainWindowBuilder` creates four pages in the central stacked widget:

1. Dashboard
2. Text editor tabs
3. Data manager
4. Application settings

`WindowController` controls navigation and window state. Feature-specific work
is delegated further:

- `EditorController` binds editor toolbar actions.
- `DocumentActions` opens, saves and locks documents.
- `EditorTabManager` manages both editor tab groups.
- `DataManager` owns the shared `QStandardItemModel` data tree.
- `ProjectActions` coordinates project-level open/save/new operations.
- `ApplicationLifecycle` checks unsaved documents and projects before exit.

## Important coupling

`text_editor` and `data_manager` currently depend on each other:

- saving a script emits changed requirement references to the data manager;
- the data manager can request that a referenced script be opened.

This is intentional application behavior but also the most important boundary
to watch when refactoring. Prefer exchanging signals or small interfaces over
adding more direct knowledge of the opposite feature.

See the [component UML diagram](../uml/architecture.puml) for the dependency
overview.

