# SPDX-License-Identifier: GPL-2.0-or-later
"""Cinzel (OFL) — roman capitals close to the Uncharted logo; bundled under launcher/fonts/."""
from pathlib import Path
import sys


def resource_root():
    meipass = getattr(sys, '_MEIPASS', None)
    if meipass and (Path(meipass) / 'fonts').is_dir():
        return Path(meipass)
    return Path(__file__).resolve().parent


def font_path(name):
    path = resource_root() / 'fonts' / name
    return path if path.is_file() else None
