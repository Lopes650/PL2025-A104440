# Máquina de Vendas

## 1. Objetivo

O objetivo deste programa é gerenciar o stock de produtos em uma máquina de vendas e controlar as transações de compras, incluindo o saldo inserido e a seleção de produtos. O sistema permite listar os produtos disponíveis, inserir saldo e selecionar produtos para compra, além de atualizar o stock após cada transação.

## 2. Funções Implementadas

### 2.1 **StockParser**

- **Objetivo**: Carrega o stock do ficheiro `stock.json` para a memória.
- **Entrada**: Caminho para o ficheiro JSON (`ficheiro`).
- **Saída**: Lista com os produtos presentes no stock, extraída do arquivo JSON.
- **Exemplo**:

#### stocks.json:
```json
   {
    "stock": 
        [
            {"cod": "A23", "nome": "água 0.5L", "quant": 8, "preco": 0.7},
            {"cod": "B45", "nome": "refrigerante 0.33L", "quant": 5, "preco": 1.2},
            {"cod": "C12", "nome": "sumo 0.25L", "quant": 10, "preco": 1.0},
            {"cod": "D67", "nome": "batata frita", "quant": 7, "preco": 1.5},
            {"cod": "E89", "nome": "barra de chocolate", "quant": 4, "preco": 1.8},
            {"cod": "F34", "nome": "pastilha elástica", "quant": 15, "preco": 0.5},
            {"cod": "G56", "nome": "bolacha oreo", "quant": 6, "preco": 1.3},
            {"cod": "H78", "nome": "maltesers", "quant": 9, "preco": 1.4},
            {"cod": "I90", "nome": "barra de whey", "quant": 5, "preco": 1.6},
            {"cod": "J21", "nome": "chá gelado 0.5L", "quant": 7, "preco": 1.1}
        ]
    }
```


#### stock:
```python
[{'cod': 'A23', 'nome': 'água 0.5L', 'quant': 8, 'preco': 0.7}, {'cod': 'B45', 'nome': 'refrigerante 0.33L', 'quant': 5, 'preco': 1.2}, {'cod': 'C12', 'nome': 'sumo 0.25L', 'quant': 10, 'preco': 1.0}, {'cod': 'D67', 'nome': 'batata frita', 'quant': 7, 'preco': 1.5}, {'cod': 'E89', 'nome': 'barra de chocolate', 'quant': 4, 'preco': 1.8}, {'cod': 'F34', 'nome': 'pastilha elástica', 'quant': 15, 'preco': 0.5}, {'cod': 'G56', 'nome': 'bolacha oreo', 'quant': 6, 'preco': 1.3}, {'cod': 'H78', 'nome': 'maltesers', 'quant': 9, 'preco': 1.4}, {'cod': 'I90', 'nome': 'barra de whey', 'quant': 5, 'preco': 1.6}, {'cod': 'J21', 'nome': 'chá gelado 0.5L', 'quant': 7, 'preco': 1.1}]
```
### 2.2 **atualizarStock**

- **Objetivo**: Atualiza o stock, no final da execução, no ficheiro JSON, com as informações finais do stock.
- **Entrada**: Caminho para o ficheiro JSON (`ficheiro`), Novo stock (`novo_stock`).
- **Saída**: O ficheiro `stock.json` é sobrescrito com o novo stock.

### 2.3 **listar_stock**

- **Objetivo**: Lista os produtos presentes no stock no terminal.
- **Entrada**: Lista de produtos (`stock`).
- **Saída**: Exibe no terminal as informações de todos os produtos no formato tabelado.
- **Exemplo**:

 #### Chamada:
  ```python
    listar_stock(stock)
  ```

  #### Saída:
  ```python
cod |  nome                 |  quantidade  |  preço
--------------------------------------------------
A23    água 0.5L               8              0.7  
B45    refrigerante 0.33L      5              1.2  
C12    sumo 0.25L              10             1.0  
D67    batata frita            7              1.5  
E89    barra de chocolate      4              1.8  
F34    pastilha elástica       15             0.5  
G56    bolacha oreo            6              1.3  
H78    maltesers               9              1.4  
I90    barra de whey           5              1.6  
J21    chá gelado 0.5L         7              1.1
  ```

