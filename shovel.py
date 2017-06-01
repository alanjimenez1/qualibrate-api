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
from colorama import Fore, Back, Style, init
init(autoreset=True)

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

@task
def stats():
    '''Run lines of code analysis'''
    result = subprocess.getoutput('cloc . | grep -e "^SUM:"')
    files, blank, comment, code = [x for x in result.split(" ") if x != '' and x.isnumeric() ]
    #print(files, blank, comment, code)
    print(Fore.RED + Style.BRIGHT + "⌜" + str(files) + Fore.RESET, end=' ')
    print(Fore.YELLOW + Style.BRIGHT + "⌟" + str(comment) + Fore.RESET, end=' ')
    print(Fore.CYAN + Style.BRIGHT + "␣" + str(blank) + Fore.RESET, end=' ')
    print(Fore.GREEN + Style.BRIGHT + "⌞" + str(code) + Fore.RESET)
