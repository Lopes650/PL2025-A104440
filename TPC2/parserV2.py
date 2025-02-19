import re


def writeCompositores(listaCompositores):
    
    listaCompositores.sort()
    
    with open("TPC2/output2/ListaCompositores.txt", "w") as f2:
        
        for compositor in listaCompositores:
            f2.write(compositor + "\n")

def writeDicionario(dicionario):
    
    with open("TPC2/output2/DestribuiçãoPorPeriodo.txt", "w") as f:
        for chave, valor in dicionario.items():
            f.write(f"{chave}: {valor}\n")
            
def writeDicList(dicionario):
    with open("TPC2/output2/ObrasporPeriodo.txt", "w") as f:
        
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
    with open("TPC2/obras.csv") as f:
        f.readline()
        string = f.read()
    
    listaCompositores = []
    periodoDic = dict()
    periodoObraDic = dict()
    
    # Atualizar a expressão regular para incluir caracteres acentuados e espaços em branco
    pattern = re.compile(r"^(.*?);(?:.*?);(?:[0-9]{4});([\wÀ-ÿ ]+);([)('\wÀ-ÿ ,-]+);(?:[0-9:]+);(?:[A-Za-z0-9]+)$", re.MULTILINE | re.DOTALL)
    
    matches = pattern.findall(string)
    
    for match in matches:
        if match[2] not in listaCompositores:
            listaCompositores.append(match[2])
        
        periodoDic = orderPer(match[1], periodoDic)
        
        if match[1] not in periodoObraDic:
            periodoObraDic[match[1]] = [match[0]]
        else:
            periodoObraDic[match[1]].append(match[0])
    
    writeCompositores(listaCompositores)
    writeDicionario(periodoDic)
    writeDicList(periodoObraDic)

parserCSV()