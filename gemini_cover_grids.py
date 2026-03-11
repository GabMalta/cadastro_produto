from PIL import Image, ImageDraw, ImageFont
import os

# === Configurações Globais de Estilo ===
COR_BANNER = (78, 185, 180) # O tom de turquesa da referência
COR_TEXTO = "white"
try:
    # Tente usar uma fonte bold do sistema. Ajuste o caminho se necessário.
    FONTE_PADRAO = ImageFont.truetype("arialbd.ttf", 90) # Windows
    # FONTE_PADRAO = ImageFont.truetype("/Library/Fonts/Arial Bold.ttf", 90) # Mac
except IOError:
    print("Aviso: Fonte Arial Bold não encontrada. Usando padrão.")
    FONTE_PADRAO = ImageFont.load_default()

# === Função Auxiliar de Redimensionamento Inteligente ===
def aspect_fill_crop(image_path, target_width, target_height):
    """
    Abre uma imagem, redimensiona proporcionalmente para preencher 
    o tamanho alvo e corta os excessos centralizados.
    """
    img = Image.open(image_path).convert('RGB')
    width, height = img.size
    
    # Calcula a proporção necessária para preencher a área
    ratio_w = target_width / width
    ratio_h = target_height / height
    scale = max(ratio_w, ratio_h)
    
    new_w = int(width * scale)
    new_h = int(height * scale)
    
    img_resized = img.resize((new_w, new_h), Image.LANCZOS)
    
    # Calcula o corte central
    left = (new_w - target_width) // 2
    top = (new_h - target_height) // 2

    
    img_cropped = img_resized.crop((left, top, left + target_width, top + target_height))
    return img_cropped


# (Inclua os imports e a função auxiliar 'aspect_fill_crop' aqui)
def layout_coluna_vertical(imagens_lista, texto="CREPE AMANDA", output="layout2.jpg"):
    LARGURA_TOTAL = 800
    ALTURA_TOTAL = 1200
    LARGURA_BANNER = 200
    
    canvas = Image.new('RGB', (LARGURA_TOTAL, ALTURA_TOTAL), "white")
    
    # 1. Calcula tamanho das imagens (4 empilhadas)
    largura_img = LARGURA_TOTAL - LARGURA_BANNER
    altura_img = ALTURA_TOTAL // 4
    
    # 2. Processa e cola as imagens na esquerda
    for i, img_path in enumerate(imagens_lista):
        img_processada = aspect_fill_crop(img_path, largura_img, altura_img)
        canvas.paste(img_processada, (0, i * altura_img))
        
    # 3. Cria o Banner Lateral (Usando uma nova imagem para poder rotacionar o texto)
    banner_lateral = Image.new('RGB', (LARGURA_BANNER, ALTURA_TOTAL), COR_BANNER)
    draw_banner = ImageDraw.Draw(banner_lateral)
    
    # Criar uma camada separada para o texto para poder rotacionar
    txt_layer = Image.new('RGBA', (ALTURA_TOTAL, LARGURA_BANNER), (255,255,255,0))
    draw_txt = ImageDraw.Draw(txt_layer)
    
    # Centralizar texto na camada temporária
    bbox = draw_txt.textbbox((0, 0), texto, font=FONTE_PADRAO)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    txt_pos_x = (ALTURA_TOTAL - text_w) / 2
    txt_pos_y = (LARGURA_BANNER - text_h) / 2 - 15

    draw_txt.text((txt_pos_x, txt_pos_y), texto, fill=COR_TEXTO, font=FONTE_PADRAO)
    
    # Rotacionar 90 graus e colar no banner principal
    rotated_txt = txt_layer.rotate(90, expand=1)
    
    # Ajuste fino da posição do texto rotacionado
    offset_x = (LARGURA_BANNER - rotated_txt.width) // 2
    offset_y = (ALTURA_TOTAL - rotated_txt.height) // 2
    
    banner_lateral.paste(rotated_txt, (offset_x, offset_y), rotated_txt)
    
    # Cola o banner final no canvas
    canvas.paste(banner_lateral, (largura_img, 0))
    
    canvas.save(output, quality=95)
    print(f"Layout 2 salvo: {output}")
    
# (Inclua os imports e a função auxiliar 'aspect_fill_crop' aqui)

