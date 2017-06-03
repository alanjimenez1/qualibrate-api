from orator import DatabaseManager
import yaml
import os

try:
    current_environment = os.environ['FLASK_ENV']
except KeyError:
    current_environment = 'development'

base_dir = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(base_dir, "orator_%s.yml" % current_environment)

with open(config_file, "r") as file:
    config = yaml.load(file)


db = DatabaseManager(config['databases'])
