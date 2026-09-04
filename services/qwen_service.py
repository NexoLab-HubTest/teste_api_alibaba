import json
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


WORKSPACE_ID = os.getenv("ALIBABA_WORKSPACE_ID")
API_KEY = os.getenv("DASHSCOPE_API_KEY")


def _criar_cliente() -> OpenAI:
    """
    Cria e configura o cliente do Alibaba Cloud Model Studio.
    """

    if not WORKSPACE_ID:
        raise RuntimeError(
            "ALIBABA_WORKSPACE_ID não foi definido."
        )

    if not API_KEY:
        raise RuntimeError(
            "DASHSCOPE_API_KEY não foi definida."
        )

    base_url = (
        f"https://{WORKSPACE_ID}"
        ".ap-southeast-1.maas.aliyuncs.com"
        "/compatible-mode/v1"
    )

    return OpenAI(
        api_key=API_KEY,
        base_url=base_url,
        timeout=30.0,
    )


def analisar_pokemon(dados_pokemon: dict) -> str:
    """
    Envia os dados obtidos pela PokéAPI para o Qwen3.8-Max
    e solicita uma análise simples.
    """

    cliente = _criar_cliente()

    dados_json = json.dumps(
        dados_pokemon,
        ensure_ascii=False,
        indent=2,
    )

    prompt = f"""
Você recebeu dados de um Pokémon obtidos diretamente da PokéAPI.

Dados:

{dados_json}

Faça uma análise curta em português brasileiro.

Organize a resposta nas seguintes seções:

1. Resumo
2. Características principais
3. Pontos fortes
4. Possíveis limitações
5. Curiosidade ou comentário final

Não invente atributos numéricos que não estejam presentes nos dados.
Utilize os dados fornecidos como fonte principal da análise.
"""

    resposta = cliente.chat.completions.create(
        model="qwen3.8-max",
        messages=[
            {
                "role": "system",
                "content": (
                    "Você é um assistente que interpreta "
                    "dados estruturados sobre Pokémon."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.3,
        max_tokens=600,
    )

    conteudo = resposta.choices[0].message.content

    if not conteudo:
        raise RuntimeError(
            "O Qwen retornou uma resposta vazia."
        )

    return conteudo.strip()