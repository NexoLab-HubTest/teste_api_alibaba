import os
import time

from openai import OpenAI


WORKSPACE_ID = os.environ["ALIBABA_WORKSPACE_ID"]
API_KEY = os.environ["DASHSCOPE_API_KEY"]

BASE_URL = (
    f"https://{WORKSPACE_ID}"
    ".ap-southeast-1.maas.aliyuncs.com"
    "/compatible-mode/v1"
)


client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
    timeout=30.0,
)


inicio = time.perf_counter()

try:
    response = client.chat.completions.create(
        model="qwen3.8-max",
        messages=[
            {
                "role": "system",
                "content": "Você está executando um teste de conectividade."
            },
            {
                "role": "user",
                "content": "Responda apenas COMUNICACAO_OK."
            },
        ],
        temperature=0,
        max_tokens=30,
    )

    duracao = time.perf_counter() - inicio

    print("\n=== TESTE QWEN ===")
    print("Status: OK")
    print(f"Latência: {duracao:.2f} s")
    print(f"Modelo: {response.model}")

    print("\nResposta:")
    print(response.choices[0].message.content)

    if response.usage:
        print("\nTokens:")
        print(f"  Input:  {response.usage.prompt_tokens}")
        print(f"  Output: {response.usage.completion_tokens}")
        print(f"  Total:  {response.usage.total_tokens}")

except Exception as erro:
    duracao = time.perf_counter() - inicio

    print("\n=== TESTE QWEN ===")
    print("Status: FALHA")
    print(f"Tempo até falha: {duracao:.2f} s")
    print(f"Tipo: {type(erro).__name__}")
    print(f"Erro: {erro}")