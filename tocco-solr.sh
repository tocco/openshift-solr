#!/bin/sh

rm -f /persist/index_data/index/write.lock

# entrypoint script shipped with Solr
exec docker-entrypoint.sh "$@"