def layout_hero_thumbnails(imagens_lista, texto="CREPE AMANDA", output="layout3.jpg"):
    TAMANHO = 1000 # Quadrado
    ALTURA_HERO = 550
    ALTURA_BANNER = 120
    ALTURA_THUMBS = TAMANHO - ALTURA_HERO - ALTURA_BANNER
    
    canvas = Image.new('RGB', (TAMANHO, TAMANHO), "white")
    draw = ImageDraw.Draw(canvas)
    
    # 1. Imagem Hero (A primeira da lista)
    hero_img = aspect_fill_crop(imagens_lista[0], TAMANHO, ALTURA_HERO)
    canvas.paste(hero_img, (0,0))
    
    # 2. Banner Central
    draw.rectangle([(0, ALTURA_HERO), (TAMANHO, ALTURA_HERO + ALTURA_BANNER)], fill=COR_BANNER)
    
    # Texto do Banner
    bbox = draw.textbbox((0, 0), texto, font=FONTE_PADRAO)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    pos_x = (TAMANHO - text_w) / 2
    pos_y = ALTURA_HERO + (ALTURA_BANNER - text_h) / 2 - 10
    draw.text((pos_x, pos_y), texto, fill=COR_TEXTO, font=FONTE_PADRAO)
    
    # 3. Thumbnails (As outras 3 imagens)
    largura_thumb = TAMANHO // 3
    y_start_thumbs = ALTURA_HERO + ALTURA_BANNER
    
    for i in range(3):
        # Pega da segunda imagem em diante (índice i+1)
        thumb_img = aspect_fill_crop(imagens_lista[i+1], largura_thumb, ALTURA_THUMBS)
        canvas.paste(thumb_img, (i * largura_thumb, y_start_thumbs))
        
    canvas.save(output, quality=95)
    print(f"Layout 3 salvo: {output}")
    
# (Inclua os imports e a função auxiliar 'aspect_fill_crop' aqui)

def layout_grid_translucido(imagens_lista, texto="CREPE AMANDA", output="layout4.jpg"):
    TAMANHO = 1000
    METADE = TAMANHO // 2
    
    # 1. Cria o grid base (igual ao original)
    canvas_base = Image.new('RGB', (TAMANHO, TAMANHO), "white")
    posicoes = [(0, 0), (METADE, 0), (0, METADE), (METADE, METADE)]
    
    for i, caminho in enumerate(imagens_lista):
        img = aspect_fill_crop(caminho, METADE, METADE)
        canvas_base.paste(img, posicoes[i])
        
    # 2. Criar camada para transparência (RGBA)
    overlay = Image.new('RGBA', (TAMANHO, TAMANHO), (0,0,0,0))
    draw_overlay = ImageDraw.Draw(overlay)
    
    # 3. Desenhar a faixa translúcida
    ALTURA_FAIXA = 200
    y_faixa_inicio = (TAMANHO - ALTURA_FAIXA) // 2
    y_faixa_fim = y_faixa_inicio + ALTURA_FAIXA
    
    # Cor Turquesa com Alpha (Transparência). O último número (200) é a opacidade (0-255)
    cor_translucida = COR_BANNER + (220,) 
    draw_overlay.rectangle([(0, y_faixa_inicio), (TAMANHO, y_faixa_fim)], fill=cor_translucida)
    
    # 4. Texto
    bbox = draw_overlay.textbbox((0, 0), texto, font=FONTE_PADRAO)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    pos_x = (TAMANHO - text_w) / 2
    pos_y = (TAMANHO - text_h) / 2 - 10
    
    draw_overlay.text((pos_x, pos_y), texto, fill=COR_TEXTO, font=FONTE_PADRAO)
    
    # 5. Compor a imagem base com o overlay
    canvas_final = Image.alpha_composite(canvas_base.convert('RGBA'), overlay)
    
    canvas_final.convert('RGB').save(output, quality=95)
    print(f"Layout 4 salvo: {output}")

def layout_mosaic_pro(imagens_lista, texto="CREPE AMANDA", output="layout5.jpg"):
    TAMANHO = 1000
    LARGURA_GRANDE = 650
    LARGURA_PEQUENA = TAMANHO - LARGURA_GRANDE
    ALTURA_PEQUENA = TAMANHO // 3
    
    canvas = Image.new('RGB', (TAMANHO, TAMANHO), "white")
    
    # 1. Imagem de Destaque (Esquerda)
    img_grande = aspect_fill_crop(imagens_lista[0], LARGURA_GRANDE, TAMANHO)
    canvas.paste(img_grande, (0, 0))
    
    # 2. Três imagens menores (Direita)
    for i in range(1, 4):
        img_sm = aspect_fill_crop(imagens_lista[i], LARGURA_PEQUENA, ALTURA_PEQUENA)
        canvas.paste(img_sm, (LARGURA_GRANDE, (i-1) * ALTURA_PEQUENA))
        
    # 3. Etiqueta de Texto (Pill Shape no canto)
    draw = ImageDraw.Draw(canvas)
    padding_h, padding_v = 40, 20
    bbox = draw.textbbox((0, 0), texto, font=FONTE_PADRAO)
    txt_w = bbox[2] - bbox[0]
    txt_h = bbox[3] - bbox[1]
    
    rect_x0, rect_y0 = 30, TAMANHO - txt_h - (padding_v * 2) - 30
    rect_x1, rect_y1 = rect_x0 + txt_w + (padding_h * 2), TAMANHO - 30
    
    # Desenha o fundo da etiqueta (Turquesa)
    draw.rectangle([rect_x0, rect_y0, rect_x1, rect_y1], fill=COR_BANNER)
    draw.text((rect_x0 + padding_h, rect_y0 + padding_v - 5), texto, fill=COR_TEXTO, font=FONTE_PADRAO)
    
    canvas.save(output, quality=95)
    print(f"Layout 5 salvo: {output}")
    
