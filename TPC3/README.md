# Conversor de Markdown para HTML

## 1. Objetivo

O objetivo do programa é converter arquivos de texto em formato Markdown para HTML. O conversor utiliza expressões regulares para identificar padrões do Markdown e substituí-los por suas equivalentes tags HTML.

## 2. Argumentos de Entrada

- **Arquivo de Entrada**: O arquivo Markdown deve ser um documento de texto estruturado contendo cabeçalhos, listas, texto formatado, links e imagens.

## 3. Funcionamento

O programa realiza a conversão do arquivo Markdown para HTML por meio das seguintes transformações:

1. **Conversão de Cabeçalhos:**

   - Identifica e substitui cabeçalhos Markdown (`#`, `##`, `###`, etc.) por tags HTML `<h1>`, `<h2>`, `<h3>`, etc.
   - Utiliza a expressão regular `^(#+)\s*(.*)` para capturar os níveis de cabeçalho e o título correspondente.

2. **Conversão de Texto Formatado:**

   - Substitui **negrito** (`**texto**`) por `<b>texto</b>`.
   - Substitui *itálico* (`*texto*`) por `<i>texto</i>`.
   - Utiliza as expressões regulares `\*\*(.+)\*\*` e `\*(.+)\*` para capturar os textos formatados.

3. **Conversão de Listas Ordenadas:**

   - Identifica itens de listas numeradas (`1. Item`) e os converte para `<li>Item</li>`.
   - Seguidamente identifica os itens `<li>Item<li>`, previamente convertidos, e coloca-os entre`<ol></ol>`
   - A expressão regular usada para capturar os itens é `^(\d+\.\s+.+)`.
   - A expressão regular usada para capturar os itens convertidos é `(<li>\d+\..*?</li>(?:\n<li>\d+\..*?</li>)*)`.

1. **Conversão de Links:**

   - Substitui links Markdown (`[texto](url)`) por links HTML (`<a href="url">texto</a>`).
   - Utiliza a expressão `\[(.+)\]\((.+)\)` para a conversão.

2. **Conversão de Imagens:**

   - Substitui imagens Markdown (`![alt](url)`) por imagens HTML (`<img src="url" alt="alt">`).
   - Utiliza a expressão `!\[(.+)\]\((.+)\)`.

## 4. Saída

O programa gera um arquivo HTML com a formatação correspondente ao conteúdo original do Markdown. O arquivo de saída é salvo como `TPC3/teste.html`.

## 5. Exemplo de Uso

### **Entrada (Markdown):**

```markdown
# Exemplo

Este é um **exemplo**
Este é um *exemplo*

1. Primeiro item
2. Segundo item
3. Terceiro item
4. Quarto item
5. Quinto item
   
Como pode ser consultado em [página da UC](http://www.uc.pt)

1. Primeiro item
2. Segundo item
3. Terceiro item

Como se vê na imagem seguinte: ![imagem dum coelho](http://www.coellho.com)
```

### **Saída (HTML)**:

```html
<h1>Exemplo</h1>

Este é um <b>exemplo<b>
Este é um <i>exemplo<i>

<li>Primeiro item</li>
<li>Segundo item</li>
<li>Terceiro item</li>
<li>Quarto item</li>
<li>Quinto item</li>

Como pode ser consultado em <a href="http://www.uc.pt">página da UC</a>

<li>Primeiro item</li>
<li>Segundo item</li>
<li>Terceiro item</li>

Como se vê na imagem seguinte: <img src="http://www.coellho.com" alt="imagem dum coelho">
```

