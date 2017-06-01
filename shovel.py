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
    '''Test specific modules'''
    print(subprocess.getoutput("python -m unittest test/%s/*_test.py -v" % module_folder))

@task
def lint():
    '''Run linter on code'''
    print(subprocess.getoutput("pylint ."))

@task
def data_sample(table_name, rows=10):
    '''Returns a simple sample of data from the database'''
    print(subprocess.getoutput('sqlite3 -header -column database/development.sqlite "select * from %s limit %s"' % (table_name, rows)))


@task
def stats():
    '''Code analysis ⌜:files ⌟:comments ␣:blank ⌞:lines'''
    result = subprocess.getoutput('cloc . | grep -e "^SUM:"')
    files, blank, comment, code = [x for x in result.split(" ") if x != '' and x.isnumeric() ]
    print(Style.BRIGHT + Fore.CYAN + "⌜" + Fore.RESET + str(files) , end=' ')
    print(Style.BRIGHT + Fore.CYAN + "⌟" + Fore.RESET + str(comment) , end=' ')
    print(Style.BRIGHT + Fore.CYAN + "␣" + Fore.RESET + str(blank) , end=' ')
    print(Style.BRIGHT + Fore.CYAN + "⌞" + Fore.RESET + str(code) )