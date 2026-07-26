# Condition file format

Condition files are XML-like text files represented in the data tree as:

```text
ConditionFileNode
└── ConditionNode
    └── ValueNode
        └── TestStepNode
```

Example:

```xml
<?xml version="1.0"?>
<Conditions>
  <Condition Name="Ignition" Type="Input">
    <Value Name="On" Type="Boolean">
      <TS Name="Set ignition" A="Set" Nominal="1" Comment="required" />
    </Value>
  </Condition>
</Conditions>
```

The parser recognizes these attributes:

| Element | Attributes |
|---|---|
| `Condition` | `Name`, `Type` |
| `Value` | `Name`, `Type` |
| `TS` | `Name`, `A`, `Nominal`, `Comment` |

Parsing and serialization are implemented in
`data_manager/condition_file_format.py`.

