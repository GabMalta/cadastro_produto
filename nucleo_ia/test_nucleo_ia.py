"""
Smoke test do pacote nucleo_ia — unittest puro, SEM Django (prova, na prática, que o pacote não
depende dele: se precisasse rodar via `manage.py test`, essa prova não existiria). Mocka as
chamadas de rede (Claude/Gemini) — não gasta token nem exige as chaves de API configuradas.

Rodar com: python -m unittest nucleo_ia/test_nucleo_ia.py -v
"""
import io
import json
import unittest
from unittest.mock import MagicMock, patch

from PIL import Image

from nucleo_ia import curador_descricao, inspiracao_uso, pesquisa_tecido
from nucleo_ia.render_utils import selo_ilustrativo


def _resposta_claude(texto: str) -> MagicMock:
    """Simula o retorno de `client.messages.create` (mesmo formato usado em agentes/tests.py)."""
    bloco = MagicMock(type="text", text=texto)
    resposta = MagicMock()
    resposta.content = [bloco]
    resposta.stop_reason = "end_turn"
    resposta.usage.input_tokens = 200
    resposta.usage.output_tokens = 80
    resposta.usage.server_tool_use = MagicMock(web_search_requests=2)
    return resposta


def _imagem_sintetica_bytes() -> bytes:
    buf = io.BytesIO()
    Image.new("RGB", (64, 64), (10, 20, 30)).save(buf, format="JPEG")
    return buf.getvalue()


class CuradorDescricaoTests(unittest.TestCase):
    @patch("nucleo_ia.claude_client.client")
    def test_curar_descricao_bloco_metragem_antes_da_copy(self, mock_client):
        texto = json.dumps({
            "titulo": "Tricoline Floral para Patchwork",
            "descricao": "<p>Tecido macio e fácil de costurar.</p>",
            "palavras_chave": ["tricoline", "floral"],
            "tags": ["algodao"],
            "largura": "1,40 m",
        })
        mock_client.messages.create.return_value = _resposta_claude(texto)

        resultado = curador_descricao.curar_descricao(
            codigo="1m-TESTE", nome="Tricoline Floral", contexto="tom de voz de teste",
            categoria="Tecidos", preco="29.90", cores=["Azul", "Rosa"],
        )

        self.assertEqual(resultado["titulo"], "Tricoline Floral para Patchwork")
        self.assertEqual(resultado["palavras_chave"], ["tricoline", "floral"])
        # bloco de metragem vem ANTES da copy
        desc = resultado["descricao"]
        self.assertLess(desc.index("Cada unidade representa"), desc.index("Tecido macio"))
        self.assertIn("1m x 1,40 m", desc)
        self.assertGreater(resultado["custo_usd"], 0)

    @patch("nucleo_ia.claude_client.client")
    def test_curar_descricao_propaga_feedback(self, mock_client):
        texto = json.dumps({
            "titulo": "T", "descricao": "<p>D</p>", "palavras_chave": [], "tags": [], "largura": None,
        })
        mock_client.messages.create.return_value = _resposta_claude(texto)

        curador_descricao.curar_descricao(
            codigo="1m-TESTE", nome="Tricoline Floral", contexto="ctx",
            feedback="encurte o título",
            sugestao_anterior={"titulo": "Título antigo", "palavras_chave": [], "tags": [],
                               "descricao": "<p>Copy antiga.</p>"},
        )
        mensagens = mock_client.messages.create.call_args.kwargs["messages"]
        conteudo = mensagens[0]["content"]
        self.assertIn("encurte o título", conteudo)
        self.assertIn("Título antigo", conteudo)

    def test_sem_bloco_metragem_corta_o_bloco(self):
        bloco = curador_descricao._bloco_metragem("1,50 m")
        descricao = f"{bloco}\n\n<p>Copy de venda.</p>"
        self.assertEqual(curador_descricao.sem_bloco_metragem(descricao), "<p>Copy de venda.</p>")


class InspiracaoUsoTests(unittest.TestCase):
    @patch("nucleo_ia.claude_client.client")
    def test_escrever_prompt_inspiracao_propaga_feedback(self, mock_client):
        texto = json.dumps({
            "prompt": "A dress on a mannequin, no people, no text.",
            "cena": "festa", "justificativa": "Vende o caimento do tecido.",
        })
        mock_client.messages.create.return_value = _resposta_claude(texto)

        resultado = inspiracao_uso.escrever_prompt_inspiracao(
            nome_tecido="Cetim Charmeuse", briefing="Usado em vestidos de festa.",
            contexto="ctx", feedback="menos dourado", prompt_anterior="Prompt anterior aqui",
        )
        self.assertIn("no people", resultado["prompt"])
        self.assertEqual(resultado["cena"], "festa")

        mensagens = mock_client.messages.create.call_args.kwargs["messages"]
        conteudo = mensagens[0]["content"]
        self.assertIn("menos dourado", conteudo)
        self.assertIn("Prompt anterior aqui", conteudo)

    @patch("nucleo_ia.inspiracao_uso.baixar_imagem")
    @patch("nucleo_ia.inspiracao_uso.gerar_imagem")
    def test_gerar_imagem_inspiracao_aplica_selo(self, mock_gerar, mock_baixar):
        mock_baixar.return_value = b"bytes-da-referencia"
        mock_gerar.return_value = _imagem_sintetica_bytes()

        saida = inspiracao_uso.gerar_imagem_inspiracao(
            "prompt de teste", referencia_url="https://exemplo.com/foto.jpg",
        )

        mock_baixar.assert_called_once_with("https://exemplo.com/foto.jpg")
        mock_gerar.assert_called_once()
        # devolve JPEG válido, maior que a imagem original (por causa do selo)
        img = Image.open(io.BytesIO(saida))
        self.assertEqual(img.format, "JPEG")

    @patch("nucleo_ia.inspiracao_uso.baixar_imagem")
    @patch("nucleo_ia.inspiracao_uso.gerar_imagem")
    def test_gerar_imagem_inspiracao_sem_referencia(self, mock_gerar, mock_baixar):
        mock_gerar.return_value = _imagem_sintetica_bytes()
        inspiracao_uso.gerar_imagem_inspiracao("prompt sem referencia")
        mock_baixar.assert_not_called()
        mock_gerar.assert_called_once_with("prompt sem referencia", referencia=None, aspect="1:1")


class PesquisaTecidoTests(unittest.TestCase):
    @patch("nucleo_ia.claude_client.client")
    def test_pesquisar_tecido_devolve_briefing_e_custo(self, mock_client):
        mock_client.messages.create.return_value = _resposta_claude(
            "Cetim charmeuse é um tecido acetinado... Termos de busca: cetim, charmeuse."
        )

        resultado = pesquisa_tecido.pesquisar_tecido(
            nome="Cetim Charmeuse Liso", contexto="glossário de teste",
            categoria="Tecidos", descricao_atual="tecido brilhante",
        )

        self.assertIn("Termos de busca", resultado["briefing"])
        self.assertEqual(resultado["buscas_web"], 2)
        self.assertGreater(resultado["custo_usd"], 0)

        conteudo = mock_client.messages.create.call_args.kwargs["messages"][0]["content"]
        self.assertIn("Cetim Charmeuse Liso", conteudo)
        self.assertIn("Categoria: Tecidos", conteudo)


class RenderUtilsTests(unittest.TestCase):
    def test_selo_ilustrativo_devolve_jpeg_valido(self):
        saida = selo_ilustrativo(_imagem_sintetica_bytes())
        img = Image.open(io.BytesIO(saida))
        self.assertEqual(img.format, "JPEG")


if __name__ == "__main__":
    unittest.main()
