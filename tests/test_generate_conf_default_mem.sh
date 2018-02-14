#!/bin/bash
set -Eeu

export SOLR_PARAM_SOLR_PORT=1234
export SOLR_PARAM_SOLR_HEAP=1024m
export SOLR_PARAM_ZK_CLIENT_TIMEOUT=300

exec tests/generate_conf.sh tests/sample_config.conf.expected_default_mem
