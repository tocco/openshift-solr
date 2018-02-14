#!/bin/bash
set -Eeu

export MEMORY_LIMIT=$((1024**3))
export MEMORY_FACTOR=0.3

exec tests/generate_conf.sh tests/sample_config.conf.expected_custom_mem_factor
