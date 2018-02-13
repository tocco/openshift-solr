#!/bin/bash
set -Eeu

rm -f /persist/index_data/index/write.lock

# set heap memory based on requested memory
if [ -z "${SOLR_PARAM_SOLR_HEAP-}" ] && [ -n "${REQUESTED_MEMORY-}" ]; then
    memory_factor=${MEMORY_FACTOR-0.52}
    export SOLR_PARAM_SOLR_HEAP=$(awk 'BEGIN { printf "%dm", '$REQUESTED_MEMORY'/1048576 * '$memory_factor' }')
fi

# write config file based on environment variables
/usr/local/bin/tocco-solr-config.py /opt/solr/bin/solr.in.sh

# force exit on OOM
# (GC_TUNE, unlike its name suggests, can be used for any Java option)
echo 'GC_TUNE="-XX:+ExitOnOutOfMemoryError${GC_TUNE+ $GC_TUNE}"' >>/opt/solr/bin/solr.in.sh

# entrypoint script shipped with Solr
exec docker-entrypoint.sh "$@"
