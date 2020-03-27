#!/usr/bin/python3

import os
import sys

if len(sys.argv) != 2:
    sys.exit("ERROR: container requires 1 parameter: A foundries.io API token")


if os.fork() == 0:
    # child - check keys forever
    args = ["/sync-authorized-keys", sys.argv[1]]
    factory = os.environ.get("FACTORY")
    if factory:
        args.append(factory)
    os.execv(args[0], args)

args = ["/usr/local/sbin/sshd", "-D", "-p", "2222", "-E", "/dev/stderr"]
os.execv(args[0], args)
