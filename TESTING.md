# Testing the Auth environment in Vagrant

### Prerequisites: Vagrant installed on host system

## Initialize a Ubuntu 16.04 environment in Vagrant

```
vagrant box add bento/ubuntu-16.04
vagrant init bento/ubuntu-16.04
vagrant up
```

## SSH into your Vagrant box
```
vagrant ssh
```

## Install required software to run the demo

```
sudo apt-get update
sudo apt-get install curl default-jdk git maven postgresql postgresql-contrib virtualenv
```
## Clone the Okapi repo and build it
```
cd ~ && git clone --recursive https://github.com/folio-org/okapi.git
cd okapi
mvn clean install
```
## Clone and build the authtoken module
```
cd ~ && git clone https://github.com/folio-org/mod-authtoken.git
cd ~/mod-authtoken && git checkout dev && mvn clean install
```
## Clone and build the permissions module
```
cd ~ && git clone --recursive https://github.com/folio-org/mod-permissions.git
cd ~/mod-permissions && git checkout dev && mvn clean install
```
## Clone and build the login module
```
cd ~ && git clone --recursive https://github.com/folio-org/mod-login.git
cd ~/mod-login && git checkout dev && mvn clean install -DskipTests
```
## Clone and build the mod-users repo
```
cd ~ && git clone --recursive https://github.com/folio-org/mod-users.git
cd ~/mod-users && mvn clean install
```

## Clone and build the mod-users-bl repo
```
cd ~ && git clone --recursive https://github.com/folio-org/mod-users-bl.git
cd ~/mod-users-bl && mvn clean install
```
## Clone the folio-test-env repo
```
cd ~ && git clone --recursive https://github.com/folio-org/folio-test-env.git
```
## Create symlinks in the testing directory for Okapi
```
cd ~/folio-test-env/testing/auth_test/ && ln -s ~/okapi/okapi-core/target okapi
```

## Create a symlink for mod-users
```
cd ~/folio-test-env/testing/auth_test/ &&  ln -s ~/mod-users mod-users
```

## Create a symlink for permissions module
```
cd ~/folio-test-env/testing/auth_test/ &&  ln -s ~/mod-permissions mod-permissions
```
## Create a symlink for login module
```
cd ~/folio-test-env/testing/auth_test/ &&  ln -s ~/mod-login mod-login 
```
## Create a symlink for authtoken module
```
cd ~/folio-test-env/testing/auth_test/ &&  ln -s ~/mod-authtoken mod-authtoken
```

## Create a symlink for mod-users-bl module
```
cd ~/folio-test-env/testing/auth_test/ && ln -s ~/mod-users-bl mod-users-bl
```
## Initialize our Postgres data (and clear out any existing cruft)
```
sudo -u postgres bash -c "psql -c \"DROP DATABASE folio_backend;\""
sudo -u postgres bash -c "psql -c \"DROP ROLE diku_login_module;\""
sudo -u postgres bash -c "psql -c \"DROP ROLE diku_permissions_module;\""
sudo -u postgres bash -c "psql -c \"DROP ROLE diku_mod_users;\""
sudo -u postgres bash -c "psql -c \"DROP ROLE dbuser;\""
sudo -u postgres bash -c "psql -c \"CREATE USER dbuser WITH SUPERUSER PASSWORD 'qwerty';\""
sudo -u postgres bash -c "psql -c \"CREATE ROLE diku_login_module PASSWORD 'diku' NOSUPERUSER NOCREATEDB INHERIT LOGIN;\""
sudo -u postgres bash -c "psql -c \"CREATE ROLE diku_permissions_module PASSWORD 'diku' NOSUPERUSER NOCREATEDB INHERIT LOGIN;\""
sudo -u postgres bash -c "psql -c \"CREATE ROLE diku_mod_users PASSWORD 'diku' NOSUPERUSER NOCREATEDB INHERIT LOGIN;\""
sudo -u postgres bash -c "psql -c \"CREATE DATABASE folio_backend WITH OWNER=dbuser ENCODING 'UTF8' LC_CTYPE 'en_US.UTF-8' LC_COLLATE 'en_US.UTF-8' TEMPLATE 'template0';\""
sudo -u postgres bash -c "psql folio_backend < /home/vagrant/folio-test-env/testing/postgres/folio_backend.sql"
```

## Install python virtual env, run script to update deployment descriptors
```
cd ~/folio-test-env/testing/auth_test && virtualenv -p /usr/bin/python3 pyenv
./pyenv/bin/python generate_descriptors.py --batch_file_path descriptor_batch.json --allow_fail
```
## Run the script to load Okapi and the modules
```
cd ~/folio-test-env/testing/auth_test/
./run_me.sh && ./load_new_bl.sh
```
