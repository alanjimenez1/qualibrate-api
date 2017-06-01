# Creates instance for database
docker run --name mysqldb -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 -d mysql:5.7

# Creates user migration
orator make:model User -m
orator make:model Project -m

# Migrate
orator migrate -c database/orator.yml -d sqlite

# Verify migration status
orator migrate:status -c database/orator.yml -d sqlite

# Seed tables
PYTHONPATH=.:models orator db:seed --seeder user_table_seeder -c database/orator.yml -d sqlite -f

# Full Database refresh
PYTHONPATH=.:models orator migrate:refresh --seed -c database/orator.yml -d sqlite -f

# Testing
PYTHONPATH=.:models python test/models/user_test.py
