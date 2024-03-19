import logging, sys
from os import system

from .const import CUR, DEFAULT

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def _chk_window(x=..., y=..., _specific=False):
        if not _specific:  
            if DEFAULT[1][2] or DEFAULT[1][1]: # IS IN MENU  
                x_cols = CUR[0][0].vec[0]+5
                y_lins = CUR[0][0].vec[1]+6
            else: #IS PLAYING MAP
                x_cols = CUR[1][DEFAULT[1][4]].transform[0]+5
                y_lins = CUR[1][DEFAULT[1][4]].transform[1]+6
        else:
            x_cols = x+30
            y_lins = y+20

        from os import system  
        system(f'mode con: cols={x_cols} lines={y_lins}')

def erase_screen():
    system("cls")

def print_debug(*msg):
    logging.debug(msg)

def _insert(old_, new_, from_=..., to_=..., specific_=...) -> str:
    temp = []
    new = ""
    cont = 0

    #print(f"Viejo: {len(old_)}", f"Nuevo: {len(new_)}",f"Desde: {from_}",f"Hasta: {to_}", f"Especifico: {specific_}" )

    for i in range(len(old_)):
        temp.append(old_[i])

    if to_ is ... and from_ is not ...:
        to_ = len(new_) + from_

    for mw in range(len(temp)):
        if specific_ is not ...:
            if mw > 0 and mw == specific_:
                temp[mw] = new_
        elif mw in range(from_, to_):
            temp[mw] = new_[cont]
            cont += 1

    for i in range(len(temp)):
         new += temp[i]

    return new


#LO DEJO POR XD

import ctypes

FW_DONTCARE       = 0
LF_FACESIZE       = 32
STD_OUTPUT_HANDLE = -11

class _COORD(ctypes.Structure):
    _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

class _CONSOLE_FONT_INFOEX(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_ulong),
                ("nFont", ctypes.c_ulong),
                ("dwFontSize", _COORD),
                ("FontFamily", ctypes.c_uint),
                ("FontWeight", ctypes.c_uint),
                ("FaceName", ctypes.c_wchar * LF_FACESIZE)]


def set_console_font(font_name="Lucida Console", size_x=11, size_y=0, acent=400):
    font = _CONSOLE_FONT_INFOEX()
    font.cbSize = ctypes.sizeof(_CONSOLE_FONT_INFOEX)
    font.nFont = 0
    font.dwFontSize.X = size_x #16
    font.dwFontSize.Y = size_y #0
    font.FontFamily = FW_DONTCARE
    font.FontWeight = acent
    font.FaceName = font_name #Consolas

    handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    ctypes.windll.kernel32.SetCurrentConsoleFontEx(
            handle, ctypes.c_long(False), ctypes.pointer(font))
