def _path_() -> str:
    from tkinter import filedialog
    return filedialog.askdirectory()

def _check_proyects() -> list[str]:
    from os import chdir, path, listdir, mkdir, getcwd
    global root
    
    try:
        chdir(root+"/proyects")
    except:
        mkdir(root+"/proyects")
        chdir(root+"/proyects")

    info={}
    for nme in list(filter(path.isdir, listdir())):
        chdir(f"{nme}")
        info[nme] = open(f"{getcwd()}/meta.info", "rt").read().split(",")
        chdir("..")

    return info

