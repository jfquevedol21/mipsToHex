from tkinter import *

def retornaLineas(archivo):
    codigoMips=open(archivo,'r')
    code=codigoMips.read()
    contadorCaracteres=0
    lineas=[]
    finalesDeLinea=[]
    for x in code:
        if x== "\n":
            finalesDeLinea.append(contadorCaracteres)
        contadorCaracteres=contadorCaracteres+1
        if contadorCaracteres == len(code):
            finalesDeLinea.append(len(code))

    
    ayuda=0
    for x in range(len(finalesDeLinea)):
        if ayuda==0:
            lineas.append(code[:finalesDeLinea[x]])
            ayuda=1
        else:
            lineas.append(code[finalesDeLinea[x-1]+1:finalesDeLinea[x]])
    return lineas

def lineaEnHex(lineaa):
    lineas=lineaa
    tipoI=["beq","bne","blez","bgtz","addi","addiu","slti","sltiu",
            "andi","ori","xori","lui","lb","lh","lw","lbu","lhu","sb",
            "sh","sw"]
    opcodeI=[4,5,6,7,8,9,10,11,12,13,14,15,32,33,34,36,37,40,41,43]

    tipoR=["sll","srl","sra","sllv","srlv","srav","jr","jalr","syscall","break",
            "mfhi","mthi","mflo","mtlo","mult","multu","div","divu","add","addu",
            "sub","subu","and","or","xor","nor","slt","sltu"]

    tipoJ=["j","jal"]

    opcodeJ=[2,3]

    functR=[0,2,3,4,6,7,8,9,12,13,16,17,18,19,24,25,26,27,32,33,34
            ,35,36,37,38,39,42,43]

    setDeRegistros=["$0","$at","$v0","$v1","$a0","$a1","$a2","$a3","$t0","$t1"
                    ,"$t2","$t3","$t4","$t5","$t6","$t7","$s0","$s1","$s2"
                    ,"$s3","$s4","$s5","$s6","$s7","$t8","$t9","$k0","$k1"
                    ,"$gp","$sp","$fp","$ra"]

    comando="nada"
    comandoStop=0
    param1="nada"

    param2="nada"
    param3="nada"

    contador=0
    for x in lineas:
        if x==" ":
            comando=lineas[:contador]
            comandoStop=contador
            break
        contador=contador+1

    param1Stop=comandoStop

    for x in lineas[comandoStop:]:
        if param1Stop == len(lineas)-1:
            param1=lineas[comandoStop+1:param1Stop+1]
        if x==",":
            param1=lineas[comandoStop+1:param1Stop]
            break
        param1Stop=param1Stop+1

    param2Stop=param1Stop+1
    flagTipoIParentesis=0
    for x in lineas[param1Stop+1:]:
        if param2Stop == len(lineas)-1:
            param2=lineas[param1Stop+2:param2Stop+1]
        if x==",":
            param2=lineas[param1Stop+2:param2Stop]
            break
        if x=="(":
            param2=lineas[param1Stop+2:param2Stop]
            flagTipoIParentesis=1
            break
        param2Stop=param2Stop+1

    if flagTipoIParentesis==0:
        param3=lineas[param2Stop+2:len(lineas)]
    if flagTipoIParentesis==1:
        param3=lineas[param2Stop+1:len(lineas)-1]

    cosas=[comando, param1, param2, param3]

    equivalenteDec=[]

    tipo=None
    esTipoJ=0
    for x in tipoI:
        if comando==x:
            tipo=0
            if comando == "blez" or comando== "bgtz" or comando == "lui":
                equivalenteDec.append(opcodeI[tipoI.index(comando)])
                equivalenteDec.append(setDeRegistros.index(param1))
                equivalenteDec.append(0)
                equivalenteDec.append(param2)
                break
            elif comando == "lb" or comando == "lh" or comando == "lw" or comando == "lbu" or comando == "lhu" or comando == "sb":
                equivalenteDec.append(opcodeI[tipoI.index(comando)])
                equivalenteDec.append(setDeRegistros.index(param3))
                equivalenteDec.append(setDeRegistros.index(param1))
                equivalenteDec.append(param2)
                break
            elif comando == "beq" or comando == "bne":
                equivalenteDec.append(opcodeI[tipoI.index(comando)])
                equivalenteDec.append(setDeRegistros.index(param1))
                equivalenteDec.append(setDeRegistros.index(param2))
                equivalenteDec.append(param3)
                break
            else:
                equivalenteDec.append(opcodeI[tipoI.index(comando)])
                equivalenteDec.append(setDeRegistros.index(param2))
                equivalenteDec.append(setDeRegistros.index(param1))
                equivalenteDec.append(param3)
                break

    for x in tipoR:
        if comando==x:
            tipo=1
            if comando == "sll" or comando == "srl" or comando == "sra":
                equivalenteDec.append(0) #(op) opcode de todos los tipo R es 0
                equivalenteDec.append(0) #(rs) estas instrucciones tipo R no tienen rs
                equivalenteDec.append(setDeRegistros.index(param2)) #(rt)
                equivalenteDec.append(setDeRegistros.index(param1)) #(rd)
                equivalenteDec.append(param3) #(shamt)
                equivalenteDec.append(functR[tipoR.index(comando)])
                break
            elif comando == "sllv" or comando == "srlv" or comando == "srav":
                equivalenteDec.append(0) #(op) opcode de todos los tipo R es 0
                equivalenteDec.append(setDeRegistros.index(param3)) #(rs)
                equivalenteDec.append(setDeRegistros.index(param2)) #(rt)
                equivalenteDec.append(setDeRegistros.index(param1)) #(rd)
                equivalenteDec.append(0) #(shamt) no tiene
                equivalenteDec.append(functR[tipoR.index(comando)]) #(funct)
                break
            elif comando == "jr" or comando == "jalr":
                tipoJ=1
                equivalenteDec.append(0) # opcode de todos los tipo R es 0
                equivalenteDec.append(setDeRegistros.index(param1)) #(rs)
                equivalenteDec.append(0) # (rt) no tiene
                equivalenteDec.append(0) # (rd) no tiene
                equivalenteDec.append(0) # (shamt) no tiene
                equivalenteDec.append(functR[tipoR.index(comando)]) #(funct)
                break
            elif comando == "break" or comando == "syscall":
                equivalenteDec.append(0) #opcode es 0
                equivalenteDec.append(0) #(rs) no tiene
                equivalenteDec.append(0) #(rt) no tiene
                equivalenteDec.append(0) #(rd) no tiene
                equivalenteDec.append(0) #(shamt) no tiene
                equivalenteDec.append(functR[tipoR.index(comando)]) #(funct)
                break
            elif comando == "mfhi" or comando == "mflo":
                equivalenteDec.append(0) #(op) es 0
                equivalenteDec.append(0) #(rs) no tiene
                equivalenteDec.append(0) #(rt) no tiene
                equivalenteDec.append(setDeRegistros.index(param1)) #(rd)
                equivalenteDec.append(0) #(shamt) no tiene
                equivalenteDec.append(functR[tipoR.index(comando)]) #(funct)
                break
            elif comando == "mthi" or comando == "mtlo":
                equivalenteDec.append(0) #(op) es 0
                equivalenteDec.append(setDeRegistros.index(param1)) #(rs) no tiene
                equivalenteDec.append(0) #(rt) no tiene
                equivalenteDec.append(0) #(rd)
                equivalenteDec.append(0) #(shamt) no tiene
                equivalenteDec.append(functR[tipoR.index(comando)]) #(funct)
                break
            elif comando == "mult" or comando == "multu" or comando == "div" or comando =="divu":
                equivalenteDec.append(0) # (op) es 0
                equivalenteDec.append(setDeRegistros.index(param1)) #(rs)
                equivalenteDec.append(setDeRegistros.index(param2)) #(rt)
                equivalenteDec.append(0) #(rd)
                equivalenteDec.append(0) #(shamt)
                equivalenteDec.append(functR[tipoR.index(comando)])
                break
            else:
                equivalenteDec.append(0) #(op) es 0
                equivalenteDec.append(setDeRegistros.index(param2))#(rs)
                equivalenteDec.append(setDeRegistros.index(param3))#(rt)
                equivalenteDec.append(setDeRegistros.index(param1))#(rd)
                equivalenteDec.append(0)#(shamt)
                equivalenteDec.append(functR[tipoR.index(comando)])
                break

    for x in tipoJ:
        if comando==x:
            tipo=2
            equivalenteDec.append(opcodeJ[tipoJ.index(comando)])
            equivalenteDec.append(param1)
            break

    equivalenteBin=""

    if tipo == 0:
        for x in range(len(equivalenteDec)):
            if x==0:
                formatiado=format(int(equivalenteDec[x]),'#08b')
                equivalenteBin=equivalenteBin+formatiado[2:]
            if x==1:
                formatiado=format(int(equivalenteDec[x]),'#07b')
                equivalenteBin=equivalenteBin+formatiado[2:]
            if x==2:
                formatiado=format(int(equivalenteDec[x]),'#07b')
                equivalenteBin=equivalenteBin+formatiado[2:]
            if x ==3:
                formatiado=format(int(equivalenteDec[x]),'#018b')
                equivalenteBin=equivalenteBin+formatiado[2:]
        
    equivalenteHex="0x"

    if tipo == 1:
        for x in range(len(equivalenteDec)):
            if x==0:
                formatiado=format(int(equivalenteDec[x]),'#08b')
                equivalenteBin=equivalenteBin+formatiado[2:]
            if x==1:
                formatiado=format(int(equivalenteDec[x]),'#07b')
                equivalenteBin=equivalenteBin+formatiado[2:]
            if x==2:
                formatiado=format(int(equivalenteDec[x]),'#07b')
                equivalenteBin=equivalenteBin+formatiado[2:]
            if x==3:
                formatiado=format(int(equivalenteDec[x]),'#07b')
                equivalenteBin=equivalenteBin+formatiado[2:]
            if x==4:
                formatiado=format(int(equivalenteDec[x]),'#07b')
                equivalenteBin=equivalenteBin+formatiado[2:]
            if x==5:
                formatiado=format(int(equivalenteDec[x]),'#08b')
                equivalenteBin=equivalenteBin+formatiado[2:]


    if tipo==2:
        address=4194304+((int(equivalenteDec[1]))*4)
        equivalenteDec[1]=address

    if tipo==0 or tipo ==1:
        for x in range(int(len(equivalenteBin)/4)):
            equivalenteHex=equivalenteHex+hex(int(equivalenteBin[3*x+x:3*x+x+4],2))[2:]
    else:
        hexAddress=hex(equivalenteDec[1])[2:]
        binaryHexAddress="0000"
        for x in range(len(hexAddress)):
            formatiado=format(int("0x"+hexAddress[x],16),'#06b')
            binaryHexAddress=binaryHexAddress+formatiado[2:]
        binaryHexAddress=binaryHexAddress
        equivalenteBin=equivalenteBin+(format(int(opcodeJ[tipoJ.index(comando)]),'#08b')[2:]) +binaryHexAddress
        for x in range(int(len(equivalenteBin)/4)):
            equivalenteHex=equivalenteHex+hex(int(equivalenteBin[3*x+x:3*x+x+4],2))[2:]
    return equivalenteHex

def mipsToHexFunct():
    textoSalida.delete('1.0',END)
    elCode=direccion.get()
    lineasDelCode=retornaLineas(elCode)
    lineasEnHex=""
    for x in lineasDelCode:
        lineasEnHex=lineasEnHex+lineaEnHex(x)+"\n"
    textoSalida.insert("insert",lineasEnHex)
    print(retornaLineas("mipsCode.txt"))

root=Tk()
elframe=Frame(root,width=300,height=600)
elframe.pack()

texto=Label(elframe, text="Nombre del archivo .txt"+"\n"+"Ejemplo: mipsCode.txt")
texto.place(x=90,y=20)

direccion=Entry(elframe)
direccion.place(x=94,y=65)

mipsToHexButton=Button(elframe, text="MIPS → Hex", command=mipsToHexFunct)
mipsToHexButton.place(x=120,y=105)

textoSalida=Text(elframe,width=24,height=25)
textoSalida.place(x=50,y=160)
    


root.mainloop()