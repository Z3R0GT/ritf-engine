
define t = Character("iwi")


#DEFINE ENTORNO PYTHON
init python:
    from os import getcwd, chdir, listdir, path, mkdir

    if "renpy.exe" in list(filter(path.isfile, listdir())): 
        chdir("..")
        chdir("./_internal/tesr/game")
        mkdir("mods")
        a =open(f"{getcwd()}/a.rpy", "w")
        #genera un codigo
        a.write(f"label b:\n    scene hola\n    \"n\" \"hola\"\n    jump a")
        a.close()
    else:
        chdir("./game/mods")
        n = list(filter(path.isfile, listdir()))
        

label a:
    scene hola

    show t sad

    t "miau"

    jump b