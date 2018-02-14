#!/usr/bin/python3
import functools
import os
import re
import sys

PREFIX = 'SOLR_PARAM_'
IS_ENTRY = re.compile('^\s*(?P<name>[^=]*)\s*=')
DEFAULT_MEMORY_FACTOR = 0.52


def extract_config_from_env(env):
    return {k[len(PREFIX):]: v for k, v in env.items() if k.startswith(PREFIX)}


def rewrite_config(old, new, config):
    config = config.copy()
    write_conf = functools.partial(print, file=new, end='')

    # update existing config entries
    for line in old:
        match = IS_ENTRY.search(line)
        if match:
            name = match.group('name')
            value = config.pop(name, None)
            if value:
                write_conf('{}={}\n'.format(name, value))
            else:
                write_conf(line)
        else:
            write_conf(line)

    print(file=new)
    print('### GENERATED ###', file=new)

    # write new entries
    for key, value in sorted(config.items()):
        write_conf('{}={}\n'.format(key, value))


def add_static_options(file):
    """
        Additional configurations that are included unconditionally
    """
    # force exit on OOM
    print('GC_TUNE="-XX:+ExitOnOutOfMemoryError${GC_TUNE+ $GC_TUNE}"', file=file)

    # use ParallelGC
    print('GC_TUNE="-XX:+UseParallelGC -Xms64m -XX:MinHeapFreeRatio=15 -XX:MaxHeapFreeRatio=30${GC_TUNE+ $GC_TUNE}"', file=file)


def max_heap_from_limit(config):
    """
        Set memory limit based on OpenShift memory limit
    """
    memory_factor = float(config.get('MEMORY_FACTOR', DEFAULT_MEMORY_FACTOR))
    memory_limit = float(config['MEMORY_LIMIT'])
    return '{:.0f}m'.format(memory_limit / 1024**2 * memory_factor)


def main(path, env):
    config = extract_config_from_env(env)
    if 'MEMORY_LIMIT' in env and 'SOLR_PARAM_SOLR_HEAP' not in config:
        config['SOLR_PARAM_SOLR_HEAP'] = max_heap_from_limit(env)
    orig_path = path + '.orig'
    os.rename(path, orig_path)
    with open(path, "w") as new, open(orig_path) as old:
        rewrite_config(old, new, config)
        add_static_options(new)

if __name__ == '__main__':
    main(sys.argv[1], os.environ)
