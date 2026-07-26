# R2Editor UML diagrams

The diagrams are maintained as PlantUML source:

- `architecture.puml` — packages and feature-level dependencies
- `data-model.puml` — the `QStandardItem`-based project data trees
- `controllers.puml` — application shell, controllers and delegated actions

## Rendering

With PlantUML installed:

```powershell
plantuml -tsvg docs/uml/*.puml
```

Alternatively, install the PlantUML extension in VS Code and open a `.puml`
file to preview or export it.

The older `R2_Class_Diagram.uxf` remains compatible with UMLet, but it reflects
an earlier design where more responsibilities lived directly in `MainWindow`.
