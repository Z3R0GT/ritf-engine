from typing_extensions import Literal

from ..internal.tool.debug import _insert
from .gen_obj import gen_obj, DEV

class gen_wns:
    def __wns__(self):
        self.square = []
        self.pre_view = ""

    def _create_pre_view(self):
        self._erase_pre_view()

        for line in self.square:
            self.pre_view += f"{line}\n"

    def _erase_pre_view(self):
        self.pre_view = ""

    def get_pre_view(self, is_print=False)->str:
        if not is_print:
            print(self.pre_view)
        return self.pre_view


    def _create_line(self):
        self:gen_obj

        for y in range(self.vec[1]):
            for x in range(self.vec[0]):
                self.pre_view += self.character
            self.square.append(self.pre_view+f"     line {self.abs}: {y}")
            self._erase_pre_view()

    def _create_line_num(self):
        self:gen_obj

        self._erase_pre_view()

        line_all = ""
        line_num = ""
        nro = 0
        try:
            for num in range(self.transform[0]):
                line_all += f"{(num % 10)}"
                if line_all[-1] == "0":
                    line_num += f"{nro}"
                    nro += 1
                else:
                    line_num += " "
        except:
            for num in range(self.vec[0]):
                line_all += f"{(num % 10)}"
                if line_all[-1] == "0":
                    line_num += f"{nro}"
                    nro += 1
                else:
                    line_num += " "
        
        self.square.append(line_all)
        self.square.append(line_num)
        self._create_pre_view()

    def _edit_line(self, coords:list[tuple[int, int]], CHR:str=""):
        self._erase_pre_view()
        self: gen_obj | gen_wns

        for _in in coords:
            len_chr = len(CHR)
            if len_chr >= self.vec[0]:
                #add
                self.square[_in[1]] = _insert(self.square[_in[1]], f"{CHR}", from_=_in[0], to_=self.vec[0])
                #security
                self.square[_in[1]] = _insert(self.square[_in[1]], f"{self.character}", specific_=self.vec[0]-1)

                return True, int(len_chr-self.vec[0])
            else:
                self.square[_in[1]] = _insert(self.square[_in[1]], f"{CHR}", from_=_in[0], to_=_in[0]+len_chr)
                return False, 0 

        self._create_pre_view()


    def _create_square(self, coord:list[int, int], invert:bool=False):
        self:gen_obj | gen_wns

        for x in range(coord[1]):
            if x == 0 or x == (coord[1]-1):
                temp_line = f"{self.character}" * coord[0]
            else:
                temp_line = f"{self.character}"+ " " * (coord[0] - 2) + f"{self.character}"
        
            if DEV[0]:
                self.square.append(temp_line + f"     line {self.abs}: {x}")
            else:
                self.square.append(temp_line)
        self._create_pre_view()

    def _erase_square(self):
        self.square = []


class gen_ui:
    
    def create_text(self,
                    text:str,
                    sector:Literal["CENTER", "UPPER", "LOWER", "CUSTOM"],
                    line:tuple[int, int],
                    chk=True):
        
        def __recursive(ver:list[bool, int]):
            temp = []
            new = ""
            for chr_per in range(len(text)-ver[1], len(text)):
                temp.append(text[chr_per])

            for chr_all in range(len(temp)):
                new += temp[chr_all]

            self.create_text(new, sector, (line[0], line[1]+1), False)

        self:gen_wns
        self._erase_pre_view()

        if sector == "CUSTOM":
            ver = self._edit_line([(line)], text)
            if ver[0]:
                __recursive(ver)
        elif sector == "UPPER":
            if chk:
                line = (1,1)
            ver = self._edit_line([(line)], text)
            if ver[0]:
                __recursive(ver)
        elif sector == "CENTER":
            if chk:
                line = (int(self.vec[0]/2)-5, int(self.vec[1]/2))
            ver = self._edit_line([(line)], text)
            if ver[0]:
                __recursive(ver)
        elif sector == "LOWER":
            if chk:
                line = (1, self.vec[1]-2)
            
        self._create_pre_view()