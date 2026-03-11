# Quick Reference - Cover Product API

## Inicialização

```python
from apps.data_scraping.utils.cover_product import CoverProduct

cover = CoverProduct(
    product_path="C:\\caminho\\para\\produto",
    size_cover=1280,           # Padrão: 1280
    promocao=False,            # Padrão: False
    config_path=None           # Usa padrão se None
)
```

## Métodos Principais

### 1. Generate Cover (Novo - Recomendado)
```python
filepath = cover.generate_cover(
    layout_name="grid_3x3",    # Nome do layout
    name_save="capa1",         # Nome do arquivo
    title=None,                # Título opcional
    fill=None,                 # Cor do banner RGB
    stroke_fill="#fff",        # Cor da borda do texto
    stroke_width=5,            # Largura da borda
    font_color="#000"          # Cor do texto
)
```

### 2. Métodos Legados (Ainda Funcionam)
```python
# Faixa Horizontal (4 imagens)
cover.layout_faixa_horizontal(name_save, title, fill, font_color)

# Grid 3x3 (9 imagens)
cover.cover_grid(name_save, title, fill, stroke_fill, stroke_width, font_color)

# Três Imagens
cover.cover_three(name_save, title, fill, stroke_fill, stroke_width, font_color)

# Grid Custom 5 imagens
cover.cover_grid_2(name_save, title, fill, stroke_fill, stroke_width, font_color)

# Grid Custom 6 imagens
cover.cover_grid_3(name_save, title, fill, stroke_fill, stroke_width, font_color)

# Imagem inteira com logo
cover.cover_full_logo(name_save, title, company="LEGITIMA")
```

## Layouts Disponíveis - Originais

| Nome | Imagens | Descrição |
|------|---------|-----------|
| `faixa_horizontal` | 4 | 4 imagens em strip |
| `grid_3x3` | 9 | Grid 3x3 |
| `cover_three` | 3 | Assimétrico |
| `grid_5_images` | 5 | Custom 5 imagens |
| `grid_6_images` | 6 | Custom 6 imagens |
| `full_image_with_logo` | 1 | Imagem inteira com logo |

## Novos Layouts Customizados ✨

| Nome | Imagens | Descrição |
|------|---------|-----------|
| `layout_coluna_vertical` | 4 | 4 imagens empilhadas verticalmente com banner lateral rotacionado |
| `layout_hero_thumbnails` | 4 | Imagem hero no topo com 3 thumbnails abaixo e banner central |
| `layout_grid_translucido` | 4 | Grid 2x2 com faixa translúcida horizontal no centro |
| `layout_mosaic_pro` | 4 | Imagem grande à esquerda com 3 imagens menores empilhadas à direita |
| `layout_gallery_clean` | 4 | 4 imagens com margens e barra de banner centralizada |
| `layout_split_vertical` | 4 | 4 fatias verticais com caixa de banner centralizada |
| `layout_circular_focus` | 4 | 3 fatias horizontais com imagem circular no centro e banner inferior |
| `layout_diagonal_split` | 2 | 2 imagens com divisão diagonal e texto centralizado |
| `layout_masonry` | 4 | Layout assimétrico estilo masonry com caixa de overlay central |

## Tratamento de Erros

```python
from apps.data_scraping.utils.cover_exceptions import (
    InvalidImageError,           # Imagem inválida
    InsufficientImagesError,     # Não tem imagens suficientes
    LayoutNotFoundError,         # Layout não existe
    MissingAssetError,           # Logo ou fonte faltando
    InvalidConfigError,          # Config inválida
    CoverProductError            # Erro genérico
)

try:
    filepath = cover.generate_cover(layout_name="grid_3x3", name_save="capa")
except InsufficientImagesError:
    print("Não há imagens suficientes")
except LayoutNotFoundError:
    print("Layout inválido")
except Exception as e:
    print(f"Erro: {e}")
```

## Configuração (cover_config.json)

### Acessar Configuração
```python
from apps.data_scraping.utils.cover_product import ConfigLoader

config = ConfigLoader()
layout = config.get_layout("grid_3x3")
font_path = config.get_asset_path("fonts", "title")
default_color = config.get_default("background_color")
```

