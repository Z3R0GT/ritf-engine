from engine import *
from time import sleep

ver : str = "a1.1.3.0"
ver_main : str = "1.0"

web ="https://www.youtube.com/watch?v=dQw4w9WgXcQ"

DEV[0] = False
in_ = Button(X=12, Y=12, DEFAULT="BACK")

def proyect_new(arg):
    print_debug("COMING SOON")
    sleep(3)
    in_.execute(0)

def proyect_list(arg):
    print_debug("COMING SOON")
    sleep(3)
    in_.execute(0)

page = Page(X=100, Y=15, CHR="#")
page.create_text("Roses In The Flame's mod engine", "CUSTOM", (3, 3))
page.create_text(f"version {ver}", "CUSTOM", (page.vec[0]-len(ver)-12, 1))

btn = Button(X=5, Y=6, TEXT="Create new proyect", ACTION=proyect_new)
page.add_btn(btn)

btn = Button(X=5, Y=8, TEXT="Load proyect's list", ACTION=proyect_list)
page.add_btn(btn)

btn = Button(X=5, Y=10, TEXT="Exit", DEFAULT="EXIT")
page.add_btn(btn)

btn = Button(X=1, Y=12, TEXT="Website main", ACTION=web, DEFAULT="LINK")
page.add_btn(btn)

btn = Button(X=1, Y=13, TEXT="Website tales", ACTION=web, DEFAULT="LINK")
page.add_btn(btn)

page.add_panel(84, 7, 16, 8)

page.add_panel(64, 7, 16, 8)

btn = Button(X=65, Y=8, TEXT="Open URL", ACTION=web,DEFAULT="LINK")
page.add_btn(btn)

page.start_cast()