import requests
import json
from core.senha import CHAT_GPT_TOKEN
import sys, os

sys.path.append(os.path.abspath(os.curdir))

class Descricao():
    def __init__(self,palavra_chave,composicao,qtd_mt,largura):
        self.palavra_chave = palavra_chave
        self.composicao = composicao
        self.qtd_mt = qtd_mt
        self.largura = largura
        
    
    def descricao_referencia():
        with open (fr'.\core\chat_gpt\referencia\descricao.txt', 'r') as desc:
            descricao = desc.read()

        return descricao

    def desc_chatgpt(self,ref=False):
        model = 'gpt-3.5-turbo'
        link = 'https://api.openai.com/v1/chat/completions'
        headers = {"Authorization": f"Bearer {CHAT_GPT_TOKEN}", "Content-Type": "application/json"}

        if ref:
            desc_ref = Descricao.descricao_referencia()
            prosseguir = input('Podemos prosseguir?(s/n)')
            while prosseguir == 'n':
                if prosseguir == 's' or prosseguir == 'S':
                    break
                elif prosseguir == 'n' or prosseguir == 'N':
                    desc_ref = input('Cole aqui novamente a descrição de referencia:')
                    prosseguir = input('Podemos prosseguir?(s/n)')
                else:
                    prosseguir = input('Responda com "s" ou "n" \n Podemos prosseguir?(s/n)')

            
            body_message = {
                'model': model,
                'messages': Descricao.roles(f'Palavra-chave: {self.palavra_chave}, Descrição de referencia: {desc_ref}')
            }

            body_message = json.dumps(body_message)

            requisicao = requests.post(link, headers=headers, data=body_message)
            resposta = requisicao.json()
            descricao = resposta["choices"][0]['message']['content']
            return descricao
        else:
            
            body_message = {
                'model': model,
                'messages': Descricao.roles(f'Palavra-chave: {self.palavra_chave}')
                    }

            body_message = json.dumps(body_message)

            requisicao = requests.post(link, headers=headers, data=body_message)
            resposta = requisicao.json()
            descricao = resposta["choices"][0]['message']['content']
            return descricao
    

    def monta_descricao(self,descricao):
        if type(self.qtd_mt) == list:
            desc_total = []
            for mt in self.qtd_mt:
                info_compra = f'''<p style="text-align: center;">Informações Para Compra:</p>
                                    <p style="text-align: center;"></p>
                                    <p style="text-align: center;">Cada unidade se refere a {mt} metros inteiros do tecido. Exemplo:</p>
                                    <p style="text-align: center;">1und = {mt:,.0f}m x {self.largura}m</p>
                                    <p style="text-align: center;">2und = {mt * 2 :,.0f}m x {self.largura}m</p>
                                    <p style="text-align: center;">3und = {mt * 3 :,.0f}m x {self.largura}m</p>
                                    <p style="text-align: center;"></p>
                                    <p style="text-align: center;">E assim por adiante. Os tecidos serão enviados inteiros sem corte.</p>
                                    <p style="text-align: center;">Não cortamos medidas em centímetros como 3,50m, 4,50m, etc.</p>
                                    <p style="text-align: center;"></p>'''

                info_tec = f'''<p style="text-align: center;">Informações do Tecido:</p>
                <p style="text-align: center;">{self.palavra_chave}</p>
                <p style="text-align: center;">Composição: {self.composicao}</p>
                <p style="text-align: center;">Largura: {self.largura} Metros</p>
                <p style="text-align: center;"></p>
                <p style="text-align: center;"></p>'''

                info_tec = f'''<p style="text-align: center;">Informações do Tecido:</p>
                <p style="text-align: center;">{self.palavra_chave}</p>
                <p style="text-align: center;">Composição: {self.composicao}</p>
                <p style="text-align: center;">Largura: {self.largura} Metros</p>
                <p style="text-align: center;"></p>
                <p style="text-align: center;"></p>'''

                desc = info_compra + info_tec + descricao
                desc_total.append(desc)
        else:
            
            info_compra = f'''<p style="text-align: center;">Informações Para Compra:</p>
            <p style="text-align: center;"></p>
            <p style="text-align: center;">Cada unidade se refere a {self.qtd_mt} metros inteiros do tecido. Exemplo:</p>
            <p style="text-align: center;">1und = {self.qtd_mt}m x {self.largura}m</p>
            <p style="text-align: center;">2und = {self.qtd_mt * 2 :,.0f}m x {self.largura}m</p>
            <p style="text-align: center;">3und = {self.qtd_mt * 3 :,.0f}m x {self.largura}m</p>
            <p style="text-align: center;"></p>
            <p style="text-align: center;">E assim por adiante. Os tecidos serão enviados inteiros sem corte.</p>
            <p style="text-align: center;">Não cortamos medidas em centímetros como 3,50m, 4,50m, etc.</p>
            <p style="text-align: center;"></p>'''

            info_tec = f'''<p style="text-align: center;">Informações do Tecido:</p>
            <p style="text-align: center;">{self.palavra_chave}</p>
            <p style="text-align: center;">Composição: {self.composicao}</p>
            <p style="text-align: center;">Largura: {self.largura} Metros</p>
            <p style="text-align: center;"></p>
            <p style="text-align: center;"></p>'''

            desc_total = info_compra + info_tec + descricao
        
        return desc_total
    def roles(msg):
        role = [
            {'role': 'user', 'content': 'Preciso que otimize algumas descrições de produtos para SEO para mim'},
            {'role': 'assistant', 'content': 'Claro! Ficarei feliz em ajudá-lo a otimizar as descrições dos produtos para SEO. Por favor, forneça as descrições dos produtos que você gostaria de otimizar, juntamente com as palavras-chave ou frases-chave relevantes que você deseja segmentar. Com essas informações, poderei oferecer sugestões específicas e eficazes para otimizar suas descrições de produtos para mecanismos de busca.'},
            {'role': 'user', 'content': 'Trata-se de um tecido 100% poliéster muito utilizado na indústria têxtil, em casas de artesanato, na confecção de uniformes, roupas sociais, toalhas de mesa, decorações diversas, almofadas e também muito utilizado na confecção de cortinas.\n\nConfecção roupas sociais, uniformes em geral, saias, vestidos, coletes, e muitas outras aplicações em vestuário masculino e feminino.\nCapas de almofadas, cortinas, roupa de cama, bandôs, e vários outros artigos de decoração.\nFlores, laços, roupas de bonecos, entre muitas outras aplicações artesanais.\n\nSua aplicação na confecção de produtos é bem vasta, com um pouco de criatividade, pode-se criar qualquer coisa.\nMaterial de alta qualidade e resistência com durabilidade é indeterminada.\n\nPalavra-chave: Tecido Oxfordine Liso'},
            {'role': 'assistant', 'content': 'Aqui estão as descrições otimizadas dos produtos utilizando a palavra-chave "Tecido Oxfordine Liso" para SEO:\nTecido Oxfordine Liso - Ideal para Confecção de Roupas Sociais e Uniformes\nExplore a versatilidade do tecido Oxfordine liso para criar roupas sociais e uniformes de alta qualidade. Com sua composição 100% poliéster, esse tecido é amplamente utilizado na indústria têxtil e oferece durabilidade incomparável. Vista-se com elegância e sofisticação usando esse tecido versátil e resistente.\nTecido Oxfordine Liso - Transforme sua Decoração com Estilo e Praticidade\nDê um toque de classe à sua decoração com o tecido Oxfordine liso. Seja para cortinas, capas de almofadas, roupa de cama ou outros itens decorativos, esse tecido 100% poliéster é a escolha perfeita. Sua alta qualidade e resistência garantem um visual impecável e durabilidade prolongada. Descubra infinitas possibilidades de decoração com esse tecido versátil e elegante.\nTecido Oxfordine Liso - O Favorito dos Artesãos para Projetos Criativos\nDesperte sua criatividade com o tecido Oxfordine liso! Esse material poliéster de alta qualidade é amplamente utilizado em projetos artesanais, como flores, laços e roupas de bonecos. Com o tecido Oxfordine liso, suas criações ganharão vida com durabilidade e resistência excepcionais. Deixe sua imaginação fluir e crie peças únicas e encantadoras com esse tecido versátil.\nEspero que essas descrições otimizadas ajudem a destacar os benefícios e usos do Tecido Oxfordine Liso, aumentando sua visibilidade nos mecanismos de busca.'},
            {'role': 'user', 'content': 'Crie uma variação da primeira opção'},
            {'role': 'assistant', 'content': 'Claro! Aqui está uma variação da primeira opção:\nTecido Oxfordine Liso - Qualidade e Durabilidade para Confecção de Roupas Sociais e Uniformes\nDescubra a excelência do tecido Oxfordine liso para a confecção de roupas sociais e uniformes impecáveis. Composição 100% poliéster, esse tecido é amplamente utilizado na indústria têxtil devido à sua alta qualidade e resistência. Seja na criação de saias, vestidos, coletes ou outras peças de vestuário masculino e feminino, o tecido Oxfordine liso oferece um acabamento elegante e durabilidade indeterminada. Vista-se com estilo e confiança com esse tecido versátil e duradouro.\nEspero que essa variação atenda às suas necessidades!'},
            {'role': 'user', 'content': 'Reescreva a descrição abaixo a otimizando para SEO utilizando como palavra-chave: "Tecido Oxfordine Liso"\n\nO tecido Oxfordine é uma versão mais leve do tecido Oxford. Seu caimento é mais leve e é levemente transparente. É muito usado na linha de camisaria, uniformes, jalecos e até para artesanato. Possui uma ótima durabilidade e excelente custo benefício.\nTrata-se de um tecido 100% poliéster muito utilizado na indústria têxtil, em casas de artesanato, na confecção de uniformes, roupas sociais, toalhas de mesa, decorações diversas, almofadas e também muito utilizado na confecção de cortinas.\n\nConfecção roupas sociais, uniformes em geral, saias, vestidos, coletes, e muitas outras aplicações em vestuário masculino e feminino.\nCapas de almofadas, cortinas, roupa de cama, bandôs, e vários outros artigos de decoração.\nFlores, laços, roupas de bonecos, entre muitas outras aplicações artesanais.\n\nSua aplicação na confecção de produtos é bem vasta, com um pouco de criatividade, pode-se criar qualquer coisa.\nMaterial de alta qualidade e resistência com durabilidade é indeterminada.'},
            {'role': 'assistant', 'content': 'Descubra a versatilidade do Tecido Oxfordine Liso para suas criações!\nO Tecido Oxfordine Liso é a escolha perfeita para diversos projetos na indústria têxtil e artesanato. Com sua composição 100% poliéster, esse tecido leve e levemente transparente é amplamente utilizado na confecção de roupas sociais, uniformes, jalecos, toalhas de mesa, almofadas e até cortinas. Sua aplicação abrange desde vestuário masculino e feminino, como saias, vestidos e coletes, até artigos de decoração, como capas de almofadas, roupa de cama e bandôs.\nAlém disso, o Tecido Oxfordine Liso oferece uma durabilidade excepcional e excelente custo-benefício. Sua alta qualidade e resistência garantem a longevidade das peças confeccionadas. Seja você um profissional da moda ou um entusiasta do artesanato, as possibilidades são infinitas. Deixe sua criatividade fluir e crie produtos únicos e encantadores com esse tecido versátil.\nAproveite toda a versatilidade do Tecido Oxfordine Liso e desfrute de um material de alta qualidade que permite a criação de qualquer coisa que sua imaginação permitir. Experimente esse tecido duradouro e apaixone-se por suas inúmeras aplicações.\nEspero que essa descrição otimizada atenda às suas necessidades de SEO, destacando os benefícios e usos do Tecido Oxfordine Liso.'},
            {'role': 'user', 'content': 'crie uma meta descrição'},
            {'role': 'assistant', 'content': 'Claro! Aqui está uma sugestão de meta descrição otimizada para SEO:\n"Descubra a versatilidade do Tecido Oxfordine Liso, um tecido 100% poliéster amplamente utilizado na indústria têxtil, confecção de roupas sociais, uniformes e decorações. Com alta qualidade, durabilidade e excelente custo-benefício, crie peças únicas e encantadoras para moda e artesanato. Explore suas infinitas aplicações e deixe sua criatividade fluir. Aproveite toda a versatilidade desse tecido versátil e duradouro."\nLembre-se de adaptar essa meta descrição para atender aos requisitos técnicos específicos da plataforma ou website em que você pretende utilizar.'},
            {'role': 'user', 'content': 'É preciso que tenha no máximo 256 caracteres'},
            {'role': 'assistant', 'content': 'Compre Tecido Oxfordine Liso - Versátil, durável e de alta qualidade. Ideal para moda, artesanato e decoração. Crie peças únicas com facilidade. Aproveite agora!'},
            {'role': 'user', 'content': 'melhore um pouco'},
            {'role': 'assistant', 'content': 'Tecido Oxfordine Liso - Versatilidade e qualidade em moda e decoração. Durável, resistente e perfeito para criar peças únicas. Compre agora!'},
            {'role': 'user', 'content': 'mais uma vez'},
            {'role': 'assistant', 'content': 'Tecido Oxfordine Liso - Versatilidade e qualidade para moda e decoração. Durável e resistente, crie peças únicas. Compre agora e deixe sua criatividade fluir!'},
            {'role': 'user', 'content': 'fale sobre como ele pode ser usado'},
            {'role': 'assistant', 'content': 'Descubra a versatilidade do Tecido Oxfordine Liso em suas criações! Ideal para moda e decoração, esse tecido 100% poliéster oferece inúmeras possibilidades. Na moda, pode ser utilizado na confecção de roupas sociais, uniformes, saias, vestidos e coletes, tanto para homens quanto para mulheres. Na decoração, é perfeito para capas de almofadas, cortinas, roupa de cama, bandôs e diversos outros artigos decorativos. Além disso, sua aplicação no artesanato é vasta, permitindo a criação de flores, laços, roupas de bonecos e muito mais. Com sua durabilidade e alta qualidade, o Tecido Oxfordine Liso é o aliado perfeito para transformar suas ideias em realidade. Solte sua criatividade e desfrute de um tecido versátil em todas as suas aplicações. Compre agora e comece a criar peças únicas com o Tecido Oxfordine Liso!'},

        ]

        role.append({'role': 'user', 'content': msg})
        return role

