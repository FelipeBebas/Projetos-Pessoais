# **Documentação do Script: Geração de Imagens Personalizadas com Texto**

## **Descrição Geral**
Este script utiliza dados de um arquivo CSV para gerar imagens personalizadas a partir de um modelo PSD. Cada linha no CSV contém dois textos que são adicionados dinamicamente à imagem, com ajuste de posicionamento, tamanho e formatação.

---

## **Bibliotecas Utilizadas**
- **`PIL` (Pillow)**: Para manipulação de imagens (desenho e ajustes de texto).
- **`psd_tools`**: Para carregar e manipular arquivos PSD.
- **`pandas`**: Para carregar e processar arquivos CSV.
- **`os`**: Para operações de sistema e manipulação de caminhos.
- **`re`**: Para sanitizar nomes de arquivos, removendo caracteres inválidos.

---

## **Funcionamento**
1. **Entrada**:
   - Um arquivo PSD (`template.psd`): Utilizado como base para as imagens.
   - Um arquivo CSV (`texts.csv`): Contém duas colunas (`A` e `B`) com os textos que serão inseridos nas imagens.
   - Arquivos de fontes (`Montserrat-ExtraBold.ttf` e `Montserrat-Medium.ttf`): Usados para estilização do texto.

2. **Saída**:
   - Imagens no formato PNG, geradas no diretório `output`.

3. **Fluxo Principal**:
   - **Carregamento do PSD**: A primeira camada do arquivo PSD é usada como imagem base.
   - **Leitura do CSV**: Os textos são extraídos e tratados.
   - **Adição de Texto**:
     - Os textos são ajustados dinamicamente para caber nas caixas delimitadas.
     - O tamanho da fonte é recalculado caso o texto exceda o espaço disponível.
   - **Criação de Arquivos**: As imagens geradas são salvas no diretório de saída.

---

## **Estrutura do Código**

### **1. Configurações**
- Caminhos dos arquivos, como o diretório do script, o CSV, o PSD e as fontes, são definidos no início do código.
- Um diretório chamado `output` é criado, caso não exista, para salvar as imagens.

### **2. Função `add_text_to_image`**
Responsável por adicionar texto à imagem com as seguintes funcionalidades:
- Centralização automática.
- Ajuste dinâmico do texto para caber em um box de largura e altura definidas.
- Suporte a múltiplas linhas e espaçamento configurável.

### **3. Processamento do CSV**
- Os dados do CSV são lidos usando o `pandas`.
- As colunas do CSV são renomeadas para `A` e `B` para simplificar o código.

### **4. Geração das Imagens**
- Para cada linha do CSV:
  - Uma cópia da imagem base é criada.
  - O texto é extraído, estilizado e adicionado à imagem.
  - O nome do arquivo é gerado dinamicamente, utilizando a coluna `A` (tratada para evitar caracteres inválidos).
  - A imagem final é salva no diretório de saída.

### **5. Incremento do Contador**
- Um contador numera os arquivos gerados sequencialmente.

---

## **Entradas e Saídas**
### **Arquivo CSV (`texts.csv`)**
- Deve conter duas colunas:
  - **Coluna A**: Texto principal que será convertido para maiúsculas.
  - **Coluna B**: Texto secundário.
- Formato esperado: delimitado por `;`.

### **Modelo PSD (`template.psd`)**
- Deve conter uma camada utilizável como base para as imagens.

### **Fontes**
- Certifique-se de incluir os arquivos de fonte (`Montserrat-ExtraBold.ttf` e `Montserrat-Medium.ttf`) no mesmo diretório do script.

---

## **Dependências e Instalação**
Antes de executar o script, instale as dependências necessárias:
```bash
pip install pillow psd-tools pandas
