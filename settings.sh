# Create app environment
docker-machine create qfphost -d virtualbox --virtualbox-share-folder /sw/apps2/qualibrate:/home/docker/app --virtualbox-cpu-count 3

# Build the app
docker build -t qfpapi .

# Run the app
docker run -d --name qfpapi-01 -p 5000:5000 qfpapi

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

# Performance benchmarking
gunicorn -w 4 app:APP --worker-class tornado
wrk -c 10 -d 10 http://127.0.0.1:8000/users/6ef9d6dc46ff11e79d9a7831c1d2599c
