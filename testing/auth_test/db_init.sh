#!/bin/bash

sudo -u postgres bash -c "psql -c \"DROP DATABASE folio_backend;\""
sudo -u postgres bash -c "psql -c \"DROP ROLE diku_mod_login;\""
sudo -u postgres bash -c "psql -c \"DROP ROLE diku_mod_permissions;\""
sudo -u postgres bash -c "psql -c \"DROP ROLE diku_mod_users;\""
sudo -u postgres bash -c "psql -c \"DROP ROLE diku_mod_inventory_storage;\""
sudo -u postgres bash -c "psql -c \"DROP ROLE dbuser;\""
sudo -u postgres bash -c "psql -c \"CREATE USER dbuser WITH SUPERUSER PASSWORD 'qwerty';\""
sudo -u postgres bash -c "psql -c \"CREATE DATABASE folio_backend WITH OWNER=dbuser ENCODING 'UTF8' LC_CTYPE 'en_US.UTF-8' LC_COLLATE 'en_US.UTF-8' TEMPLATE 'template0';\""

