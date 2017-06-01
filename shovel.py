# -*- coding: utf-8 -*-
"""
Software development project
administration tasks
"""

__author__ = "@canimus"
__license__ = "MIT"
__revision__ = "1.0"

import subprocess
from shovel import task

@task
def dbstatus(name):
    '''Provides the status of the current migrations'''
    print(subprocess.getoutput("orator migrate:status --config=database/orator.yml -d %s" % name))

@task
def install():
    '''Install all project dependencies'''
    print(subprocess.getoutput("pip install -r requirements.txt"))

@task
def test(module_folder):
    '''Test all models'''
    print(subprocess.getoutput("python -m unittest test/%s/*_test.py -v" % module_folder))

@task
def lint(prefix="E"):
    '''Run linter on code'''
    print(subprocess.getoutput("pylint . | grep --colour -e \"^%s\"" % prefix))
