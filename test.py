a = ["temp_a_0.","temp_a_1.","temp_a_2.","temp_b_0.","temp_b_1.","temp_c_0."]
b = ["temp_a_0."]

def owo(a:str) -> int:
    c=0
    for _in in a:
        c+=1
        if _in == "_":
            break
    return c

for i in a:
    name = i[5:]
    if not i in b:
        c=0
        last_in = b[-1][5:]
        
        num_1 = owo(name)
        num_2 = owo(last_in)
        
        print(name[:num_1-1], last_in[:num_2-1], int(name[num_1:].replace(".", "")), int(last_in[num_2:].replace(".", "")))
        if name[:num_1-1] == last_in[:num_2-1] and int(name[num_1:].replace(".", "")) >= int(last_in[num_2:].replace(".", "")):
            b[-1] = i
        else:
            b.append(i)

"""
for i in a:
    name = i[:1]
    print(i[2:])
    if not name in b:
        if name == b[-1][:1] and int(i[2:]) > int(b[-1][2:]):
            b[-1] = i
        else:
            b.append(i)
"""
        

print(b)