import PyInstaller.__main__

PyInstaller.__main__.run([
    '-D',
    '-w',
    r'.\src\main.py',
    '--icon',
    r'.\img\icon.jpg'
])