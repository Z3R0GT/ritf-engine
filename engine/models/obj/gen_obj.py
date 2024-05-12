from ..internal.tool.debug import print_debug
from ..internal.tool.const import * 

def _set_name(nme:str, nme_dft = ("DEFAULT", "NRO")) -> str:
    if nme != "":
        return nme
    else:
        return f"{nme_dft[0]}_{nme_dft[1]}"

def __check__(msg):
    from re import search 
    if search("[0-9]", msg):
        return int(msg)
    else:
        return msg

class gen_obj:
    def __init__(self,
                 *,
                 X:int,
                 Y:int,
                 CHR:str,
                 ABS:str,
                 ID:int,
                 NMO:str="") -> None:
        
        self.vec = [X, Y]
        self._tmp_vec = [X, Y]

        self.abs = ABS
        self.id = ID

        self.character = CHR
        self.name = _set_name(NMO, (self.abs, self.id))

        self.meta = {
            "name": self.name,
            "vec":  self.vec,
            "abs":  self.abs,
            "id":   self.id,
            "chr":  self.character,
        }

    def _set_meta(self, nme, kwr):
        self.meta[nme] = kwr

    def _edit_meta(self, nme:str|int, tpy:str|int=..., kwr=...):
        if type(tpy) != type(...):
            if type(kwr) == type([]):
                self.meta[nme][tpy].append(kwr)
            elif type(kwr) == type({}):
                self.meta[nme][tpy].append(kwr)
            else:
                self.meta[nme].append(kwr)
        else:
            self._set_meta(nme, kwr)

    def get_meta(self, is_print=True) -> dict:
        if is_print:
            print(self.meta)
        return self.meta
    

class gen_btn:
    def __init__(self, func):
        self.action = func

    def _input_(self, msg:tuple[str]):
        self._in = []

        for text in msg:
            if not text == "":
                self._in.append(input(f"{text}\n>  "))

        self.action(self._in)

    def execute(self, arg):
        self.action(arg)