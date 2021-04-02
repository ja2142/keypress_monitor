# QKL - Qt Key Logger

## Running with function keys

```bash
# firstly create fifo
mkfifo keylogger_pipe
# start keylogging
./logkeys_with_func
# start gui
./main.py
```

## Running without function keys

```bash
# firstly create fifo
mkfifo keylogger_pipe
# start keylogging
./logkeys
# start gui
./main.py --no-func-keys
```

