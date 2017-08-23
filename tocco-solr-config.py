#!/usr/bin/python3
import functools
import os
import re
import sys

IS_ENTRY = re.compile('^\s*(?P<name>[^=]*)\s*=')


def extract_config_from_env(env):
    return {k[5:]: v for k, v in env.items() if k.startswith('SOLR_')}


def rewrite_config(old, new, config):
    config = config.copy()
    write_conf = functools.partial(print, file=new, end='')

    # update existing config entries
    for line in old:
        match = IS_ENTRY.search(line)
        if match:
            name = match.group('name')
            if name in config:
                write_conf('{}={}\n'.format(name, config[name]))
                del config[name]
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
