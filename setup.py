import sys
import os
from cx_Freeze import setup,Executable

files = ['view','src']
exe = Executable(script="run.py", base='Win32GUI',icon=os.getcwd() + '\\iconLogo.ico')

setup(
    name="FBaixar Videos",
    version='1.0',
    description="",
    author='Luiz Eduardo Cassimiro',
    options={'builder_exe':{'include_files': files,'includes': ['pytube']}},
    executables=[exe]

)