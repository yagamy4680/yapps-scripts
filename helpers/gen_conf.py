#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import sys
import os


def clean_string(string):
    xs = string
    xs = xs.strip()
    xs = xs[:-1] if xs[-1] is '"' else xs
    xs = xs[1:] if xs[0] is '"' else xs
    return xs


def load_as_dictionary(file):
    with open(file) as f:
        lines = f.readlines()
    xs = [ l.strip() for l in lines ]
    xs = [ x for x in xs if len(x) is not 0 ]
    xs = [ x for x in xs if not x.startswith('#') ]
    xs = [ x.split(':') for x in xs ]
    xs = [ (x[0], clean_string(x[1])) for x in xs ]
    return dict(xs)


def merge_configuration(defaults, conf_file, used_files):
    if not os.path.exists(conf_file):
        return defaults

    dest = {}
    try:
        conf = load_as_dictionary(conf_file)
        used = False
        for key, value in defaults.items():
            if key in conf:
                dest[key] = conf[key]
                used = True
                print("overwrite %s with %s" % (key, conf_file))
            else:
                dest[key] = defaults[key]
        if used:
            used_files.append(conf_file)
        return dest
    except Exception as e:
        print("failed to load %s" % (conf_file))
        return defaults




def main():
    if len(sys.argv) < 4:
        print("too few arguments")
        sys.exit(1)

    output_script_file = sys.argv[1]
    sys_file = sys.argv[2]
    files = sys.argv[3:]
    if not os.path.exists(sys_file):
        print("%s doesn't exist" % sys_file)
        sys.exit(2)

    sys_config = load_as_dictionary(sys_file)
    used_files = []
    for f in files:
        sys_config = merge_configuration(sys_config, f, used_files)

    with open(output_script_file, 'w') as out:
        prefix = os.environ['PREFIX'] if 'PREFIX' in os.environ else ""
        print("#!/bin/bash\n#", file=out)
        xs = sys_config.items()
        xs = sorted(xs)
        [ print("export %s%s=\"%s\"" % (prefix, key, value), file=out) for key, value in xs ]
        print('', file=out)
        print('if [ "true" == "${CONF_VERBOSE}" ]; then', file=out)
        print("\tINFO \"[conf] $(PURPLE %s) is merged from:\"" % (output_script_file), file=out)
        print("\tINFO \"[conf]\t[v] $(YELLOW %s)\"" % (sys_file), file=out)
        for f in files:
            used = "[o]" if f in used_files else "[x]"
            print("\tINFO \"[conf]\t%s $(YELLOW %s)\"" % (used, f), file=out)
        print("\tINFO \"[conf] environment variables loaded from $(PURPLE %s)\"" % (output_script_file), file=out)
        [ print("\tINFO \"[conf] \t%s%s: $(LIGHT_GREEN %s)\"" % (prefix, key, value), file=out) for key, value in xs ]
        print('fi', file=out)


if __name__ == '__main__':
    main()
