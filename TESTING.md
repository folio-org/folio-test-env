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
sudo add-apt-repository "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -sc)-pgdg main"
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get install postgresql-9.6
```

## Restart Postgres to make 9.6 run on the default port
```
sudo sed -i 's/port = 5432/port = 5433/g' /etc/postgresql/9.5/main/postgresql.conf
sudo sed -i 's/port = 5432/port = 5433/g' /etc/postgresql/9.5/main/postgresql.conf
sudo service postgresql restart
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
cd ~/mod-authtoken && mvn clean install
```
## Clone and build the permissions module
```
cd ~ && git clone --recursive https://github.com/folio-org/mod-permissions.git
cd ~/mod-permissions && mvn clean install
```
## Clone and build the login module
```
cd ~ && git clone --recursive https://github.com/folio-org/mod-login.git
cd ~/mod-login &&  mvn clean install
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

## Clone and build the mod-inventory-storage repo
```
cd ~ && git clone --recursive https://github.com/folio-org/mod-inventory-storage.git
cd ~/mod-inventory-storage && mvn clean install
```

## Clone and build the mod-inventory repo
```
cd ~ && git clone --recursive https://github.com/folio-org/mod-inventory.git
cd ~/mod-inventory && mvn clean install
```

## Clone the folio-test-env repo
```
cd ~ && git clone https://github.com/folio-org/folio-test-env.git
```

## Copy the sample config files
```
cp ~/folio-test-env/testing/test/run_okapi.json.sample ~/folio-test-env/testing/test/run_okapi.json
cp ~/folio-test-env/testing/test/modules.json.sample ~/folio-test-env/testing/test/modules.json
cp ~/folio-test-env/testing/test/load_data.json.sample ~/folio-test-env/testing/test/load_data.json
```

## Install python virtual env, enter into env
```
cd ~/folio-test-env/testing/test && virtualenv -p /usr/bin/python3 pyenv
source pyenv/bin/activate
pip install requests 
```

## Run the script to load Okapi and the modules
```
cd ~/folio-test-env/testing/test/
pyenv/bin/python run_okapi.py --runtime-conf run_okapi.json --module-conf modules.json --db-conf /home/vagrant/folio-test-env/testing/postgres/pg_options.json --load-data-conf load_data.json
```
