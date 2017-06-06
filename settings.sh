# Create app environment
docker-machine create qfphost -d virtualbox --virtualbox-share-folder /sw/apps2/qualibrate:/home/docker/app --virtualbox-cpu-count 3
docker-machine create qfphost -d virtualbox --virtualbox-share-folder /sw/apps2/qualibrate:/home/docker/app --virtualbox-cpu-count 3 --virtualbox-boot2docker-url "file://$HOME/Downloads/CentOS-7-x86_64-Minimal-1611.iso"


# Docker compose
curl -L https://github.com/docker/compose/releases/download/1.13.0/docker-compose-`uname -s`-`uname -m` > docker-compose
chmod +x docker-compose

# Set environment for host
eval $(docker-machine env qfphost)

# Monitoring system
docker run -d -p 9000:9000 --name qfp-mon -v "/var/run/docker.sock:/var/run/docker.sock" portainer/portainer

# Create the swam initialisation
docker swarm init --advertise-addr eth1

# Create an internal network
docker network create -d bridge qfp-nw

# Create data volume
docker volume create --name=qfp-data
docker volume create --driver local --opt type=btrfs --opt device=/home/docker/app/.data qfp-data
docker volume create --driver local --opt type=btrfs --opt device=/home/docker/app/.data --opt o=size=100m,uid=1000:50 qfp-data
docker volume create --driver local --opt type=btrfs --opt device=/mnt/sda1/qfp-data qfp-data

# Web Server
docker run --name qfp-web --network qfp-nw -v /home/docker/app/static:/usr/share/nginx/html:ro -v /home/docker/app/nginx.conf:/etc/nginx/nginx.conf:ro -p 80:80 -d nginx


# Creates instance for database
docker run -d --name qfp-db -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=qfp_active -p 3306:3306 --network qfp-nw -v qfp-data:/var/lib/mysql mysql:5.7
docker run -d --name qfp-db -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=qfp_active -p 3306:3306 --network qfp-nw -v /home/docker/app/.data:/var/lib/mysql:rw mysql:5.7

# Build the app
docker build -t qfpapi --build-arg FLASK_ENV=production .

# Run the app
docker run -d --name qfp-app -p 5000:5000 --network qfp-nw qfpapi

# Run script
docker exec -it qfp-app bash -c 'orator migrate -c "database/orator_$FLASK_ENVIRONMENT.yml" -f'
docker exec -it qfp-app bash -c 'PYTHONPATH=.:models orator db:seed --seeder user_table_seeder -c "database/orator_$FLASK_ENVIRONMENT.yml" -d mysql -f'

# Creates user migration
orator make:model User -m
orator make:model Project -m

# Migrate
orator migrate -c database/orator_development.yml -d sqlite -f
orator migrate -c "database/orator_$FLASK_ENVIRONMENT.yml" -f

# Verify migration status
orator migrate:status -c database/orator_development.yml -d sqlite
orator migrate:status -c "database/orator_$FLASK_ENVIRONMENT.yml"

# Seed tables
PYTHONPATH=.:models orator db:seed --seeder user_table_seeder -c database/orator_development.yml -d sqlite -f
PYTHONPATH=.:models orator db:seed --seeder user_table_seeder -c "database/orator_$FLASK_ENVIRONMENT.yml" -d mysql -f

# Full Database refresh
PYTHONPATH=.:models orator migrate:refresh -c database/orator_development.yml -d sqlite -f
PYTHONPATH=.:models orator migrate:refresh -c "database/orator_$FLASK_ENVIRONMENT.yml" -d mysql -f

# Testing
PYTHONPATH=.:models python test/models/user_test.py

# Performance benchmarking
gunicorn -w 4 --worker-class=tornado app:APP
gunicorn -w 4 --worker-class="egg:meinheld#gunicorn_worker" app:APP
gunicorn -w 4 --worker-class=meinheld.gmeinheld.MeinheldWorker app:APP
wrk -c 10 -d 10 http://127.0.0.1:8000/users/6ef9d6dc46ff11e79d9a7831c1d2599c
wrk -c 10 -d 10 http://127.0.0.1:8000/users
wrk -c 10 -d 10 http://192.168.99.100:5000/users