def layout_gallery_clean(imagens_lista, texto="CREPE AMANDA", output="layout6.jpg"):
    TAMANHO = 1000
    MARGEM = 20  # Espaço entre as fotos e bordas
    TAM_IMG = (TAMANHO - (MARGEM * 3)) // 2
    
    canvas = Image.new('RGB', (TAMANHO, TAMANHO), "white")
    draw = ImageDraw.Draw(canvas)
    
    # 1. Posicionamento das 4 imagens com margens
    posicoes = [
        (MARGEM, MARGEM), 
        (TAM_IMG + MARGEM * 2, MARGEM),
        (MARGEM, TAM_IMG + MARGEM * 2),
        (TAM_IMG + MARGEM * 2, TAM_IMG + MARGEM * 2)
    ]
    
    for i in range(4):
        img = aspect_fill_crop(imagens_lista[i], TAM_IMG, TAM_IMG)
        canvas.paste(img, posicoes[i])
        
    # 2. Barra Central de Texto (Flutuante e menor)
    ALTURA_BARRA = 100
    y0 = (TAMANHO - ALTURA_BARRA) // 2
    draw.rectangle([0, y0, TAMANHO, y0 + ALTURA_BARRA], fill=COR_BANNER)
    
    # Texto (ajustando o tamanho da fonte para caber na barra menor)
    fonte_menor = ImageFont.truetype("arialbd.ttf", 60) if "arialbd.ttf" else FONTE_PADRAO
    bbox = draw.textbbox((0, 0), texto, font=fonte_menor)
    txt_w, txt_h = bbox[2]-bbox[0], bbox[3]-bbox[1]
    draw.text(((TAMANHO-txt_w)//2, y0 + (ALTURA_BARRA-txt_h)//2 - 5), texto, fill=COR_TEXTO, font=fonte_menor)
    
    canvas.save(output, quality=95)
    print(f"Layout 6 salvo: {output}")
    
def layout_split_vertical(imagens_lista, texto="CREPE AMANDA", output="layout7.jpg"):
    TAMANHO = 1000
    LARGURA_FATIA = TAMANHO // 4
    
    canvas = Image.new('RGB', (TAMANHO, TAMANHO), "white")
    draw = ImageDraw.Draw(canvas)
    
    # 1. Colar as 4 fatias verticais
    for i in range(4):
        img = aspect_fill_crop(imagens_lista[i], LARGURA_FATIA, TAMANHO)
        canvas.paste(img, (i * LARGURA_FATIA, 0))
        
    # 2. Círculo Central ou Losango para o Texto
    # Vamos usar um retângulo arredondado centralizado
    largura_box, altura_box = 700, 180
    x0, y0 = (TAMANHO - largura_box)//2, (TAMANHO - altura_box)//2
    x1, y1 = x0 + largura_box, y0 + altura_box
    
    # Desenha um box com borda branca para destacar das fatias
    draw.rectangle([x0-5, y0-5, x1+5, y1+5], fill="white") # Borda externa
    draw.rectangle([x0, y0, x1, y1], fill=COR_BANNER)
    
    # Texto
    bbox = draw.textbbox((0, 0), texto, font=FONTE_PADRAO)
    txt_w, txt_h = bbox[2]-bbox[0], bbox[3]-bbox[1]
    draw.text(((TAMANHO-txt_w)//2, (TAMANHO-txt_h)//2 - 10), texto, fill=COR_TEXTO, font=FONTE_PADRAO)
    
    canvas.save(output, quality=95)
    print(f"Layout 7 salvo: {output}")
    
def layout_circular_focus(imagens_lista, texto="CREPE AMANDA", output="layout8.jpg"):
    TAMANHO = 1000
    canvas = Image.new('RGB', (TAMANHO, TAMANHO), "white")
    
    # 1. Três fatias horizontais ao fundo
    altura_fatia = TAMANHO // 3
    for i in range(3):
        img = aspect_fill_crop(imagens_lista[i], TAMANHO, altura_fatia)
        canvas.paste(img, (0, i * altura_fatia))
        
    # 2. Círculo Central com a 4ª imagem
    diametro = 450
    img_circ = aspect_fill_crop(imagens_lista[3], diametro, diametro)
    
    # Criar máscara circular
    mask = Image.new('L', (diametro, diametro), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0, diametro, diametro), fill=255)
    
    # Colar com borda branca
    pos_central = ((TAMANHO - diametro)//2, (TAMANHO - diametro)//2)
    draw_border = ImageDraw.Draw(canvas)
    borda = 15
    draw_border.ellipse((pos_central[0]-borda, pos_central[1]-borda, 
                         pos_central[0]+diametro+borda, pos_central[1]+diametro+borda), fill="white")
    
    canvas.paste(img_circ, pos_central, mask)
    
    # 3. Texto curvo ou etiqueta inferior
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([250, 850, 750, 950], fill=COR_BANNER)
    bbox = draw.textbbox((0, 0), texto, font=FONTE_PADRAO)
    draw.text(((TAMANHO-(bbox[2]-bbox[0]))//2, 875), texto, fill=COR_TEXTO, font=FONTE_PADRAO)
    
    canvas.save(output, quality=95)
    
def layout_diagonal_split(imagens_lista, texto="CREPE AMANDA", output="layout9.jpg"):
    TAMANHO = 1000
    # Cria duas imagens grandes
    img_esq = aspect_fill_crop(imagens_lista[0], TAMANHO, TAMANHO)
    img_dir = aspect_fill_crop(imagens_lista[1], TAMANHO, TAMANHO)
    
    # Máscara diagonal
    mask = Image.new('L', (TAMANHO, TAMANHO), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.polygon([(TAMANHO, 0), (TAMANHO, TAMANHO), (0, TAMANHO)], fill=255)
    
    img_esq.paste(img_dir, (0,0), mask)
    canvas = img_esq
    
    #Faixa Diagonal Turquesa
    overlay = Image.new('RGBA', (TAMANHO, TAMANHO), (0,0,0,0))
    draw_ov = ImageDraw.Draw(overlay)
    draw_ov.line([(0, TAMANHO), (TAMANHO, 0)], fill="gray", width=30)
    
    canvas.paste(overlay, (0,0), overlay)
    
    # Texto (Simples no centro para evitar complexidade de rotação de fontes no PIL)
    draw = ImageDraw.Draw(canvas)
    bbox = draw.textbbox((0, 0), texto, font=FONTE_PADRAO)
    draw.text(((TAMANHO-(bbox[2]-bbox[0]))//2, (TAMANHO//2)-50), texto, fill="white", stroke_fill="black",stroke_width=5, font=FONTE_PADRAO)
    
    canvas.save(output, quality=95)

def layout_masonry(imagens_lista, texto="CREPE AMANDA", output="layout11.jpg"):
    TAMANHO = 1000
    canvas = Image.new('RGB', (TAMANHO, TAMANHO), "white")
    
    # Definição de blocos assimétricos (x, y, largura, altura)
    blocos = [
        (0, 0, 400, 600),   # Alta esquerda
        (400, 0, 600, 400), # Larga topo direita
        (0, 600, 600, 400), # Larga base esquerda
        (600, 400, 400, 600) # Alta direita baixo
    ]
    
    for i in range(4):
        x, y, w, h = blocos[i]
        img = aspect_fill_crop(imagens_lista[i], w, h)
        canvas.paste(img, (x, y))
        
    # Overlay central pequeno e quadrado
    draw = ImageDraw.Draw(canvas)
    side = 300
    draw.rectangle([(TAMANHO-side)//2, (TAMANHO-side)//2, (TAMANHO+side)//2, (TAMANHO+side)//2], fill=COR_BANNER, outline="white", width=5)
    
    # Quebrar texto em duas linhas se for grande
    fonte_p = ImageFont.truetype("arialbd.ttf", 50)
    draw.text((380, 470), "CREPE\nAMANDA", fill="white", font=fonte_p, align="center")
    
    canvas.save(output, quality=95)
    
# Exemplo de uso:
# path = r'D:\SITE LEGITIMA TEXTIL\CATÁLOGO DIGITAL\TULE PEROLA LISO ACTT149\TULE PEROLA LISO ACTT149 - Fotos'
# fotos = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')][:4]


# layout_faixa_horizontal(fotos, texto="TULE PEROLA LISO")
# layout_coluna_vertical(fotos, texto="TULE PEROLA LISO")
# layout_hero_thumbnails(fotos, texto="TULE PEROLA LISO")
# layout_grid_translucido(fotos, texto="TULE PEROLA LISO")
# layout_mosaic_pro(fotos, texto="TULE PEROLA LISO")
# layout_gallery_clean(fotos, texto="TULE PEROLA LISO")
# layout_split_vertical(fotos, texto="TULE PEROLA LISO")
# layout_circular_focus(fotos, texto="TULE PEROLA LISO")
# layout_diagonal_split(fotos, texto="TULE PEROLA LISO")
# layout_masonry(fotos, texto="TULE PEROLA LISO")
