import PyInstaller.__main__
import os

# res = os.popen(cmd="pyinstaller -F -w -i ./resource/icon.ico -p C:\ProgramData\Anaconda3 -n view -specpath dist main.py")
# for line in res.readlines():
#     print(line)


PyInstaller.__main__.run([
    'main.py',  # py入口
    '-F',  # 打包为单个文件
    '-w',  # 运行时不带dos窗口
    '-iresource/128.ico',  # 图标路径
    '-p C:\ProgramData\Anaconda3',  # 解释器路径
    '-n viewer',  # app name
    '-specpath dist'  # spec文件路径
]
)
