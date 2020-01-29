# -*- mode: python ; coding: utf-8 -*-
from os import getcwd
from os.path import join, dirname

block_cipher = None
block_cipher = pyi_crypto.PyiBlockCipher(key='1sad2*$_+-`!"aop')

# Root directory
ROOT = dirname(getcwd())

INFO = {}
# Load application info
with open(join(ROOT, 'info.py')) as f:
    for line in f.readlines():
        if '=' in line:
            info = line.strip().replace(' ', '').split('=')
            INFO[info[0]] = info[1][1:-1]

paths = [ROOT,
         join(ROOT, 'SearchDialog'),
         join(ROOT, 'SettingDialog'),
         join(ROOT, 'Strings'),
         join(ROOT, 'Utils')]

added_files = [(join(ROOT, 'Icons'), 'Icons'),
               (join(ROOT, 'CHANGES.md'), '.'),
               (join(ROOT, 'CreateStartup.vbs'), '.'),
               (join(ROOT, 'LICENSE.md'), '.'),
               (join(ROOT, 'README.md'), '.')]

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
          upx=True,
          console=False,
          icon=join(ROOT, 'Icons', 'XSearch.ico'))

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='{}_{}'.format(INFO.get('APP_NAME'), INFO.get('VERSION')))