### Estrutura de Layout em JSON
```json
{
  "meu_layout": {
    "description": "Descrição",
    "min_images": 4,
    "image_count": 4,
    "structure": "custom_4",
    "positions": {
      "0": {
        "size": [0.5, 0.5],           // % do canvas
        "position": [0, 0]             // % do canvas
      }
    }
  }
}
```

## Exemplos de Uso

### Exemplo 1: Simples
```python
cover = CoverProduct("C:\\meu_produto")
path = cover.generate_cover(
    layout_name="grid_3x3",
    name_save="capa1"
)
print(f"Salvo em: {path}")
```

### Exemplo 2: Com Título
```python
path = cover.generate_cover(
    layout_name="faixa_horizontal",
    name_save="promo",
    title="PROMOÇÃO 50%",
    fill=(255, 50, 50),
    font_color="#fff"
)
```

### Exemplo 3: Com Logo
```python
path = cover.cover_full_logo(
    name_save="premium",
    title="Produto Premium",
    company="LEGITIMA"
)
```

### Exemplo 4: Múltiplas Capas
```python
layouts = ["grid_3x3", "grid_5_images", "cover_three"]

for layout in layouts:
    try:
        path = cover.generate_cover(
            layout_name=layout,
            name_save=f"capa_{layout}"
        )
        print(f"✓ {layout}")
    except Exception as e:
        print(f"✗ {layout}: {e}")
```

### Exemplo 5: Adicionar Novo Layout
```json
// Em cover_config.json, adicione:
{
  "layouts": {
    "meu_layout_2x2": {
      "description": "Grid 2x2",
      "min_images": 4,
      "image_count": 4,
      "structure": "custom_4",
      "positions": {
        "0": {"size": [0.5, 0.5], "position": [0, 0]},
        "1": {"size": [0.5, 0.5], "position": [0.5, 0]},
        "2": {"size": [0.5, 0.5], "position": [0, 0.5]},
        "3": {"size": [0.5, 0.5], "position": [0.5, 0.5]}
      }
    }
  }
}
```

Depois use:
```python
path = cover.generate_cover(layout_name="meu_layout_2x2", name_save="capa")
```

### Exemplo 6: Novo Layout - Coluna Vertical
```python
path = cover.layout_coluna_vertical(
    name_save="coluna_test",
    title="MEU PRODUTO",
    fill=(0, 165, 165)  # Turquesa
)
```

### Exemplo 7: Novo Layout - Hero com Thumbnails
```python
path = cover.layout_hero_thumbnails(
    name_save="hero_test",
    title="GRANDE DESTAQUE",
    fill=(255, 100, 50)  # Laranja
)
```

### Exemplo 8: Novo Layout - Grid Translúcido
```python
path = cover.layout_grid_translucido(
    name_save="translucido_test",
    title="COM TRANSPARÊNCIA",
    fill=(0, 0, 255)  # Azul
)
```

### Exemplo 9: Novo Layout - Mosaic Pro
```python
path = cover.layout_mosaic_pro(
    name_save="mosaic_test",
    title="LAYOUT PROFISSIONAL",
    fill=(150, 75, 0)  # Marrom
)
```

### Exemplo 10: Novo Layout - Gallery Clean
```python
path = cover.layout_gallery_clean(
    name_save="gallery_test",
    title="GALERIA LIMPA",
    fill=(255, 165, 0)  # Dourado
)
```

### Exemplo 11: Novo Layout - Split Vertical
```python
path = cover.layout_split_vertical(
    name_save="split_test",
    title="FATIAS VERTICAIS",
    fill=(100, 50, 200)  # Roxo
)
```

### Exemplo 12: Novo Layout - Circular Focus
```python
path = cover.layout_circular_focus(
    name_save="circular_test",
    title="FOCO CIRCULAR",
    fill=(255, 20, 147)  # Rosa profundo
)
```

### Exemplo 13: Novo Layout - Diagonal Split
```python
path = cover.layout_diagonal_split(
    name_save="diagonal_test",
    title="DIAGONAL",
    font_color="#fff"
)
```

