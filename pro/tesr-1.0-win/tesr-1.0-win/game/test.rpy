
define t = Character("iwi")


#DEFINE ENTORNO PYTHON
init python:
    lst_run = []

    def abcd():
        return "1"

    from os import listdir, path

    #Is it in editor mode?
    if "renpy.exe" in list(filter(path.isfile, listdir())):
        pass
    else:
        from os import getcwd, chdir, mkdir
        
        root = getcwd()

        chdir("./mods")
        cur_mods = list(filter(path.isdir, listdir()))

        cur_file = []

        for name in cur_mods:
            chdir(f"{name}")
            with open(f"{getcwd()}/base.info", "rt") as file:
                    for i in file.read().split(";"):
                        comm = list(i.split(","))

                        line = list(comm[1].replace("-", ",").replace("[","").replace("]", "").split(","))    
                        lb = list(comm[2].replace("-", ",").replace("[","").replace("]", "").split(","))
                    




"""
        if len(cur_mods) == 0:
            pass #VARIABLE FOR VERIFICATION
        else:
            for name in cur_mods:
                chdir(f"{name}")
                file =  open(f"{getcwd()}/base.info", "rt")
                info = file.read().split(";")

                for i in info:
                    comm = list(i.split(",")) #commands
                    chdir(root+"/game")
                    ftc = open(root+f"/game/{comm[0]}","rt") #file_to_copy   
                    ftc_inf = ftc.readlines()

                    #Convert all files
                    line = list(comm[1].replace("-", ",").replace("[","").replace("]", "").split(","))
                    
                    lb = list(comm[2].replace("-", ",").replace("[","").replace("]", "").split(","))

                    #if ftc_inf[int(com[0])-1].replace("\n", "").replace("\", ") ==com[1]: # DO YOU HAVE THE REFERENCE COMMAND?
                    for k in lb:
                        ftc_inf[int(line[0])] = f"jump {k}"

                    with open(root+f"/mods/{name}/{comm[0][:-4]}_modder.rpy", "w") as ftp:  #file_to_paste
                        for m in ftc_inf:
                            ftp.write(m)
                    
                    ftp.close()

                    chdir(root+f"/mods/{name}")

label a:
    scene hola

    show t sad

    t "miau"
    
    #DECLARACIÓN DE VARIABLE DE PYTHON-RENPY
    $ ans = abcd()

    #CODIGO PARA ENLAZAR PYTHON CON RENPY
    "h" "[ans]"
    



