import os

from ProgramData import SYSTEMDIR

SYSTEM_JSON = os.path.join(SYSTEMDIR, "system.json")

from ProgramFiles.flaskr.mymod.system._system import SystemDictionary

system = SystemDictionary()