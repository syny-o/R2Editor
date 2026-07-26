# Testing

Tests use Python's standard `unittest` framework and live in `tests/`.

Run the complete suite from the repository root:

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

Run one module:

```powershell
python -m unittest tests.test_coverage_data
```

The suite focuses primarily on logic that can run without displaying the PyQt
application, including:

- file parsers and serializers;
- coverage rules and scanning;
- requirement comparison, export and references;
- editor text operations and outline parsing;
- filesystem operations;
- recent-project handling.

When adding behavior, keep parsing and transformation logic outside widgets
where possible. This allows it to be tested without creating a Qt event loop.

