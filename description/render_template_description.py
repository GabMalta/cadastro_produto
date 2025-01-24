from jinja2 import Environment, FileSystemLoader


def render_template_description(data: dict, promo=False):
    path = r"C:\Users\gabri\OneDrive\Área de Trabalho\PROGRAMACAO\PYTHON\cadastra_produto_bling\description"
    # Carrega os templates do diretório atual
    file_loader = FileSystemLoader(path)
    env = Environment(loader=file_loader)

    # Carrega o template
    template = (
        env.get_template("description.html")
        if not promo
        else env.get_template("description_promo.html")
    )

    # Renderiza o template com os dados
    return template.render(data)
