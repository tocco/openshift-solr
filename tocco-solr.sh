#!/bin/bash
set -Eeu

# set custom default log level
export SOLR_PARAM_SOLR_LOG_LEVEL=WARN

rm -f /persist/index_data/index/write.lock

# write config file based on environment variables
/usr/local/bin/tocco-solr-config.py /opt/solr/bin/solr.in.sh

# entrypoint script shipped with Solr
exec docker-entrypoint.sh "$@"
