import os
from cx_Freeze import setup, Executable

# Inclui toda a pasta assets (imagens, sons, etc.)
include_files = [("assets", "assets")]

executables = [
    Executable(
        'main.py',
        icon='assets/images/icon.ico'
    )
]

setup(
    name="PoliRush",
    version="1.0",
    description="Police Rush App",
    options={
        "build_exe": {
            "packages": ["pygame"],
            "include_files": include_files
        }
    },
    executables=executables
)