### Exemplo 14: Novo Layout - Masonry
```python
path = cover.layout_masonry(
    name_save="masonry_test",
    title="ESTILO\nMASONRY",  # Multi-linha
    fill=(50, 150, 50)  # Verde
)
```

### Exemplo 15: Loop com Novos Layouts
```python
novos_layouts = [
    "layout_coluna_vertical",
    "layout_hero_thumbnails", 
    "layout_grid_translucido",
    "layout_mosaic_pro",
    "layout_gallery_clean",
    "layout_split_vertical",
    "layout_circular_focus",
    "layout_diagonal_split",
    "layout_masonry"
]

cover = CoverProduct("C:\\seu\\produto")

for layout_name in novos_layouts:
    try:
        # Chamar método dinamicamente
        metodo = getattr(cover, layout_name)
        path = metodo(
            name_save=f"capa_{layout_name}",
            title="MINHA CAPA"
        )
        print(f"✓ {layout_name}")
    except Exception as e:
        print(f"✗ {layout_name}: {e}")
```

## Classes Disponíveis

```python
from apps.data_scraping.utils.cover_product import (
    CoverProduct,         # Classe principal
    ConfigLoader,         # Carrega configurações
    FontManager,          # Gerencia fontes
    ImageLoader,          # Carrega imagens
    ImageProcessor,       # Processa imagens
    LayoutEngine,         # Motor de layouts
    CoverRenderer,        # Renderiza canvas
    FileManager           # Gerencia arquivos
)
```

## Propriedades da Instância

```python
cover = CoverProduct("C:\\produto")

# Propriedades disponíveis:
cover.product_path           # Path do produto
cover.size_cover             # Tamanho do canvas
cover.promocao               # É promoção?
cover.images_path            # Path das imagens
cover.save_path              # Path para salvar
cover.available_images       # Lista de imagens válidas

cover.config_loader          # ConfigLoader instance
cover.font_manager           # FontManager instance
cover.image_processor        # ImageProcessor instance
cover.layout_engine          # LayoutEngine instance
cover.renderer               # CoverRenderer instance
cover.file_manager           # FileManager instance
```

## Valores Padrão (cover_config.json)

```json
"defaults": {
  "background_color": [255, 255, 255],
  "font_color": "#000",
  "stroke_color": "#fff",
  "stroke_width": 5,
  "fill_color": null,
  "image_format": "RGB",
  "save_quality": 95,
  "title_max_length": 20
}
```

## Troubleshooting

| Erro | Causa | Solução |
|------|-------|---------|
| `InvalidImageError` | Pasta de fotos não existe | Verifique path do produto |
| `InsufficientImagesError` | Menos imagens que o layout requer | Adicione mais fotos |
| `LayoutNotFoundError` | Layout não existe | Verifique nome do layout |
| `MissingAssetError` | Logo ou fonte não encontrada | Verifique cover_config.json |
| `InvalidConfigError` | JSON inválido | Valide cover_config.json |

## Cores RGB Úteis

```python
# Vermelho
fill=(255, 0, 0)

# Verde
fill=(0, 255, 0)

# Azul
fill=(0, 0, 255)

# Preto
fill=(0, 0, 0)

# Branco
fill=(255, 255, 255)

# Cinza
fill=(128, 128, 128)

# Laranja
fill=(255, 165, 0)

# Rosa
fill=(255, 192, 203)

# Amarelo
fill=(255, 255, 0)
```

## Performance Tips

1. **Cache de Instância**: Reutilize a mesma instância `CoverProduct` para múltiplas capas
2. **Imagens Grandes**: Redimensione as imagens antes se forem muito grandes
3. **Múltiplas Capas**: Use loop em vez de criar instância nova cada vez
4. **Config Custom**: Passe `config_path` se usar configuração customizada

```python
# ✓ Bom
cover = CoverProduct("C:\\produto")
for i in range(10):
    cover.generate_cover(layout_name="grid_3x3", name_save=f"capa_{i}")

# ✗ Ruim
for i in range(10):
    cover = CoverProduct("C:\\produto")  # Cria instância a cada iteração
    cover.generate_cover(layout_name="grid_3x3", name_save=f"capa_{i}")
```

