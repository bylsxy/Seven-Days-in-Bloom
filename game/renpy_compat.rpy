"""Ren'Py compatibility helpers for newer engine versions."""

init -999 python:
    import renpy

    # Some Ren'Py releases move public helpers into the ``renpy.exports``
    # module. Fall back to that module when an attribute is no longer exported
    # at the top level so existing scripts keep working across versions.
    _renpy_exports = getattr(renpy, "exports", None)
    if _renpy_exports is None:
        try:
            from renpy import exports as _renpy_exports
        except Exception:
            _renpy_exports = None

    def _copy_from_exports(attr_name):
        if _renpy_exports and hasattr(_renpy_exports, attr_name) and not hasattr(renpy, attr_name):
            setattr(renpy, attr_name, getattr(_renpy_exports, attr_name))

    # Restore helpers that were available in older Ren'Py versions.
    _copy_from_exports("get_side_image")
    _copy_from_exports("list_files")

    if not hasattr(renpy, "list_files"):
        loader = getattr(renpy, "loader", None)
        if loader and hasattr(loader, "listdirfiles"):
            def _compat_list_files():
                for entry in loader.listdirfiles():
                    yield entry

            renpy.list_files = _compat_list_files
