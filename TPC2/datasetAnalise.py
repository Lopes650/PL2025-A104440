
def writeCompositores(listaCompositores):
    
    listaCompositores.sort()
    
    with open("TPC2/output/ListaCompositores.txt", "w") as f2:
        
        for compositor in listaCompositores:
            f2.write(compositor + "\n")

def writeDicionario(dicionario):
    
    with open("TPC2/output/DestribuiçãoPorPeriodo.txt", "w") as f:
        for chave, valor in dicionario.items():
            f.write(f"{chave}: {valor}\n")
            
def writeDicList(dicionario):
    with open("TPC2/output/ObrasporPeriodo.txt", "w") as f:
        
        for chave, lista_args in dicionario.items():
            f.write(f"{chave}:\n")
            for arg in lista_args:
                f.write(f"{arg}\n")
            f.write("\n")


def orderPer(periodo, periodoDic):
    
    if periodo in periodoDic:           
        periodoDic[periodo] = periodoDic[periodo] + 1
    else:
        periodoDic[periodo] = 1
    
    return periodoDic

def parserCSV():
    
    f = open("TPC2/obras.csv")
    f.readline()
    obra = ""
    counter = 0
    anterior = ''
    casoEspecial = False
    
    listaCompositores = []
    periodoDic = dict()
    periodoObraDic = dict()
    
    for linha in f.readlines():
        
        if linha.count(";") == 6:
            
            partes = linha.split(";")
            
            titulo = partes[0]
            periodo = partes[3]
            compositor = partes[4]
        
            if compositor not in listaCompositores:
                listaCompositores.append(compositor)
            
            periodoDic = orderPer(periodo,periodoDic)
        
            if periodo not in periodoObraDic:
                periodoObraDic[periodo] = []  # Inicializa a lista se a chave não existir
            periodoObraDic[periodo].append(titulo)
        
        else:    
            for char in linha:
                #print(char)
                obra += char 
            
                if char == ";":
                
                    if counter == 1 and anterior == '"':
                        counter += 1
                        #print(counter)
                    
                    
                    elif counter != 1:
                        counter += 1
                        #print(counter)
                    else:
                        casoEspecial = True
                
                anterior = char
            
                if counter == 6 and char == '\n':
                    
                    if casoEspecial == False:
                        counter = 0
                        partes = obra.split(";")

                        titulo = partes[0]
                        periodo = partes[3]
                        compositor = partes[4]
                        
                        if compositor not in listaCompositores:
                            listaCompositores.append(compositor)
                            
                        periodoDic = orderPer(periodo,periodoDic)
                        
                        if periodo not in periodoObraDic:
                            periodoObraDic[periodo] = []  # Inicializa a lista se a chave não existir
                        periodoObraDic[periodo].append(titulo)
                        
                        obra = ''
                        #print(titulo)
                        #print(periodo)
                    
                    else:
                        counter = 0
                        err = obra.count(";") - 6
                        partes = obra.split(";")
                        
                        titulo = partes[0] 
                        periodo = partes[3 + err]
                        compositor = partes[4 + err]
                        
                        if compositor not in listaCompositores:
                            listaCompositores.append(compositor)
                            
                        
                        periodoDic = orderPer(periodo,periodoDic)
                        if periodo not in periodoObraDic:
                            periodoObraDic[periodo] = []  # Inicializa a lista se a chave não existir
                        periodoObraDic[periodo].append(titulo)

                        
                        obra = ''
                        casoEspecial = False
                        #print(titulo)
    
    partes = obra.split(";")
    
    titulo = partes[0]
    periodo = partes[3]
    compositor = partes[4]
    
    print(titulo)
    if compositor not in listaCompositores:
        listaCompositores.append(compositor)
                        
    periodoDic = orderPer(periodo,periodoDic)
                    
    if periodo not in periodoObraDic:
        periodoObraDic[periodo] = [] 
        
    periodoObraDic[periodo].append(titulo)
    
    writeCompositores(listaCompositores)
    writeDicionario(periodoDic)
    writeDicList(periodoObraDic)

parserCSV()









