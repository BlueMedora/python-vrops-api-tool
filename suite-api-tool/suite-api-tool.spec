# -*- mode: python -*-

block_cipher = None


a = Analysis(['suite-api-tool.py'],
             pathex=['/Users/keithstouffer/projects/python-vrops-monitor/suite-api-tool'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='suite-api-tool',
          debug=False,
          strip=False,
          upx=True,
          console=False )
app = BUNDLE(exe,
             name='suite-api-tool.app',
             icon=None,
             bundle_identifier=None,
             info_plist={'NSHighResolutionCapable': 'True'}
             )
