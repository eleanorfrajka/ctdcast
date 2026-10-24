"""The deprecated ``ctdcast.plotters.plots`` façade warns and re-exports the split modules."""

import importlib
import sys

import pytest

from ctdcast.plotters import ladcp, maps, profiles, sections, timeseries


def test_plots_facade_warns_and_reexports():
    sys.modules.pop("ctdcast.plotters.plots", None)
    with pytest.warns(DeprecationWarning, match="ctdcast.plotters.plots is split"):
        plots = importlib.import_module("ctdcast.plotters.plots")
    for mod in (maps, profiles, sections, timeseries, ladcp):
        for name in dir(mod):
            obj = getattr(mod, name)
            if (
                not name.startswith("_")
                and callable(obj)
                and getattr(obj, "__module__", None) == mod.__name__
            ):
                assert getattr(plots, name) is obj, name
                assert name in plots.__all__, name


def test_no_internal_caller_imports_the_facade():
    """Package code imports the subject modules, so the warning never fires in-tree."""
    from pathlib import Path

    pkg = Path(importlib.import_module("ctdcast").__file__).parent
    offenders = [
        str(p.relative_to(pkg))
        for p in pkg.rglob("*.py")
        if p.name != "plots.py"
        and "ctdcast.plotters.plots import" in p.read_text(encoding="utf-8")
    ]
    assert offenders == []
