#!/bin/bash

#######
echo "Starting Okapi"
java -jar -Dloglevel=DEBUG okapi/okapi-core-fat.jar dev &> /tmp/okapi_out.log &
export OKAPI_PID=$!
echo Okapi PID is $OKAPI_PID
sleep 6  #Give Okapi a few seconds to spin up

echo "Creating our tenant"
curl -w '\n' -X POST -D - \
    -H "Content-type: application/json" \
    -d @./tenants/diku.json \
    http://localhost:9130/_/proxy/tenants

### Permissions module
echo "Registering the Permissions module"
curl -w '\n' -X POST -D - \
    -H "Content-type: application/json" \
    -d @./mod-permissions/ModuleDescriptor.json \
    http://localhost:9130/_/proxy/modules

echo "Deploying the Permissions module"
curl -w '\n' -D - -s \
    -X POST \
    -H "Content-type: application/json" \
    -d @./deployment_descriptors/permissions.json \
    http://localhost:9130/_/discovery/modules

echo "Adding the Permissions module to our tenant"
curl -w '\n' -X POST -D - \
    -H "Content-type: application/json" \
    -d @./tenant_associations/permissions.json \
    http://localhost:9130/_/proxy/tenants/diku/modules

### Users module
echo "Registering the Users module"
curl -w '\n' -X POST -D - \
    -H "Content-type: application/json" \
    -d @./mod-users/ModuleDescriptor.json \
    http://localhost:9130/_/proxy/modules

echo "Deploying the Users module"
curl -w '\n' -D - -s \
    -X POST \
    -H "Content-type: application/json" \
    -d @./deployment_descriptors/mod-users.json \
    http://localhost:9130/_/discovery/modules

echo "Adding the Users module to our tenant"
curl -w '\n' -X POST -D - \
    -H "Content-type: application/json" \
    -d @./tenant_associations/mod-users.json \
    http://localhost:9130/_/proxy/tenants/diku/modules

### Login module
echo "Registering the login module"
curl -w '\n' -X POST -D - \
    -H "Content-type: application/json" \
    -d @./mod-login/ModuleDescriptor.json \
    http://localhost:9130/_/proxy/modules

echo "Deploying the login module"
curl -w '\n' -D - -s \
    -X POST \
    -H "Content-type: application/json" \
    -d @./deployment_descriptors/login.json \
    http://localhost:9130/_/discovery/modules

echo "Adding the login module to our tenant"
curl -w '\n' -X POST -D - \
    -H "Content-type: application/json" \
    -d @./tenant_associations/login.json \
    http://localhost:9130/_/proxy/tenants/diku/modules

### authtoken module
echo "Registering the authtoken module"
curl -w '\n' -X POST -D - \
    -H "Content-type: application/json" \
    -d @./mod-authtoken/ModuleDescriptor.json \
    http://localhost:9130/_/proxy/modules

echo "Deploying the authtoken module"
curl -w '\n' -D - -s \
    -X POST \
    -H "Content-type: application/json" \
    -d @./deployment_descriptors/authtoken.json \
    http://localhost:9130/_/discovery/modules

echo "Adding the authtoken module to our tenant"
curl -w '\n' -X POST -D - \
    -H "Content-type: application/json" \
    -d @./tenant_associations/authtoken.json \
    http://localhost:9130/_/proxy/tenants/diku/modules

echo "Okapi process id is $OKAPI_PID"