## Documentação Completa

- **README.md** - Documentação técnica detalhada
- **MIGRATION_GUIDE.md** - Guia de migração do código antigo
- **REFACTORING_SUMMARY.md** - Resumo da refatoração
- **cover_config.json** - Arquivo de configuração

## Referência dos Novos Layouts

### layout_coluna_vertical
```python
cover.layout_coluna_vertical(
    name_save="capa",
    title="TÍTULO",
    fill=(0, 165, 165),      # Cor banner lateral
    font_color="#fff"         # Cor do texto
)
```
- **Imagens**: 4 (empilhadas verticalmente)
- **Características**: Banner lateral com texto rotacionado 90°
- **Tamanho canvas**: 1280 x 1920px (proporção 2:3)

### layout_hero_thumbnails
```python
cover.layout_hero_thumbnails(
    name_save="capa",
    title="DESTAQUE",
    fill=(0, 165, 165),
    font_color="#fff"
)
```
- **Imagens**: 4 (1 hero + 3 thumbnails)
- **Características**: Grande imagem no topo, 3 pequenas abaixo com banner no meio
- **Distribuição**: Hero 55% altura, Banner 12%, Thumbs 33%

### layout_grid_translucido
```python
cover.layout_grid_translucido(
    name_save="capa",
    title="TRANSPARÊNCIA",
    fill=(0, 165, 165),
    font_color="#fff"
)
```
- **Imagens**: 4 (grid 2x2)
- **Características**: Grid com faixa translúcida horizontal sobreposição
- **Transparência**: 220 (em escala 0-255)

### layout_mosaic_pro
```python
cover.layout_mosaic_pro(
    name_save="capa",
    title="MOSAIC",
    fill=(0, 165, 165),
    font_color="#fff"
)
```
- **Imagens**: 4 (1 grande + 3 pequenas)
- **Características**: 65% esquerda para grande imagem, 35% direita com 3 empilhadas
- **Badge**: Texto em caixa no canto inferior esquerdo

### layout_gallery_clean
```python
cover.layout_gallery_clean(
    name_save="capa",
    title="GALERIA",
    fill=(0, 165, 165),
    font_color="#fff"
)
```
- **Imagens**: 4 (grid 2x2)
- **Características**: Grid com margens, barra de banner centralizada
- **Margem**: 2% do tamanho total entre imagens e bordas

### layout_split_vertical
```python
cover.layout_split_vertical(
    name_save="capa",
    title="DIVISÃO",
    fill=(0, 165, 165),
    font_color="#fff"
)
```
- **Imagens**: 4 (fatias verticais)
- **Características**: 4 fatias verticais iguais, caixa centralizada com borda branca
- **Caixa**: 70% largura, 18% altura

### layout_circular_focus
```python
cover.layout_circular_focus(
    name_save="capa",
    title="CIRCULAR",
    fill=(0, 165, 165),
    font_color="#fff"
)
```
- **Imagens**: 4 (3 fatias + 1 circular)
- **Características**: 3 faixas horizontais com imagem circular no centro + borda branca
- **Círculo**: Diâmetro 45%, borda 15px branca

### layout_diagonal_split
```python
cover.layout_diagonal_split(
    name_save="capa",
    title="DIAGONAL",
    fill=None,              # Não é usado
    font_color="#fff"
)
```
- **Imagens**: 2 (diagonal split)
- **Características**: 2 imagens separadas por linha diagonal, texto no centro
- **Linha**: 30px cinza, divisão pelo triângulo inferior

### layout_masonry
```python
cover.layout_masonry(
    name_save="capa",
    title="MASONRY",       # ou "LINHA1\nLINHA2" para multi-linha
    fill=(0, 165, 165),
    font_color="#fff"
)
```
- **Imagens**: 4 (blocos assimétricos)
- **Características**: Layout masonry com caixa overlay central
- **Blocos**: 400x600, 600x400, 600x400, 400x600
- **Overlay**: 300x300px quadrado com borda branca 5px

---

**Última atualização**: Janeiro 2026
