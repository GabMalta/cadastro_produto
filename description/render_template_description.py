from jinja2 import Environment, FileSystemLoader


def render_template_description(data:dict, desc_gpt=False, promo=False):
    path = r'C:\Users\gabri\OneDrive\Área de Trabalho\PROGRAMACAO\PYTHON\cadastra_produto_bling\description'
    # Carrega os templates do diretório atual
    file_loader = FileSystemLoader(path)
    env = Environment(loader=file_loader)

    # Carrega o template
    template = env.get_template('description.html') if not promo else env.get_template('description_promo.html')

    if desc_gpt:
        with open('./description/desc_gpt.txt', 'r', encoding='utf8') as arq:
            desc_gpt = arq.read()
        data['desc_gpt'] = desc_gpt

    # Renderiza o template com os dados
    return template.render(data)