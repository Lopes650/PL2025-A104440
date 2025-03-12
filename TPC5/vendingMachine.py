import json
import re

def StockParser(ficheiro):
    """Carrega o stock do ficheiro JSON para a memória."""
    
    with open(ficheiro, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    print(dados['stock'])
    return dados["stock"]

def atualizarStock(ficheiro, novo_stock):
    """Atualiza o stock no ficheiro JSON."""
    
    with open(ficheiro, 'r', encoding='utf-8') as f:
        dados = json.load(f)

    dados["stock"] = novo_stock

    with open(ficheiro, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)


def listar_stock(stock):

    """Lista o stock no terminal."""
    
    lengthy = 0;
    max = 0;
    
    for item in stock:
        if(len(item['nome']) > max):
            max = len(item['nome']);
    
    max += 5;
    print("cod |  nome                 |  quantidade  |  preço")
    print("-" * 50)
    
    for item in stock:
        print(f"{item['cod']: <6} {item['nome']: <{max}} {item['quant']: <14} {item['preco']: <5}")

def insereSaldo(moedas, saldo):
    """Calcula e formata o saldo total a partir de uma lista de moedas inseridas."""
    
    válidas = {
        "1e": 1.00,
        "2e": 2.00,
        "50c": 0.50,
        "20c": 0.20,
        "10c": 0.10,
        "5c": 0.05,
        "2c": 0.02,
        "1c": 0.01
    }

    # Somar os valores das moedas válidas inseridas
    total = sum(válidas[moeda] for moeda in moedas if moeda in válidas) + saldo

    return total

def formatar_saldo(saldo):
    inteiro = int(saldo)  
    decimal = round((saldo - inteiro) * 100)  
    return f"{inteiro}e{decimal}c"

def selecionarProduto(código, stock, saldo):
    """Seleciona um produto a partir do código e atualiza o saldo e o stock."""
    
    for item in stock:
        if item['cod'] == código:
            if item['preco'] <= saldo and item['quant'] > 0:
                item['quant'] -= 1
                saldo -= item['preco']
                print(f"maq: Pode retirar o produto dispensado {item['nome']}")
                print(f"maq: Saldo = {formatar_saldo(saldo)}")
                return saldo, stock  # Retornar uma tupla
            
            if item['preco'] > saldo:
                print("maq: Saldo insuficiente para satisfazer o seu pedido.")  
                print(f"maq: Saldo: {formatar_saldo(saldo)} Pedido: {formatar_saldo(item['preco'])}")
                return saldo, stock  # Retorna sem modificar saldo ou stock
            
            if item['quant'] == 0:
                print("maq: Produto esgotado.") 
                return saldo, stock
    
    print("Produto não encontrado.")
    return saldo, stock

def main():
    
    stock = StockParser("stock.json")
    saldo = 0.0
    
    print("maq: 2024-03-08, Stock carregado, Estado atualizado.")
    print("maq: Bom dia. Estou disponível para atender o seu pedido.")
    
    while True:
        
        comando = input(">> ").strip().upper()
        
        if comando == 'LISTAR':
            listar_stock(stock)
            continue
        
        match = re.match(r"MOEDAS\s+((?:\d+[ec](?:,\s*)?)*)$", comando, re.IGNORECASE)
        match2 = re.match(r"SELECIONAR\s+(\w\d+)$", comando, re.IGNORECASE)
        
        if match:
            moedas_str = match.group(1).lower()
            moedas = re.findall(r"\d+[ec]", moedas_str)  

            saldo = insereSaldo(moedas, saldo)

            print(f"Saldo = {formatar_saldo(saldo)}")
            continue
        
        if match2:
            código = match2.group(1)
            saldo, stock = selecionarProduto(código, stock, saldo)
            
            continue
        
        if comando == 'SALDO':
            print(f"maq: Saldo = {formatar_saldo(saldo)}")
            continue
        
        
        
        if comando == 'SAIR':
            atualizarStock("stock.json", stock)
            print(f"maq: Pode retirar o troco: {formatar_saldo(saldo)}")
            print("maq: Até a Próxima!")
            break;
            
        else:
            print("maq: Comando inválido.")
            continue
    
    

if __name__ == "__main__":
    main()






