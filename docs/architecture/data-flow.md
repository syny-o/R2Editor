# Data flow

## Opening a project

1. `ProjectActions.open()` asks the user for a project JSON file.
2. `data_manager.projects.manager.open_project()` reads the JSON.
3. The manager updates project parameters and notifies registered listeners.
4. `ProjectDataController.receive_project_data()` clears the existing model.
5. Condition, DSpace, A2L and requirement-module loaders recreate root nodes.
6. The data summary and editor completion data are refreshed.

## Editing project data

`DataManager` owns a `QStandardItemModel`. Its invisible root contains these
top-level node types:

- `ConditionFileNode`
- `DspaceFileNode`
- `A2lFileNode`
- `RequirementModule`

Feature controllers and actions modify this model. Inserted or removed rows
mark the project as modified. Condition and DSpace nodes additionally track
whether their source file must be rewritten.

## Saving a project

1. `ProjectActions.save()` calls the project manager.
2. The manager requests serializable data from `DataManager`.
3. `ProjectDataController.provide_project_data()` asks every root node for its
   project representation.
4. Modified condition and DSpace files are exported to their source files.
5. The combined project data is written to the project JSON.
6. Registered listeners receive the new saved state.

The project JSON therefore stores both file references and complete requirement
module snapshots. Condition, DSpace and A2L content remains in the referenced
source files.

## Requirement coverage

Coverage can change in two ways:

- a physical scan reads scripts below `disk_project_path`;
- saving an open script emits the symmetric difference of its old and new
  requirement references.

Both paths update the `coverage_dict` of affected requirement modules and then
refresh icons, counters and the coverage chart.

