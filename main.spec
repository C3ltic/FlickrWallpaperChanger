# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['src\\python\\main.py'],
             pathex=['C:\\Users\\yoann\\PycharmProjects\\FlickrWallpaperChanger'],
             binaries=[],
             datas=[('src\\resources\\base\\close.png', '.'),
                    ('src\\resources\\base\\icon.png', '.'),
                    ('src\\resources\\base\\minimize.png', '.'),
                    ('src\\resources\\base\\style.css', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure,
          a.zipped_data,
          cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='FlickrWallpaperChanger',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          version='version_info.txt',
          icon='src\\icons\\Icon.ico')
