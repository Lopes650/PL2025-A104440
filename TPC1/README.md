# Função Somador On/Off

## 1. Objetivo

A função somador On/Off percorre um `texto`(*String*) e soma todas as sequências de dígitos lá presentes.Este comportamento é desativado caso seja encontrado um 'off' e reativado se for encontrado um 'on', em qualquer combinação de maiúsculas e minúsculas.Caso seja encontrado um '=' o resultado atual da soma é imprimido no terminal.

## 2. Argumentos de Entrada

-`texto` (*String*): Uma string com qualquer sequência de caracteres podendo, ou não, conter espaços entre os caracteres.

## 3. Funcionamento

A função inicia 4 variáveis:

-`soma` (*Int*): Inteiro que corresponde ao valor atual da soma, iniciando-se com valor 0

-`ativado` (*Bool*): Booleano que esclarece se o comportamento de soma está ativado(TRUE) ou não(FALSE), iniciando-se em TRUE.

-`c_number` (*Char*): Caracter que guarda a sequência de digítos atual, iniciando-se como NULL.

-`i` (*Int*): Representa o índice em que o programa se encontra no `texto`, iniciando-se em 0.

A função possui um loop `while` que irá percorrer todo `texto`
guardando o caracter atual em `char` e, caso este seja um dígito (`if char.isdigit()`), será adicionado ao `c_number`, caso contrário, a função vai entrar no `else`. 

Nesta etapa, a função irá verificar se existe alguma sequência de digítos para ser somada a `soma` (`if c_number:`):

-Caso exista:
É realizada a soma(`soma += int(c_number)`) e o `c_number` é colocado a NULL(`c_number = ''`) e procede-se para a próxima iteração.

-Caso não exista:
A função irá verificar se o char corresponde ao '='(`if char == '='`) ou, se estamos perante uma sequência "on"(`elif texto[i:i+2].lower() == "on"`) ou "off"(`texto[i:i+3].lower() == "off"`). Para cada um destes casos a função irá proceder como descrito no Objetivo.

Saindo do `while`, a função irá verificar se existe alguma sequência de dígitos `c_number` a ser somada, realizando a soma caso exista, imprimindo o resultado final e finalizando.

## 4. Saída
- A função imprime a `soma` sempre que for encontrado um '=' e, no final, antes de terminar a execução.

## 5. Exemplo de Uso

```python
somadorOnOff("Hoje, 7 de Fevereiro de 2025, o professor de Processamento de Linguagens deu-nos este trabalho para fazer.=OfF E deu-nos 7= dias para o fazer...On Cada trabalho destes vale 0.25 valores da nota final!")
```

**Saída esperada:**
```
2032
2032
2057
```
## 6. Observações
- O comando `"On"` pode aparecer múltiplas vezes para reativar a soma.

- O comando `"Off"` pausa a soma sem afetar valores anteriores.

- O caracter `"="` pode ser usado várias vezes para exibir a soma parcial.

- A função inicia com o comportamento da soma ativado.

- Se aparecer dígitos seguidos como, por exemplo, "123" o programa soma 123 e não 1+2+3.

