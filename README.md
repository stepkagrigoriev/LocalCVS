# LocalCVS
Студенческий проект, в рамках которого надо реализовать локальную систему контроля версий, наподобие Git, на языке Python
# Примерная структура проекта:
```bash
LocalCVS/
├── __main__.py
├── commands/
│   ├── init.py
│   ├── add.py
│   ├── commit.py
│   ├── log.py
│   └── status.py
├── core/
│   ├── repository.py
│   ├── index.py
│   ├── object_store.py
│   ├── objects.py
│   └── utils.py
└── tests/
