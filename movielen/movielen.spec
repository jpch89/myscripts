# -*- mode: python -*-

block_cipher = None


a = Analysis(['movielen.py'],
             pathex=['D:\\code\\myscripts\\movielen'],
             binaries=[],
             datas=[('img\\��Ӱ.png', 'img'), ('ffprobe.exe', '.')],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='movielen',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='img\\��Ӱ.ico')
