
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
    
