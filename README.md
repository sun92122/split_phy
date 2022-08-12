# split_phy

~~就抽籤而已那麼麻煩~~

## python version

`3.9.7`

## Install dependencies

```shell
pip install -r requirements.txt
```

If you have pygame and PyQt5 maybe you can skip this step.

## Convert pyQt UI to python

```shell
pyuic5 -x UI.ui -o UI.py
```

Some code may need to be corrected after using this command.

## Run code

```shell
python .\src\main.py
```

## packaging code

### Requires python3.7 or above

### install installer package

```shell
pip install pyinstaller
```

### packaging

```shell
python .\package.py
```

By default, the executable file will be stored in dist folder.
