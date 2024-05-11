#from engine import *
from dev.engine import *

DEV[0] = False

def test(arg):
    print(arg[0])

def tst(arg):
    n, u, = arg
    print(n, u)

page = Page(X=20, Y=10, CHR="#")
page.create_text("Test menu", "UPPER")

btn1 = Button(X=1, Y=2, TEXT="test", ACTION=test)
btn1.caster(("hola prro", ""))
page.add_btn(btn1)

btn2 = Button(X=1, Y=3, TEXT="tst", ACTION=tst)
btn2.caster(("imprimir 1", "imprimir 2"))
page.add_btn(btn2)

btn3 = Button(X=1, Y=4, DEFAULT="EXIT")
page.add_btn(btn3)

page.start_cast()