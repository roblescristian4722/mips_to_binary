"""
    "Comilador" de ensamblador a Lenguaje maquina (tipo MIPS32)
    Cristian Ismael Robles Perez
    Seminario de arquitectura de computadoras
"""

#Funcion para convertir ints decimales a strings en binario
def Bin(dato):
    bin = ""
    dato = int(dato)
    while(dato > 0):
        if(dato % 2 == 0):
            bin += "0"
            dato /= 2
        else:
            bin += "1"
            dato -= 1
            dato /= 2
    bin = bin[::-1]
    return bin
#Fin de Bin()

""" | Clases | """
#Clase para el Op code
class OP: # Clase para Codigo de Operacion (OP)
    def __init__(self, op):
        self.op = op
        return

    #Para saber el tipo de OP Code que se esta usando
    @property 
    def tipo(self): 
        if (self.op == "add" or self.op == "sub" or self.op == "mul" or self.op == "div" or self.op == "and" or self.op == "or" or self.op == "slt" or self.op == "xnor"):
            return "Tipo R"
        elif (self.op == "lw"):
            return "lw"
        elif (self.op == "sw"):
            return "sw"
        elif (self.op == "addi"):
            return "addi"
        elif (self.op == "andi"):
            return "andi"
        elif (self.op == "ori"):
            return "ori"
        else:
            return "xxxxxx"
    
    #Para saber el funtion
    @property
    def func(self):
        if(self.op == "add"):
            return "100000"
        elif(self.op == "sub"):
            return "100010"
        elif(self.op == "mul"):
            return "011001"
        elif(self.op == "div"):
            return "011010"
        elif(self.op == "and"):
            return "100100"
        elif(self.op == "or"):
            return "100101"
        elif(self.op == "xor"):
            return "100110"
        elif(self.op == "slt"):
            return "101010"

    def __repr__(self):
        if (self.op == "add" or self.op == "sub" or self.op == "mul" or self.op == "div" or self.op == "and" or self.op == "or" or self.op == "slt" or self.op == "xnor"):
            return "000000"
        elif (self.op == "lw"):
            return "100110"
        elif (self.op == "sw"):
            return "101011"
        elif (self.op == "addi"):
            return "001000"
        elif (self.op == "andi"):
            return "001101"
        elif (self.op == "ori"):
            return "001100"
        else:
            return "xxxxxx"
#Fin de clase op code

# Clase para registros
class Reg:
    def __init__ (self, reg, tipo):
        self.reg = reg
        self.tipo = tipo
        return
    
    @property
    def valor(self):
        return int(self.reg)
    
    def __repr__(self):
        if(self.tipo == "$"):
            res = str(Bin(self.reg))
            if (5 - len(res) > 0):
                res = "0" * (5 - len(res) ) + res
            return f"{res}"
        elif(self.tipo == "#"):
            res = str(Bin(self.reg))
            if (16 - len(res) > 0):
                res = "0" * (16 - len(res) ) + res
            return f"{res}"
#Fin de clase Reg

# main
datapath = [] #Este valor se guardara en el archivo verilog.txt al final de la ejecucuion
rd = ""

with open("assembly.txt", mode = "r", encoding = "utf-8") as file:
    ins = file.readlines()

cont = 0
for i in ins: #Itera entre cada una de las instrucciones
    if(i[0] == '#' or i[0] == '\n'): # Para comentarios simples al inicio de una linea
        pass
    else: #Si la linea no es un comentario:
        if(i[-1] == '\n'):
            i = i[:-1] #Para quitar el salto de linea
        partes = i.split(",") # Se separa de la siguiente manera: [OP rd, rs, rt]
        
        op = partes[0].split(" ") # Se separa [OP, rd]
        #Se borran los "$" de cada registro
        op[1] = op[1].replace("$", "")
        partes[1] = partes[1].replace(" $", "")

        if ("$" in partes[2]):
            partes[2] = partes[2].replace(" $", "") # rt/offset, en este caso es rt
            rt = Reg(partes[2], "$") # Se asigna rt
            Tipoi = False
            if(rt.valor > 32 or rt.valor < 1):
                raise ValueError("Solo hay 32 registros, el registro ingresado tiene un valor de: ", rt.valor)
        elif("#" in partes[2]):
            partes[2] = partes[2].replace(" #", "") # rt/offset, en este caso es rt
            offset = Reg(partes[2], "#")
            Tipoi = True

        #Se asigna cada registro a una variable para mayor facilidad a la hora de concatenar
        rd = Reg(op[1], "$") # Se asigna a rd el registro que se uso en assembly.txt
        rs = Reg(partes[1], "$") # Se asigna rs
        op = OP(op[0]) #Se asigna el Op code
        
        if (op.tipo == "Tipo R" and Tipoi == False): #Tipo R
            datapath.append(f"{op}{rs}{rt}{rd}00000{op.func}")
        elif(op.tipo == "andi" or op.tipo == "ori" or op.tipo == "addi" or op.tipo == "ls" or op.tipo == "sw"):
            datapath.append(f"{op}{rs}{rd}{offset}")
        cont += 1


cont2 = 0
salida = []
for i in range(cont * 4):
    if (i % 4 == 0):
        salida.append(f"{datapath[cont2][:8]}\n")
    elif (i % 4 == 1):
        salida.append(f"{datapath[cont2][8:16]}\n")
    elif (i % 4 == 2):
        salida.append(f"{datapath[cont2][16:24]}\n")
    elif (i % 4 == 3):
        salida.append(f"{datapath[cont2][24:]}\n")
        cont2 += 1

with open("verilog.txt", mode = "w", encoding = "utf-8") as text:
    for i in salida:
        text.writelines(i)
    
