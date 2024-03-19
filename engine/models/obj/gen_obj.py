from ..internal.tool.debug import print_debug
from ..internal.tool.const import *

import re
                              # ABS     ID
def _set_name(nme, nme_dft = ("DEFAULT", "NRO")):
    if type(nme) == type(""):
        if nme != "":
            return nme
        else:
            return f"{nme_dft[0]}_{nme_dft[1]}"

def __check__(msg):
    if re.search("[0-9]", msg):
        return int(msg)
    else:
        return msg

class gen_obj:
    def __init__(self, 
                 X,
                 Y,
                 CHR,
                 ABS,
                 ID, 
                 NMO= "") -> None:
        
        self.vec = [X,Y]
        self._temp_vec = [X, Y]
        
        self.abs = ABS
        self.id = ID

        self.character = CHR
        self.name = _set_name(NMO, (self.abs, self.id))
        
        self.meta = {
            "name": self.name,
            "vec": self.vec,
            "abs": self.abs,
            "id": self.id,
            "chr": self.character,
        }
    
    def __transform__(self, size_x, size_y):
        
        self.transform = (size_x, size_y)
        self._set_meta("transform", self.transform)
    
    def __map__(self, map):
        self.map = map
        self._set_meta("map", (self.map.id, self.map.name))

    def _set_meta(self, nme, arg):
        self.meta[nme] = arg
     
    def _edit_meta(self, nme_1, nme_2, arg):
        
        if type(nme_2) != type(...):
            if type(arg) == type([]):     
                    self.meta[nme_1][nme_2].append(arg)
            elif type(arg) == type({}):
                    self.meta[nme_1][nme_2] = arg
            else:
                self.meta[nme_1].append(arg)
        else:
            self._set_meta(nme_1, arg)
    
    def get_meta(self, is_print=True):
         if is_print:
             print(self.meta)
         else:
             return self.meta 


class gen_btn:
    
    def __start__(self, *msg):
        print_debug(msg)
        
    def __default__(self):
        CUR[3].append(self.__start__)

    def __action__(self, what):
        ID = -1
        for func in CUR[3]:
            #YA EXISTE
            if func == what:
                break
            #NO EXISTE
            else:
                CUR[3].append(what)
                ID += 1
                break
        self.action = (ID, what)

    def __link__(self):
        if not len(self._in) > 0:
            self.action[1]()
        else:
            self.action[1](self._in[0: len(self._in)])
            
        self._in = []

    def _input_(self, msg:tuple):
        self._in =[]

        for text in msg:
            self._in.append(input(f"{text}\n>  "))
        
        self.__link__()
        
    def execute(self, *arg):
        self.action[1](arg)
           
        
