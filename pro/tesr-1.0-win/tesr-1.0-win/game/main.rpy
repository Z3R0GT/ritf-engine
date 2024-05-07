init python:
    #Only if a mod exits (this must be in the start of the all chapters)
    def list_to_start():
        #List of currents mods
        lst_mod = open(root+f"/game/mods/archive_lst.txt", "rt").read().split(";")
        del lst_mod[-1]

        for name in lst_mod:
            #run the chapters
            renpy.call_in_new_context(name)

label start:
    #Only need this function
    $ list_to_start()
    #Here end the game
    return 0
