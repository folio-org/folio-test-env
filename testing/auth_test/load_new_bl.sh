#!/bin/bash
### users-bl module
echo "Registering the Users-BL module"
curl -w '\n' -X POST -D - \
    -H "Content-type: application/json" \
    -d @./mod-users-bl/target/ModuleDescriptor.json \
    http://localhost:9130/_/proxy/modules

echo "Deploying the Users-BL module"
curl -w '\n' -D - -s \
    -X POST \
    -H "Content-type: application/json" \
    -d @./deployment_descriptors/users-bl.json \
    http://localhost:9130/_/discovery/modules

echo "Adding the Users-BL module to our tenant"
curl -w '\n' -X POST -D - \
    -H "Content-type: application/json" \
    -d @./tenant_associations/users-bl.json \
    http://localhost:9130/_/proxy/tenants/diku/modules


