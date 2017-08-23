#!/bin/bash
set -Eeu
trap '[ -n "${temp-}" ] && rm -rf "$temp"' EXIT

export SOLR_SOLR_PORT=1234
export SOLR_SOLR_HEAP=1024m
export SOLR_ZK_CLIENT_TIMEOUT=300

temp=$(mktemp -d)
cp tests/sample_config.conf "$temp/config"
./tocco-solr-config.py  "$temp/config"
if ! diff tests/sample_config.conf.expected "$temp/config"; then
    echo "ERROR: generated config file doesn't match expected output"
    exit 1
fi
