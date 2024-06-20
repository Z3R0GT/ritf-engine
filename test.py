import sys
from engine.config.gen_arch1 import *
from os import getcwd, system
from time import sleep

global_config(cwd=getcwd()+"/proyects/asb")
label_tst = Label(1, "owo", [1], 1)

def a(n:str, m=True):
    print(label_tst.meta[n])
    if m:
        input()

def b(n:int):
    n -= 1
    print(label_tst._if_obj[n])
    print(label_tst._if_con)
    print("CONDTIONS")
    print(label_tst._if_obj[n].meta["condition"])
        
    print("DIALOG")
    c=-1
    for i in range(len(label_tst._if_obj[n].meta["dialog"])):
        print(i)
        for m in label_tst._if_obj[n].meta["dialog"][i]:
            c+=1
            print(c, m)

    

print("ADDING CHARACTER")
label_tst.add_character("pedro")
a("character")

print("EDDTING THAT CHARACTER")
label_tst.edit_character(1, "name", "josue")
a("character")
label_tst.edit_character(1, "text", 50)
a("character")

print("DELETING THE CHARACTER")
label_tst.del_character(1)
a("character")

system("cls")
print("ADDDING CHAR + SAY")
label_tst.add_character("Snowy")
a("character")

label_tst.add_say(1, "normal", "Hi!, I'm snowy")
a("dialog")

print("CHAR X2 + SAY")
label_tst.add_character("Orpheus Nulla")
a("character")

label_tst.add_say(2, "normal", "What?, where am I?")
label_tst.add_say(2, "normal", "oh, Hi Snowy!, hru?")
a("dialog")

print("EDDITING SAY")
label_tst.edit_say(1, "normal", "message", "Hello!, I'm snowy")
a("dialog")

print("DELETING SAY")
label_tst.del_say(3, "normal")
a("dialog")

label_tst.add_say(2, "normal", "oh, Hi Snowy!, hru?")

system("cls")
print("ADDING 'IF' STATEMENT (if - equal mode)")
label_tst.add_condition("snowy.happy", "snowy.happy", "equal", "a_case")
a("_if_", False)
b(1)

a("dialog")

print("ADDING X3 SAY TO THIS IF")
line = label_tst.add_say(1, "if", "Very exited to see if this works!", 1, 1)
print(line)
a("_if_", False)
b(1)

a("dialog")
line = label_tst.add_say(2, "if", "Glad to hear tha... wait, what thing?", 1, 1)
print(line)
a("_if_", False)
b(1)

a("dialog")
line = label_tst.add_say(1, "if", "We're inside of a machine, my friend...", 1, 1)
print(line)
a("_if_", False)
b(1)

a("dialog")

system("cls")
print("ADDING ANOTHER IF (elif - not case)")
line = label_tst.edit_condition(1,"snowy.bad", "snowy.bad","ADD", "not" )
print(line)
a("_if_", False)
b(1)

a("dialog")

print("ADDING X3 SAY TO THIS IF")
line = label_tst.add_say(1, "if", "bad my friend... I feel weird thing reciently, I think that we're inside of a machina", 1, 2)
print(line)
a("_if_", False)
b(1)

a("dialog")
line = label_tst.add_say(2, "if", "oh, that's sounds bad but... wait, wym with 'machine'?", 1, 2)
print(line)
a("_if_", False)
b(1)

a("dialog")
line = label_tst.add_say(1, "if", "We're inside of a machine, my friend...", 1, 2)
print(line)
a("_if_", False)
b(1)

a("dialog")

print("EDDTING FIRST AND SECOND CONDTION (if = 1 or 0)")
line = label_tst.edit_say(1, "if", "message", "pretty excited to see if this works!", 1, 1)
print(line)
a("_if_", False)
b(1)

a("dialog")

line = label_tst.edit_say(1, "if", "message", "Pretty bad, I think we are inside a machine", 1, 2)
print(line)
a("_if_", False)
b(1)

a("dialog")

print("DELETING LAST DIALOG ON FIRST AND SECOND CONDTION (if = 1 or 0)")
label_tst.del_say(3, "if", 1, 1)
a("_if_", False)
b(1)

a("dialog")

label_tst.del_say(3, "if", 1, 2)
a("_if_", False)
b(1)

a("dialog")

line = label_tst.add_say(1, "if", "We're inside of a machine, my friend...", 1, 1)
line = label_tst.add_say(1, "if", "We're inside of a machine, my friend...", 1, 2)

print("EDDTING THE FIRST CONTIDITION (if = 1 or 0 - equal mode)")
label_tst.edit_condition(1, "HAPPY", "HAPPY", "EDIT", "equal", 1)
a("_if_", False)
b(1)

a("dialog")

print("MOVING FIRST TO SECOND CONDITION (if = 1 or 0)")
label_tst.edit_condition(1, ..., ..., "MOVE", ..., 1, 2)
a("_if_", False)
b(1)

a("dialog")

print("DELETING SECOND CONDITION (if = 1 or 0)")
label_tst.edit_condition(1, ..., ..., "DEL", ..., 2)
a("_if_", False)
b(1)

a("dialog")

print("DELETING THE ENTIRE IF LATER OF PUT A 'say', statement")
label_tst.add_say(2, "normal", "That's crazy men!")
a("dialog")

label_tst.del_condition(1)
a("dialog")