# -*- mode: python ; coding: utf-8 -*-
from os import getcwd
from os.path import join, dirname

block_cipher = None
block_cipher = pyi_crypto.PyiBlockCipher(key='1sad2*$_+-`!"aop')

# Root directory
ROOT = dirname(getcwd())

INFO = {}
# Load application info
with open(join(ROOT, 'INFO.py')) as f:
    for line in f.readlines():
        if '=' in line:
            info = line.strip().replace(' ', '').split('=')
            INFO[info[0]] = info[1][1:-1]

paths = [
    ROOT,
    join(ROOT, 'SearchDialog'),
    join(ROOT, 'SettingDialog'),
    join(ROOT, 'Strings'),
    join(ROOT, 'Utils')
]

added_files = [
    (join(ROOT, 'Icons'), 'Icons'),
    (join(ROOT, 'CHANGES.md'), '.'),
    (join(ROOT, 'CreateStartup.vbs'), '.'),
    (join(ROOT, 'LICENSE.md'), '.'),
    (join(ROOT, 'README.md'), '.',),
    (join(ROOT, 'README_cn.md'), '.',),
    (join(ROOT, 'Languages', 'map.json'), 'Languages')
]

a = Analysis([join(ROOT, 'Run.py')],
             pathex=paths,
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name=INFO.get('APP_NAME'),
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False,
          icon=join(ROOT, 'Icons', 'app.ico'))

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               upx_exclude=[],
               name='{}_{}'.format(INFO.get('APP_NAME'), INFO.get('VERSION')))
