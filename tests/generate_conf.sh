#!/bin/bash
set -Eeu
trap '[ -n "${temp-}" ] && rm -rf "$temp"' EXIT

temp=$(mktemp -d)
cp tests/sample_config.conf "$temp/config"
./tocco-solr-config.py  "$temp/config"
if ! diff $1 "$temp/config"; then
    echo "ERROR: generated config file doesn't match expected output"
    exit 1
fi
