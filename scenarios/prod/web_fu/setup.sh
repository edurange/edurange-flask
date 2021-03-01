#!/bin/bash
set -euxo pipefail

# TODO: test services are reachable.

echo "Starting apache..."
service apache2 start && echo "Apache started!"

echo "Starting mysql..."
service mysql start && echo "MySQL started!"
