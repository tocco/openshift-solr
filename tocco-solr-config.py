#!/usr/bin/python3
import functools
import os
import re
import sys

PREFIX = 'SOLR_'
IS_ENTRY = re.compile('^\s*(?P<name>[^=]*)\s*=')


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
            if name:
                write_conf('{}={}\n'.format(name, value))
            else:
                write_conf(line)
        else:
            write_conf(line)

    # write new entries
    for key, value in sorted(config.items()):
        write_conf('{}={}\n'.format(key, value))


def main(path, env):
    config = extract_config_from_env(env)
    orig_path = path + '.orig'
    os.rename(path, orig_path)
    with open(path, "w") as new, open(orig_path) as old:
        rewrite_config(old, new, config)

if __name__ == '__main__':
    main(sys.argv[1], os.environ)
