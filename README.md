# QKL - Qt Key Logger

Depends on [logkeys](https://github.com/kernc/logkeys).
Requires root to launch logkeys.

Terminating the logkeys process might not be fully reliable.
For that, and other reasons I'd advise against using it on any machine on which
any kinds of secrets are being input (in general maybe don't run a keylogger on a machine you care about).

### Running with function keys

```bash
./main.py
```

### Running without function keys

```bash
./main.py --no-func-keys
```

Close the app with alt+F4.

