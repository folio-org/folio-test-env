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
sudo apt-get install curl default-jdk git maven nodejs npm postgresql postgresql-contrib
```

## Update nodejs to the the newer version

```
sudo npm cache clean -f
sudo npm install -g n
sudo n stable
```

## Clone the Okapi repo and build it
```
git clone --recursive https://github.com/folio-org/okapi.git
cd okapi
mvn clean install
```

## Clone the auth module repo and build the 3 modules
```
cd ~ && git clone --recursive https://github.com/folio-org/mod-auth.git
cd ~/mod-auth/permissions_module && mvn clean install
cd ~/mod-auth/login_module && mvn clean install
cd ~/mod-auth/authtoken_module && mvn clean install
```

## Clone the folio-test-env repo
```
cd ~ && git clone --recursive git@github.com:folio-org/folio-test-env.git
```

## Build the nodejs sample modules we will be using

```
cd ~/folio-test-env/testing/thing_module && npm install
cd ~/folio-test-env/testing/retrieve_module && npm install
```

## Clone and build the mod-users repo
```
cd ~ && git clone --recursive https://github.com/folio-org/mod-users.git
cd ~/mod-users && mvn clean install
```

## Create symlinks in the testing directory for Okapi
```
cd ~/folio-test-env/testing/auth_test/ && ln -s ~/okapi/okapi-core/target okapi
```

## Create a symlink for mod-users
```
cd ~/folio-test-env/testing/auth_test/ &&  ln -s ~/mod-users/target mod-users
```

## Create a symlink for permssions module
```
cd ~/folio-test-env/testing/auth_test/ &&  ln -s ~/mod-auth/permissions_module/target permissions_module
```
## Create a symlink for login module
```
cd ~/folio-test-env/testing/auth_test/ &&  ln -s ~/mod-auth/login_module/target login_module
```
## Create a symlink for authtoken module
```
cd ~/folio-test-env/testing/auth_test/ &&  ln -s ~/mod-auth/authtoken_module/target authtoken_module
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

## Run the script to load the modules
```
cd ~/folio-test-env/testing/auth_test/
./run_me.sh
```

## Build and run the Mocha tests

```
cd ~/folio-test-env/testing/mocha_testing/
npm install
npm start
```
