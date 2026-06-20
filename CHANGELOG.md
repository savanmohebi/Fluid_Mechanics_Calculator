# Changelog

## v1.1

### Fixed

- Fixed the v1.1 dashboard launch flow by standardizing the enhanced entry point as `main.py`.
- Fixed module-button startup failures caused by old filenames such as `FLUID_PROPERTIES_GUI.py`, `fluid_dynamic_gui.py`, and `DIMENSIONAL_ANALYSIS_GUI.py`.
- Fixed broken imports after file renaming by using package imports from `src.engines`.
- Fixed fragile working-directory assumptions by launching module GUIs with `python -m` from the v1.1 project root.

### Changed

- Reorganized the application into a maintainable `v1.1` folder.
- Moved calculation engines into `src/engines`.
- Moved GUI windows into `src/gui`.
- Added package `__init__.py` files for reliable imports.
- Renamed confusing uppercase and versioned filenames to Python-safe names.
- Updated `requirements.txt` to contain only pip-installable external dependencies.

### Documentation

- Rewrote `README.md` with structure, installation, run commands, dependencies, and troubleshooting.
- Kept `USER_GUIDE.md` with the v1.1 documentation set.

### Project Cleanup

- Moved older entry points, packaging scripts, generated caches, and uncertain files into `legacy_or_old_versions`.
- Left a locked root `dist` executable in place because Windows/WSL refused removal, but a backup copy exists in `legacy_or_old_versions/dist`.
