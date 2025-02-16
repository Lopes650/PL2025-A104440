# Função de Processamento de Compositores e Obras

## 1. Objetivo

O objetivo do programa é processar dados sobre compositores e obras a partir de um arquivo CSV, realizar a organização dessas obras por período, e gerar três arquivos de saída contendo:
1. A lista de compositores.
2. A distribuição de obras por período.
3. A lista de obras por período.

## 2. Argumentos de Entrada

- **Arquivo CSV**: O arquivo de entrada `TPC2/obras.csv` contém informações sobre obras, incluindo título, período e compositor. As colunas são separadas por ponto e vírgula (`;`), e algumas linhas podem ter caracteres especiais que exigem tratamento específico.

## 3. Funcionamento

O programa realiza o processamento do arquivo CSV fazendo uso de:

1. **Função `writeCompositores(listaCompositores)`**:
   - Ordena a lista de compositores e escreve a lista em um arquivo de texto (`ListaCompositores.txt`).

2. **Função `writeDicionario(dicionario)`**:
   - Recebe um dicionário contendo a distribuição das obras por período e escreve esse dicionário em um arquivo de texto (`DestribuiçãoPorPeriodo.txt`).

3. **Função `writeDicList(dicionario)`**:
   - Recebe um dicionário contendo obras por período e escreve a lista de obras por período em um arquivo de texto (`ObrasporPeriodo.txt`).

4. **Função `orderPer(periodo, periodoDic)`**:
   - Atualiza a contagem das obras de cada período no dicionário `periodoDic`. Se o período já existir, incrementa a contagem, caso contrário, cria uma nova entrada com valor 1.

5. **Função `parserCSV()`**:
   - Processa o arquivo CSV, lê as informações sobre as obras, compositores e períodos.
   - Adiciona os compositores à lista `listaCompositores` e organiza as obras nos dicionários `periodoDic` e `periodoObraDic`.
   - Em seguida, chama as funções `writeCompositores()`, `writeDicionario()`, e `writeDicList()` para gerar os arquivos de saída.
  

O programa começa por fazer o parser caracter a caracter do ficheiro csv, armazenando na *String* `obra` todos os caracteres associados a uma obra. Após isso ele irá fazer uso da função `split` para dividir a `obra` nos seu componentes, tendo em atenção casos especias, retirando e armazenando os dados necessários em listas e dicionários e ignorando os desnecessários,  finalmente ira continuar a iteração e construir a obra seguinte. Após todo o ficheiro csv ter sido analisado, o programa irá usar as funções de escrita, acima descritas, para ordenar os dados e criar os ficheiros de outpu, finalizando a execução. 

## 4. Saída

O programa gera três arquivos de saída:

- `ListaCompositores.txt`: Contém a lista de compositores ordenada.
- `DestribuiçãoPorPeriodo.txt`: Contém a distribuição das obras por período.
- `ObrasporPeriodo.txt`: Contém as obras organizadas por período.

## 5. Exemplo de Uso

**Invocando:**
```python
parserCSV()
```

**São Gerados:**

**ListaCompositores.txt:**
```
Compositor A
Compositor B
Compositor C
...
```

**ObrasporPeriodo.txt:**

```
Período 1: 5 
Período 2: 3 
Período 3: 2 
...
```

**ObrasporPeriodo.txt:**
```
Período 1:
Obra 1
Obra 2
Obra 3
...

Período 2:
Obra 4
Obra 5
...
```

## 6. Observações

- O arquivo CSV de entrada deve ter 6 colunas separadas por ponto e vírgula (';'), com dados sobre o título da obra, período, compositor e outras informações.

- A função parserCSV() possui tratamento especial para linhas com dados fora do padrão (caso especial), garantindo a correta atribuição de dados.

- O programa ignora a contagem de obras por período repetido e organiza as obras no dicionário de acordo com o período.