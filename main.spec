# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\yoann\\PycharmProjects\\FlickrWallpaperChanger'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
a.datas += [('ico\\wallpaper.ico','C:\\Users\\yoann\\PycharmProjects\\FlickrWallpaperChanger\\ico\\wallpaper.ico','DATA')]
a.datas += [('ico\\check.ico','C:\\Users\\yoann\\PycharmProjects\\FlickrWallpaperChanger\\ico\\check.ico','DATA')]
pyz = PYZ(a.pure, a.zipped_data,
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
          console=False , icon='C:\\Users\\yoann\\PycharmProjects\\FlickrWallpaperChanger\\ico\\wallpaper.ico')
