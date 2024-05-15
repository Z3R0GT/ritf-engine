from .admin_dir import *

from os import getcwd, chdir, listdir, mkdir, path, remove

cwd = getcwd()

def _check_save():
    if getcwd() == f"{cwd}/saves":
        return True
    else:
        for pat in list(filter(path.isdir, listdir())):
            if pat == "saves":
                chdir(r"./saves")
                return True
        print("CURRENT: " + getcwd())
        chdir("..")
        _check_save()
                
def refresh_saves(CUR) -> list:
    CUR[4] = list(filter(path.isfile, listdir()))
    return CUR[4]

def start_test():
    _check_save()
    if getcwd()[-5:-1] == "save":
        n = save_node({"Test": True}, "test")

        try:
            if load_save(n)["Test"]:
                remove(n)
                print("PASSED")
                return True
        except KeyError:
            print("NOT CREATE \nTRY AGAIN...")
            start_test()
    else:
        print("NOT FOUND")
        _check_save()
        print("TRY AGAIN...")
        start_test()
    
        

def _path():
    from tkinter import filedialog
    return filedialog.askdirectory()    

def _paths() -> str:
    file = open(f"{getcwd()}/path.json", "w")
    try:
        json.dump(_path(), file, indent=1)
    except TypeError:
        print_debug("Ellipsis date found.")
    return file

def check_paths_all():
    #THIS FOR THE GAME
    from time import sleep
    print("select the path of the game")
    #sleep(3)

    #NOT NECCESARY
    while True:
        absolute= _path()
        match absolute[-4:]:
            case "mods":
                break
            case "ritf":
                absolute += "/mods"
                break
            case _:
                print("We need the path of the game")
                #sleep(5)

    chdir(absolute)
    cur_mods = list(filter(path.isdir, listdir()))

    

    """
    if "path.json" in list(filter(path.isfile, listdir())):
        n = load_save(f"{getcwd()}/path.json").split(",")
    else:
        n = _paths().split(",") 
    """
