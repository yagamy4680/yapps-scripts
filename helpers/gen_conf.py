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


def main():
    if len(sys.argv) < 4:
        print("too few arguments")
        sys.exit(1)

    sys_file = sys.argv[1]
    profile_file = sys.argv[2]
    output_script_file = sys.argv[3]

    if not os.path.exists(sys_file):
        print("%s doesn't exist" % sys_file)
        sys.exit(2)

    sys_config = load_as_dictionary(sys_file)
    profile_config = {}
    try:
        profile_config = load_as_dictionary(profile_file) if os.path.exists(profile_file) else profile_config
    except Exception as e:
        print("failed to load %s" % (profile_file))

    prefix = os.environ['PREFIX'] if 'PREFIX' in os.environ else ""

    for key, value in sys_config.items():
        if key in profile_config:
            sys_config[key] = profile_config[key]

    with open(output_script_file, 'w') as out:
        print("#!/bin/bash\n#", file=out)
        xs = sys_config.items()
        xs = sorted(xs)
        [ print("export %s%s=\"%s\"" % (prefix, key, value), file=out) for key, value in xs ]
        print("", file=out)
        print("INFO \"[conf] source0: $(YELLOW %s)\"" % (sys_file), file=out)
        print("INFO \"[conf] source1: $(YELLOW %s)\"" % (profile_file), file=out)
        print("INFO \"[conf] environment variables loaded from $(PURPLE %s)\"" % (output_script_file), file=out)
        [ print("INFO \"[conf] \t%s%s: $(LIGHT_GREEN %s)\"" % (prefix, key, value), file=out) for key, value in xs ]


if __name__ == '__main__':
    main()
