
def somadorOnOff(texto):
    
    soma = 0
    ativado = True
    c_number = ''
    i = 0
    
    while i < len(texto):
        
        char = texto[i]
        
        if char.isdigit() and ativado:
            c_number += char
            
        else:
            if c_number:
                soma += int(c_number)
                c_number = ''
            
            if char == '=':
                print(soma)
            
            elif texto[i:i+2].lower() == "on":
                ativado = True
                i += 1
            
            elif texto[i:i+3].lower() == "off":
                ativado = False
                i += 2
        
        i += 1;
    
    if c_number:
        soma += int(c_number)
        
    print(soma)
    

texto = "Hoje, 7 de Fevereiro de 2025, o professor de Processamento de Linguagens deu-nos este trabalho para fazer.=OfF E deu-nos 7= dias para o fazer...On Cada trabalho destes vale 0.25 valores da nota final!"

somadorOnOff(texto)