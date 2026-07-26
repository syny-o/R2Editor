# Requirement coverage

Coverage connects requirement identifiers from requirement modules to script
files below the active project directory.

## Reference syntax

The editor recognizes comma-separated references in script constructs matching
either `REFERENCE` or `$REF:`. Matching is case-insensitive and identifiers are
normalized to lowercase.

## Calculation

Each requirement module has a `coverage_filter`. Requirements selected by that
filter become keys in the module's `coverage_dict`:

```text
requirement identifier -> list of script paths
```

A requirement is:

- **covered** when its path list is non-empty;
- **not covered** when its path list is empty;
- **not calculated** when it is absent from `coverage_dict`;
- **ignored** when it is removed from coverage and stored in `ignore_list`.

Ignored requirements can also carry notes.

## Update paths

### Physical scan

`CoverageWorker` scans scripts below `disk_project_path` in a background Qt
worker. `CoverageController` applies the resulting reference-to-file mapping to
all modules with an active coverage filter.

### Editor save

When a document is saved, `DocumentActions` compares references in the original
and updated text. Changed identifiers are emitted to `DataManager`, which
updates affected modules without rescanning the complete project.

After either update, R2Editor refreshes requirement icons, summary counters and
the coverage chart and marks the project as modified when data changed.