### 2.4 **insereSaldo**

- **Objetivo**: Calcula o saldo total a partir de uma lista de moedas inseridas.
- **Entrada**: 
  - Lista de moedas (`moedas`), contendo as moedas inseridas (por exemplo, `["1e", "20c", "50c"]`).
  - Saldo inicial (`saldo`), representando o saldo disponível antes das moedas serem inseridas.
- **Saída**: O saldo total atualizado após a adição das moedas inseridas.

### 2.5 **formatar_saldo**

- **Objetivo**: Formata o saldo total em euros e cêntimos.
- **Entrada**: 
  - Saldo total (`saldo`), representando o valor a ser formatado (por exemplo, `3.75`).
- **Saída**: Saldo formatado como string no formato `xe yc`, onde `x` representa os euros e `y` representa os cêntimos.

### 2.6 **selecionarProduto**

- **Objetivo**: Seleciona um produto a partir do código e atualiza o saldo e o stock.
- **Entrada**: 
  - Código do produto (`código`), representando o identificador único do produto a ser selecionado (por exemplo, `"A23"`).
  - Lista de produtos (`stock`), contendo os itens disponíveis, com informações como código, nome, quantidade e preço.
  - Saldo atual (`saldo`), que é o valor disponível para a compra do produto.
- **Saída**: 
  - O saldo é atualizado, se o produto for comprado com sucesso.
  - O stock é modificado, com a quantidade do produto decrementada caso a compra seja realizada.
  
## 3. **Funcionamento do Sistema**

### **Carregar o Stock**
O programa carrega o stock do ficheiro `stock.json` ao iniciar, utilizando a função `StockParser`. Esta função lê o ficheiro JSON e armazena os dados de stock na memória para que possam ser acessados durante a execução do programa.

### **Inserção de Saldo**
O usuário pode inserir moedas utilizando o comando `MOEDAS`, que será interpretado pela função `insereSaldo`. O saldo é atualizado conforme as moedas válidas inseridas. As moedas válidas incluem valores como 1e, 50c, 2e, entre outros. Cada moeda inserida é convertida para o seu valor em euros e somada ao saldo atual.

### **Seleção de Produto**
O usuário pode selecionar um produto por meio do comando `SELECIONAR <código>`, onde `<código>` é o código do produto desejado. A função `selecionarProduto` verifica se o saldo do usuário é suficiente para a compra e se o produto está disponível no stock. Caso o saldo seja suficiente e o produto esteja em estoque, o saldo é atualizado, e a quantidade do produto selecionado é decrementada no stock.

### **Listagem de Produtos**
O comando `LISTAR` exibe todos os produtos disponíveis no stock, incluindo o código, nome, quantidade e preço de cada item. A função `listar_stock` é responsável por gerar a saída formatada no terminal, exibindo as informações de cada produto de maneira tabelada.

### **Saída e Atualização de Stock**
Ao sair, o programa atualiza o ficheiro `stock.json` com o stock atual utilizando a função `atualizarStock`. Essa função lê o arquivo JSON, substitui as informações de stock com as atualizadas durante a execução do programa e salva as mudanças no ficheiro.

## 4. **Exemplo de Uso**

#### Entrada (Comandos do Usuário):

```python
>> MOEDAS 1e,20c
>> SELECIONAR A23
>> LISTAR
>> SAIR
````
#### Saída (Terminal):
```python

maq: 2024-03-08, Stock carregado, Estado atualizado.
maq: Bom dia. Estou disponível para atender o seu pedido.
>> MOEDAS 1e,20c
Saldo = 1e20c

>> SELECIONAR A23
maq: Pode retirar o produto dispensado água 0.5L
maq: Saldo = 0e70c

>> LISTAR
cod   |  nome                 |  quantidade  |  preço
--------------------------------------------------
A23      água 0.5L            |  7           |  0.7  
B45      refrigerante 0.33L   |  5           |  1.2  
C12      sumo 0.25L           |  10          |  1.0  
...

>> SAIR
maq: Pode retirar o troco: 0e70c
maq: Até a Próxima!

```
```

