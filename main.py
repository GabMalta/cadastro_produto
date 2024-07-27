from apps.bling_api.produto import Produto
from apps.data_scraping.import_images import import_images

imported_product = import_images('AQUARELA', r'https://aquarelatecidos.com/Cama,%20Mesa%20e%20Banho/9880%20-%20Percal%20Estampado%20200%20Fios/index.html', 'PERCAL ESTAMPADO 200 FIOS', r'D:\SITE LEGITIMA TEXTIL\EXTRAIDOS AUTOMATICO\NOVA EXTRACAO')

cover_path = imported_product['cover_directory']
pictures_path = imported_product['pictures_directory']

produto = Produto(
    cover_path,
    pictures_path,
    'Tecido Percal 200 Fios Estampado',
    'Percal 200 Fios Estampado',
    'A9880',
    47.59
)

nome = 'Tecido Percal 200 Fios Estampado'
largura_tec = '2,50'
metragens = [3, 6, 10, 12, 15]
codigo = 'A9880'
preco = [128.24, 249.19, 408.90, 489.90, 609.90]
peso = [0.5, 1, 1.4, 1.6, 1.8]
largura = [7, 7, 7, 10, 10]
altura = [7, 7, 7, 7, 10]
profundidade = [7, 7, 10, 7, 10]

anuncios = []
for i, mt in enumerate(metragens):
    anuncio = {
        'titulo': f'{mt} Metros {nome} ({mt}m x {largura_tec}m)',
        'codigo': f'{mt}m-{codigo}',
        'preco': preco[i],
        'peso': peso[i],
        'largura': largura[i],
        'altura': altura[i],
        'profundidade': profundidade[i]
    }
    anuncios.append(anuncio)

for i,anuncio in enumerate(anuncios):
    produto.name = anuncio['titulo']
    produto.code = anuncio['codigo']
    produto.price = anuncio['preco']
    produto.weight = anuncio['peso']
    produto.larg = anuncio['largura']
    produto.alt - anuncio['altura']
    produto.profun = anuncio['profundidade']
    
    product = produto.upload_product(changed_name=False)
    
    id_deposito = 10610809064
    id_products = [data['id'] for data in product['variations']]
    
    produto.add_estoque(id_deposito, id_products, 100)

