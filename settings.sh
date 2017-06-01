# Creates instance for database
docker run --name mysqldb -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 -d mysql:5.7

# Creates user migration
orator make:model User -m

# Verify migration status
orator migrate:status -c database/orator.yml -d sqlite
