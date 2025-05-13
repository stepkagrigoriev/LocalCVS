import sys
import sys
from .Core.commands import run_command

def main(*args):
    if args:
        arguments = list(args)
    else:
        arguments = sys.argv[1::]
    if not arguments:
        print('Usage: python -m cvs <command> [flags]')
    command = arguments[0]
    flags = list(arguments[1::])
    run_command(command, flags)

if __name__ == '__main__':
    main()