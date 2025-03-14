import re

def conversorMDtoHTML(filepath):
    
    with open(filepath, 'r') as file:
        texto = file.read()
    
    # Conversão de Cabeçalhos:
    texto = re.sub(r'^(#+)\s*(.*)', lambda m: f'<h{len(m.group(1))}>{m.group(2)}</h{len(m.group(1))}>', texto, flags=re.M)
    
    # Conversão de Itálico e Bold:
    texto = re.sub(r'\*\*(.+)\*\*', r'<b>\1<b>', texto, flags=re.M)
    texto = re.sub(r'\*(.+)\*', r'<i>\1<i>', texto, flags=re.M)
    
    
    # Conversão de Listas Ordenadas:
    texto = re.sub(r'^\d+\.\s+(.+)', r'<li>\1</li>', texto, flags=re.M)
    texto = re.sub(r'(<li>.*?</li>(?:\n<li>.*?</li>)*)', r'<ol>\n\1\n</ol>', texto, flags=re.S)
    
    
    #Path para imagem:
    texto = re.sub(r'!\[(.+)\]\((.+)\)', r'<img src="\2" alt="\1">', texto, flags=re.M)
    
    #Conversão de URLs:
    texto = re.sub(r'\[(.+)\]\((.+)\)', r'<a href="\2">\1</a>', texto, flags=re.M)
    
    file = open("TPC3/teste.html", "w")
    file.write(texto)
    file.close()
    

conversorMDtoHTML("TPC3/teste.md")