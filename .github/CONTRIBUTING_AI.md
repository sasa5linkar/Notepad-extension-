# Guidelines for AI Agents and Code Assistants

This document provides essential information for AI assistants (like GitHub Copilot, ChatGPT, Claude, etc.) working on this project.

## 🔴 CRITICAL: Python Version Compatibility

**The Notepad++ PythonScript scripts in this repository MUST be compatible with Python 2.7.**

### Why Python 2.7?

The **PythonScript plugin** for Notepad++ (version 2.x) uses **Python 2.7** as its runtime environment. While the plugin also has Python 3.x versions available, the most common and stable version distributed through Notepad++ Plugin Admin is Python 2.7-based.

### Compatibility Requirements for `/scripts/*.py` Files

All scripts in the `/scripts/` directory that are meant to run inside Notepad++ via PythonScript plugin **MUST**:

1. **Use Python 2.7-compatible syntax**
   - ❌ NO f-strings: `f"Hello {name}"`
   - ✅ USE .format(): `"Hello {0}".format(name)`
   - ❌ NO type hints: `def func(x: int) -> str:`
   - ✅ USE docstrings for documentation

2. **Use only standard library modules**
   - ✅ Only use modules included in Python 2.7 standard library
   - ❌ NO external dependencies (no pip packages)
   - ❌ NO imports that require installation
   - ✅ Common safe imports: `sys`, `os`, `re`, `datetime`, `xml.etree.ElementTree`, etc.

3. **Import from Npp module**
   - All Notepad++ scripts use: `from Npp import editor, notepad`
   - The `Npp` module is provided by PythonScript plugin
   - Not available outside Notepad++ environment

### Example of Compliant Code

```python
# -*- coding: utf-8 -*-
"""
Script description here.
"""

from Npp import editor

# Get selected text
sel = editor.getSelText()

# If selection exists, wrap it in a tag
if sel:
    editor.replaceSel("<tag>{0}</tag>".format(sel))
```

### Example of NON-Compliant Code

```python
# ❌ WRONG - This will NOT work with Python 2.7!

from Npp import editor

def wrap_text(tag: str) -> None:  # ❌ Type hints (Python 3.5+)
    sel = editor.getSelText()
    if sel:
        editor.replaceSel(f"<{tag}>{sel}</{tag}>")  # ❌ f-strings (Python 3.6+)
```

## Python Version for Other Files

### `/install.py` and `/tests/*.py`

These files are **NOT** run inside Notepad++ and can use modern Python:
- ✅ Requires Python 3.8+ (see `.github/workflows/test.yml`)
- ✅ Can use f-strings, type hints, and modern syntax
- ✅ Can use pathlib, dataclasses, and other modern features
- ✅ Can import from standard library modules available in Python 3.8+

The project CI tests these files with Python 3.8 through 3.12 on Ubuntu and Windows.

## Code Style Guidelines

### For `/scripts/*.py` (Notepad++ Scripts)

1. **Keep it simple**: Use basic Python 2.7 syntax
2. **No dependencies**: Only use `Npp` module and Python 2.7 standard library
3. **UTF-8 encoding**: Always include `# -*- coding: utf-8 -*-` at the top
4. **String formatting**: Use `.format()` instead of f-strings or `%` formatting
5. **Error handling**: Use simple try/except, avoid complex exception chaining
6. **Comments**: Minimal comments; code should be self-explanatory

### For `/install.py` and `/tests/*.py`

1. **Modern Python**: Use Python 3.8+ features freely
2. **Type hints**: Optional but encouraged for clarity
3. **Pathlib**: Use `pathlib.Path` for file operations
4. **String formatting**: f-strings are preferred

## Testing

### Manual Testing in Notepad++

When adding new scripts to `/scripts/`:
1. Copy script to Notepad++ PythonScript scripts folder
2. Open Notepad++, select some text
3. Run the script via Plugins → PythonScript → Scripts
4. Verify the text is wrapped correctly
5. Test undo (Ctrl+Z) to ensure it works

### Automated Testing

The project has comprehensive tests in `/tests/`:
- Run all tests: `python -m unittest discover -s tests -v`
- Tests mock the `Npp` module for testing scripts outside Notepad++
- CI automatically tests on Python 3.8-3.12, Ubuntu & Windows

## Common Pitfalls to Avoid

1. **Using modern Python syntax in `/scripts/`**
   - Remember: Notepad++ scripts run on Python 2.7
   - Test syntax compatibility before committing

2. **Adding external dependencies**
   - PythonScript environment doesn't support pip
   - Only standard library is available

3. **Breaking existing scripts**
   - All changes should maintain backward compatibility
   - Run existing tests before committing

4. **Ignoring encoding**
   - Always use UTF-8 encoding declaration
   - Important for non-ASCII characters (project uses Serbian Cyrillic)

## File Structure

```
.
├── scripts/           # Python 2.7 compatible Notepad++ scripts
│   ├── wrap_*.py      # Main wrap scripts (Python 2.7)
│   └── test_scripts.py # Test harness (Python 2.7)
├── tests/             # Python 3.8+ unit tests
│   ├── test_wrap_scripts.py
│   └── test_install.py
├── install.py         # Python 3.8+ installer script
└── install.bat        # Windows batch file launcher
```

## Quick Reference: Python 2.7 vs 3.x

| Feature | Python 2.7 (scripts/) | Python 3.8+ (tests/, install.py) |
|---------|----------------------|-----------------------------------|
| String formatting | `.format()` | f-strings preferred |
| Print | `print "text"` or `print("text")` | `print("text")` |
| Type hints | ❌ Not available | ✅ Available |
| Unicode strings | `u"text"` | `"text"` (default) |
| Division | `/` is integer division | `/` is true division |
| Import | `from Npp import ...` | Standard imports |

## Summary for AI Agents

When modifying or creating files:

1. **Check the file location first**:
   - In `/scripts/`? → Use Python 2.7 syntax
   - In `/tests/` or `install.py`? → Use Python 3.8+ syntax

2. **For `/scripts/*.py` files**:
   - Compatible with Python 2.7
   - Use `.format()` not f-strings
   - No type hints
   - Only standard library + Npp module
   - Keep it simple

3. **For all other `.py` files**:
   - Use modern Python 3.8+
   - Follow standard Python best practices

4. **Always run tests**:
   - `python -m unittest discover -s tests -v`
   - Manual test in Notepad++ if possible

## Questions?

If you're unsure about compatibility:
- Check existing scripts in `/scripts/` for examples
- Refer to README.md section on "Kompatibilnost" (Compatibility)
- When in doubt, use simpler, older syntax for `/scripts/`
