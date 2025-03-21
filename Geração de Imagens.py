# Importação das bibliotecas necessárias
from PIL import Image, ImageDraw, ImageFont  # Para manipulação de imagens
from psd_tools import PSDImage  # Para trabalhar com arquivos PSD
import pandas as pd  # Para carregar e processar dados CSV
import os  # Para manipulação de diretórios e arquivos
import re  # Para tratar nomes de arquivos

# Função para adicionar texto à imagem
def add_text_to_image(image, text, position, font_path, font_size_px, color, max_width=None, box_height=None, line_spacing=0):
    # Criação de um objeto para desenhar na imagem
    draw = ImageDraw.Draw(image)

    # Carregamento da fonte com o tamanho especificado
    font = ImageFont.truetype(font_path, int(font_size_px))

    # Substitui '\n' por quebras de linha reais
    text = text.replace('\\n', '\n')

    # Verifica se há restrições de largura e altura do box de texto
    if max_width and box_height:
        # Divide o texto em linhas
        lines = text.split('\n')
        adjusted_lines = []

        # Ajusta as linhas para caber no box
        for line in lines:
            words = line.split()
            line = ''
            while words:
                test_line = f"{line} {words[0]}" if line else words[0]
                if draw.textbbox((0, 0), test_line, font=font)[2] <= max_width:
                    line = test_line
                    words.pop(0)
                else:
                    adjusted_lines.append(line)
                    line = ''
            if line:
                adjusted_lines.append(line)

        # Ajusta o tamanho da fonte se o texto exceder a altura do box
        line_height = draw.textbbox((0, 0), 'A', font=font)[3]
        if (line_height + line_spacing) * len(adjusted_lines) > box_height:
            font_size_px = font_size_px * box_height / ((line_height + line_spacing) * len(adjusted_lines))
            font = ImageFont.truetype(font_path, int(font_size_px))

            # Recalcula as linhas com o novo tamanho de fonte
            adjusted_lines = []
            for line in lines:
                words = line.split()
                line = ''
                while words:
                    test_line = f"{line} {words[0]}" if line else words[0]
                    if draw.textbbox((0, 0), test_line, font=font)[2] <= max_width:
                        line = test_line
                        words.pop(0)
                    else:
                        adjusted_lines.append(line)
                        line = ''
                if line:
                    adjusted_lines.append(line)

        # Insere as linhas na imagem, centralizando o texto
        y = position[1]
        for line in adjusted_lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            w = bbox[2] - bbox[0]
            x = position[0] + (max_width - w) / 2
            draw.text((x, y), line, font=font, fill=color)
            y += line_height + line_spacing
            if y > position[1] + box_height:
                break
    else:
        # Caso não existam restrições de box
        lines = text.split('\n')
        total_height = len(lines) * (draw.textbbox((0, 0), 'A', font=font)[3] + line_spacing)
        y = position[1]
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            w = bbox[2] - bbox[0]
            x = (image.width - w) / 2
            draw.text((x, y), line, font=font, fill=color)
            y += draw.textbbox((0, 0), 'A', font=font)[3] + line_spacing

# Caminhos dos arquivos (relativos ao local do script)
current_directory = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_directory, 'texts.csv')
psd_path = os.path.join(current_directory, 'template.psd')
font_bold_path = os.path.join(current_directory, 'Montserrat-ExtraBold.ttf')
font_medium_path = os.path.join(current_directory, 'Montserrat-Medium.ttf')

# Carregamento do CSV com codificação UTF-8 e delimitador ";"
df = pd.read_csv(csv_path, encoding='utf-8', delimiter=';')

# Exibe as primeiras linhas para verificar os dados
print("Primeiras linhas do CSV:")
print(df.head())

# Renomeia as colunas para 'A' e 'B' para facilitar o uso
df.columns = ['A', 'B']

# Carregamento do arquivo PSD
psd = PSDImage.open(psd_path)

# Assume que a base da imagem está na primeira camada
base_image = psd[0].composite()

# Definições de fontes, tamanhos e posições
font_size_text1_px = 109.37
font_size_text2_px = 107.00
color = "#434342"

# Posições e dimensões dos textos
position_text1 = (base_image.width / 2, 1008.6)
position_text2 = (206, 1205.6)
max_width_text2 = 3364 - 206
box_height_text2 = 400
line_spacing = 25

# Cria um diretório de saída se ele não existir
output_dir = os.path.join(current_directory, 'output')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Função para criar nomes de arquivos válidos
def sanitize_filename(text):
    return re.sub(r'\W+', '_', text)

# Contador para numerar os arquivos
counter = 1

# Loop para processar cada linha do CSV
for i, row in df.iterrows():
    # Cria uma cópia da imagem base
    image = base_image.copy()
    
    # Obtém os textos das colunas A e B
    text1 = row['A'].upper()  # Converte o texto 1 para maiúsculas
    text2 = row['B']

    # Adiciona os textos à imagem
    add_text_to_image(image, text1, position_text1, font_bold_path, font_size_text1_px, color)
    add_text_to_image(image, text2, position_text2, font_medium_path, font_size_text2_px, color, max_width=max_width_text2, box_height=box_height_text2, line_spacing=line_spacing)

    # Gera o nome do arquivo com um contador e salva a imagem
    sanitized_filename = sanitize_filename(text1)
    filename = f"{counter}_{sanitized_filename}.png"
    image.save(os.path.join(output_dir, filename))

    # Incrementa o contador
    counter += 1

print("Imagens geradas com sucesso!")
