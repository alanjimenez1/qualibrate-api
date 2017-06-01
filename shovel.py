from shovel import task
import subprocess

@task
def dbstatus(name):
	'''Prints hello and the provided name'''
	print(subprocess.getoutput("orator migrate:status --config=database/orator.yml -d %s" % name))
