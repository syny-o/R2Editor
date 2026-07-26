# Project JSON format

The project JSON records the project directory, references to external data
files and snapshots of requirement modules.

## Top-level structure

```json
{
  "Conditions Files": ["D:/project/conditions.xml"],
  "DSpace Files": ["D:/project/mapping.py"],
  "A2L Files": ["D:/project/model.a2l"],
  "REQUIREMENT MODULES": [],
  "disk_project_path": "D:/project/scripts"
}
```

| Field | Meaning |
|---|---|
| `Conditions Files` | Paths to condition source files |
| `DSpace Files` | Paths to DSpace mapping files |
| `A2L Files` | Paths to A2L files |
| `REQUIREMENT MODULES` | Serialized DOORS requirement modules |
| `disk_project_path` | Directory scanned for scripts and requirement references |

Paths are currently stored as strings and may be absolute. Moving a project to
another workstation can therefore require updating paths.

## Requirement module

```json
{
  "path": "/Project/Module",
  "columns": ["Object Identifier", "Object Text"],
  "attributes": [],
  "baseline": {},
  "update_time": "2026-07-24",
  "coverage_filter": null,
  "coverage_dict": {},
  "ignore_list": [],
  "notes": {},
  "current_baseline": null,
  "column_number_as_identifier": 0,
  "requirements": []
}
```

A requirement entry contains:

```json
{
  "reference": "REQ-123",
  "heading": "",
  "level": 1,
  "outlinks": [],
  "inlinks": [],
  "file_references": ["D:/project/scripts/test.par"],
  "is_covered": true,
  "columns_data": ["REQ-123", "Requirement text"]
}
```

The hierarchy is serialized as a depth-first flat list. The `level` field is
used to rebuild the tree when the project is opened.

