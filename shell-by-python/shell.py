import shlex
import signal
import os
import sys
import getpass
import subprocess
import platform
import socket
from func import *

built_in_cmds = {}

def init():
    register_command('cd', cd)
    register_command('getenv', getenv)
    register_command('exit', exit)
    register_command('history', history)

def register_command(name, func):
    built_in_cmds[name] = func

def display_cmd_prompt():
    user = getpass.getuser()
    hostname = socket.gethostname()
    cwd = os.getcwd()
    base_dir = os.path.basename(cwd)
    home_dir = os.path.expanduser('~')
    if base_dir == home_dir:
        base_dir = '~'
    if platform.system() != 'Windows':
        sys.stdout.write('[\033[1;33m%s\033[0;0m@%s \033[1;36m%s] $ '%(user, hostname, base_dir))
    else:
        sys.stdout.write('[%s@%s %s]$ '%(user, hostname, base_dir))
    sys.stdout.flush()

def ignore_signals():
    if platform.system() != "Windows":
        signal.signal(signal.SIGTSTP, signal.SIG_IGN)
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def tokenize(cmd):
    return shlex.split(cmd)

def preprocess(cmd_tokens):
    tokens = []
    for token in cmd_tokens:
        if token.startswith('$'):
            tokens.append(os.getenv(token[1:]))
        else:
            tokens.append(token)
    return tokens

def handler_kill(signum, frame):
    raise OSError('Killed!')

def execute(tokens):
    with open(HISTORY_PATH, 'a') as f:
        f.write(' '.join(tokens) + os.linesep)

    if tokens:  # the list is not empty
        cmd_name = tokens[0]
        cmd_arg = tokens[1:]
        if cmd_name in built_in_cmds:
            return built_in_cmds[cmd_name](cmd_arg)
        # listen to ctrl-c signal
        signal.signal(signal.SIGINT, handler_kill)
        # if the command is not in the command we build, execute it by default system command
        if platform.system() != 'Windows':
            p = subprocess.Popen(tokens)
            # parent proecess to wait for child subprocess to complete
            p.communicate()
        else:
            command = ' '.join(tokens)
            os.system(command)
    return SHELL_STATUS_RUN

def shell_loop():
    status = SHELL_STATUS_RUN
    while status == SHELL_STATUS_RUN:
        display_cmd_prompt()
        ignore_signals()
        try:
            cmd = sys.stdin.readline()
            cmd_tokens = tokenize(cmd)
            cmd_tokens = preprocess(cmd_tokens)
            status = execute(cmd_tokens)
        except:
            _, err, _ = sys.exc_info()
            print(err)


def main():
    init()
    shell_loop()

if __name__ == '__main__':
    main()