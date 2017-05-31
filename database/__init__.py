from orator import DatabaseManager
import yaml
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(base_dir, "orator.yml")

with open(config_file, "r") as file:
    config = yaml.load(file)


db = DatabaseManager(config['databases'])
