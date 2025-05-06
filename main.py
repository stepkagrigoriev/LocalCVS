from Core.commands import run_command

def main(*args):
    command = args[1]
    flags = args[2::]  
    run_command(command, flags)

if __name__ == "__main__":
    main()