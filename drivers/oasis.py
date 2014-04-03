#!/usr/bin/env python
# coding: utf-8
"""
The payu interface for the CICE model
-------------------------------------------------------------------------------
Contact: Marshall Ward <marshall.ward@anu.edu.au>
-------------------------------------------------------------------------------
Distributed as part of Payu, Copyright 2011-2012 Marshall Ward
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0
"""

# Standard Library
import os
import sys
import shlex
import shutil
import subprocess as sp

# Local
from ..fsops import mkdir_p
from ..modeldriver import Model

class Oasis(Model):

    #---
    def __init__(self, expt, name, config):
        super(Oasis, self).__init__(expt, name, config)

        self.model_type = 'oasis'
        self.copy_inputs = True

        # NOTE: OASIS3 uses an executable, but OASIS4 does not
        # TODO: Detect version?
        # if oasis_version == 3: self.default_exec = 'oasis'

        self.modules = ['pbs',
                        'openmpi']

        self.config_files = ['namcouple']


    def setup(self):
        super(Oasis, self).setup()

        # Copy OASIS data to the other submodels

        # TODO: Parse namecouple to determine filelist
        # TODO: Let users map files to models
        input_files = [f for f in os.listdir(self.work_path)
                        if not f in self.config_files]

        for model in self.expt.models:

            # Skip the oasis self-reference
            if model == self:
                continue

            mkdir_p(model.work_path)
            for f_name in self.config_files:
                f_path = os.path.join(self.work_path, f_name)
                f_sympath = os.path.join(model.work_path, f_name)
                os.symlink(f_path, f_sympath)

            mkdir_p(model.work_input_path)
            for f_name in input_files:
                f_path = os.path.join(self.work_path, f_name)
                f_sympath = os.path.join(model.work_input_path, f_name)
                os.symlink(f_path, f_sympath)
