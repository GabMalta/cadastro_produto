# Políticas — troca, devolução, frete, prazo, pagamento

> Arquivo de contexto carregado pelos agentes (sobretudo atendimento) antes de responder o
> cliente. São as **regras do negócio** — algumas têm **peso legal** (Código de Defesa do
> Consumidor). O agente **não inventa política**: se a resposta não está aqui, **escala pro
> Gabriel** em vez de chutar.
>
> Marcadores: **[definir]** = decisão ainda pendente (não afirmar ao cliente). **[confirmar]** =
> provável, mas Gabriel valida antes de uso em produção.
>
> **Contexto de canal:** hoje a venda acontece na **Shopee** (que tem regras próprias do
> marketplace) e no **WhatsApp**. Estas políticas valem para a **loja própria** (em construção) e
> como referência geral; onde a Shopee mandar diferente, prevalece a regra da Shopee.

## 1. Troca e devolução

### 1.1 Arrependimento (cliente desistiu, sem defeito)

- **Direito garantido por lei:** compra online tem **7 dias corridos** de arrependimento, a
  contar do recebimento (CDC, art. 49). A Legítima **aceita**.
- **Reembolso** do valor do produto.
- **Frete de retorno:** por **conta do cliente** — vale pra arrependimento e qualquer motivo que
  **não seja erro da loja**.
- **Condição:** produto **sem uso**, sem lavagem, sem corte adicional além do que foi vendido, em
  estado de revenda.

### 1.2 Defeito ou erro da loja (produto errado, avaria, tecido com problema)

- A Legítima **assume tudo**: troca ou reembolso, e **paga o frete** de ida e volta.
- Vale quando o problema é da loja: veio tecido errado, com defeito, avariado, metragem a menos.

### 1.3 Corte de tecido

- Venda por metro, corte mínimo de 1 m, só metros inteiros (ver `glossario-produto.md`).
- O corte padrão **não** tira o direito de arrependimento de 7 dias. **[confirmar]** com
  contador/advogado se algum corte especial/sob medida é tratado como personalizado (o que
  mudaria a regra).

### 1.4 Como o agente conduz

- Reconhecer o direito com naturalidade, **sem burocratês** (ver `tom-de-voz.md`).
- Separar claramente: **erro da loja → nós pagamos**; **arrependimento → cliente paga o retorno**.
- Caso duvidoso ou fora do previsto aqui → **escalar pro Gabriel**, não improvisar.

## 2. Frete

- **[definir]** — regra da **loja própria** ainda não decidida (frete grátis acima de X? cliente
  paga sempre? por região?). **Não prometer** valor ou frete grátis até o Gabriel definir.
- Referência do planejamento (PROJETO.md, **não confirmado**): estudar **frete grátis progressivo
  acima de ~R$ 150** pra puxar ticket.
- **Transportadora:** **[definir]** (Correios? transportadora? por CEP?).
- **Cobertura de entrega:** Brasil todo, com força maior no Sul e Sudeste (ver `empresa.md`).

## 3. Prazos

- **Postagem (manuseio):** pedido postado em **até 1 dia útil** após a confirmação do pagamento.
- **Entrega:** prazo de postagem **+** prazo da transportadora conforme CEP. O prazo do
  transporte **[definir]** junto com a transportadora.
- Pedido grande / peça fechada pode ter prazo combinado à parte pelo WhatsApp.

## 4. Pagamento

Formas aceitas:

- **Pix**
- **Cartão de crédito** (parcelado)
- **Boleto** bancário

Condições planejadas para a loja própria (PROJETO.md, **[confirmar]** se já ativas):

- **Pix à vista com ~10% de desconto** sobre o preço cheio.
- **Cartão em até 6x** com parcela mínima configurada.
- **Gateway de pagamento da loja própria: [definir]** (avaliação em curso — Mercado Pago / Asaas /
  Efí, incluindo Pix Parcelado). Não prometer parcelamento específico até definir.

## 5. Resumo rápido (pro agente)

| Situação | Quem paga o frete | O que acontece |
| --- | --- | --- |
| Arrependimento (7 dias, sem defeito) | **Cliente** | Reembolso do produto |
| Defeito / erro da loja | **Loja** | Troca ou reembolso, frete ida e volta |
| Dúvida fora desta tabela | — | **Escalar pro Gabriel** |

- **Postagem:** até **1 dia útil**.
- **Pagamento:** Pix, cartão parcelado, boleto.
- **Frete e prazo de entrega da loja própria:** ainda **[definir]** — não prometer.

---

> ⚠️ Itens **[definir]** não existem como regra ainda — o agente não deve afirmá-los ao cliente.
> Atualizar este arquivo assim que Gabriel fechar frete, transportadora e gateway.
