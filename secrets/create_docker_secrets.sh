#!/bin/bash

# Extra script to use external secrets instead of .txt files from this directory.
# Modify 'docker-compose.yml' file first and in secrets section set 'external: true' instead of 'file: ./path'.
# Run it on swarm manager machine and then remove this file.

echo "postgresql://admin:password@db/northwind" | sudo docker secret create db_uri -
echo "admin" | sudo docker secret create login -
echo "password" | sudo docker secret create password -

