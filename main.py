from Core.commands import init
import sys
def main(*args):
    if len(args) < 2:
        print("Usage: cvs <command> [flags]")
        sys.exit(1)
    command = args[1]
    flags = args[2::]
    if command == 'init':
        if len(flags) == 0:
            print("Usage: cvs init <repo-name>")
            sys.exit(1)
        init(flags[0])


if __name__ == "__main__":
    main()