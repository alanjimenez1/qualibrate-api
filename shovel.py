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
def install():
    '''Install all project dependencies'''
    print(subprocess.getoutput("pip install -r requirements.txt"))

@task
def test(module_folder):
    '''Test specific modules'''
    print(subprocess.getoutput("python -m unittest test/%s/*_test.py" % module_folder))

@task
def lint():
    '''Run linter on code'''
    print('{0:>10}'.format("apis: ") + Style.BRIGHT + Fore.CYAN + Fore.RESET + subprocess.getoutput("pylint apis").split("\n")[2].split(" ")[6])
    print('{0:>10}'.format("models: ") + Style.BRIGHT + Fore.CYAN + Fore.RESET + subprocess.getoutput("pylint models").split("\n")[2].split(" ")[6])
    print('{0:>10}'.format("app: ") + Style.BRIGHT + Fore.CYAN + Fore.RESET + subprocess.getoutput("pylint app").split("\n")[2].split(" ")[6])

@task
def data(table_name, rows=10, *columns):
    '''Returns a simple sample of data from the database'''
    parameters = '*'
    if columns:
        parameters = ','.join(columns)

    print(subprocess.getoutput('sqlite3 -header -column database/development.sqlite "select %s from %s limit %s"' % (parameters, table_name, rows)))


@task
def stats():
    '''Code analysis ⌜:files ⌟:comments ␣:blank ⌞:lines'''
    result = subprocess.getoutput('cloc . | grep -e "^SUM:"')
    files, blank, comment, code = [x for x in result.split(" ") if x != '' and x.isnumeric() ]
    print(Style.BRIGHT + Fore.CYAN + ('⌜' + Fore.RESET + '{0:<4}').format(str(files)) , end=' ')
    print(Style.BRIGHT + Fore.CYAN + ('⌟' + Fore.RESET + '{0:<4}').format(str(comment)) , end=' ')
    print(Style.BRIGHT + Fore.CYAN + ('␣' + Fore.RESET + '{0:<4}').format(str(blank)) , end=' ')
    print(Style.BRIGHT + Fore.CYAN + ('⌞' + Fore.RESET + '{0:<4}').format(str(code)) )
