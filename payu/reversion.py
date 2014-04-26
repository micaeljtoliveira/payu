# coding: utf-8

import os
import sys

import payu.envmod as envmod


def repython(version, script_path):

    # Establish the environment modules
    envmod.setup()

    # Ensure that payu is loaded
    try:
        envmod.module('use', os.environ['PAYU_MODULEPATH'])
        envmod.module('load', os.environ['PAYU_MODULENAME'])
    except KeyError:
        pass

    # NOTE: Older versions (<2.7) require the version as a tuple
    version_tuple = tuple(int(i) for i in version.split('.'))
    module_name = os.path.join('python', version)

    python_modules = [m for m in os.environ['LOADEDMODULES'].split(':')
                      if m.startswith('python')]

    if sys.version_info < version_tuple or not module_name in python_modules:

        # First unload all python (and supporting) modules
        python_modules = [m for m in os.environ['LOADEDMODULES'].split(':')
                          if m.startswith('python')]

        for mod in python_modules:
            envmod.module('unload', mod)

        # Replace with specified version
        envmod.module('load', module_name)

        # Replace the current python process with the updated version
        os.execl(script_path, *sys.argv)
