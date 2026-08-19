"""Bliss Point — a prompt compiler.

One task, shaped correctly for whichever agent receives it.
"""

from .brief import Brief, Gap, Subtask, Task
from .compiler import compile, cross_family
from .dials import DIAL_NAMES, DIAL_POLES, Dials
from .outcomes import record
from .profiles import ProfileError, list_profiles, load_profile, phases, resolve

__version__ = "0.1.0"
__all__ = [
    "Brief", "Gap", "Subtask", "Task", "Dials", "DIAL_NAMES", "DIAL_POLES",
    "ProfileError",
    "compile", "cross_family", "record",
    "list_profiles", "load_profile", "phases", "resolve",
]
