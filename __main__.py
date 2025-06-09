import sys
from .Core.commands import run_command


def main(*args):
    if args:
        arguments = list(args)
    else:
        arguments = sys.argv[1::]
    if not arguments or arguments[0] in ['--help', '-h']:
        print("""
        LocalCVS - простая локальная система контроля версий
        Доступные команды:
          init <repo>         — инициализировать новый репозиторий
          add <file> [...]    — добавить файлы в буфер
          commit -m <msg>     — закоммитить изменения с сообщением
          reset <commit>      — откатиться к заданному коммиту (sha)
          log                 — показать историю коммитов
          --help, -h          — показать это сообщение помощи
        """)
        sys.exit(1)
    command = arguments[0]
    flags = list(arguments[1::])
    run_command(command, flags)


if __name__ == '__main__':
    main()
