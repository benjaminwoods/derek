from setuptools import setup
from setuptools.config import read_configuration
from pathlib import Path

cfg = read_configuration(Path(__file__).parent / "python/setup.cfg")
setup(
    **{
        "packages": ["derek"],
        "package_dir": {"": "python/src"},
        **cfg.get("metadata", {}),
    }
)
