import os
'''
libs = {"numpy","matplotlib","pillow","sklearn","requests",\
        "jieba","beautifulsoup4","wheel","networkx","sympy",\
        "pyinstaller","django","flask","werobot","pyqt5",\
        "pandas","pyopengl","pypdf2","docopt","pygame"}
'''
#libs = {"ascii_art"}
libs = {"feedparser"}
try:
    for lib in libs:
        os.system("pip install " + lib + " -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com")
    print("Successful")
except:
    print("Failed Somehow")
