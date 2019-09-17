import sys
from .constants import *

def history(args):
    with open(HISTORY_PATH, 'r') as f:
        lines = f.readlines()
        if len(args) > 0:
            start = len(lines) - int(args[0])
        else:
            start = 0
        for line_num, line in enumerate(lines):
            if line_num >= start:
                sys.stdout.write('%s %s'%(line_num + 1, line))
        sys.stdout.flush()
    return SHELL_STATUS_RUN