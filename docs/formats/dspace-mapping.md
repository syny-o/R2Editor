# DSpace mapping format

DSpace mappings are Python-like files organized into definition functions.
R2Editor extracts calls to `append` and represents them as:

```text
DspaceFileNode
└── DspaceDefinitionNode
    └── DspaceVariableNode
```

Example:

```python
def Engine():
    EngineVar = []
    EngineVar.append(["Speed", 0, "Model/Speed"])
    return EngineVar
```

Each variable stores:

- variable name (`Speed`);
- value (`0`);
- model path (`Model/Speed`).

The parser preserves text before the first definition as the header and the
last definition block as the footer. Parsing and serialization are implemented
in `data_manager/dspace_mapping.py`.

