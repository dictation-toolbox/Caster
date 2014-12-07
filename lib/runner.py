from subprocess import Popen


def run(args):
    Popen(args, shell=False, stdin=None, stdout=None, stderr=None, close_fds=True)