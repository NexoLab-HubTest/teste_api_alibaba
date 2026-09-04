import os
import time
import statistics

from openai import OpenAI


WORKSPACE_ID = os.environ["ALIBABA_WORKSPACE_ID"]

client = OpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url=(
        f"https://{WORKSPACE_ID}"
        ".ap-southeast-1.maas.aliyuncs.com"
        "/compatible-mode/v1"
    ),
    timeout=30.0,
)


NUM_TESTES = 10

latencias = []
sucessos = 0
falhas = 0


for numero in range(1, NUM_TESTES + 1):

    inicio = time.perf_counter()

    try:
        response = client.chat.completions.create(
            model="qwen3.8-max",
            messages=[
                {
                    "role": "user",
                    "content": f"Teste {numero}. Responda apenas OK."
                }
            ],
            temperature=0,
            max_tokens=10,
        )

        latencia = time.perf_counter() - inicio

        latencias.append(latencia)
        sucessos += 1

        resposta = response.choices[0].message.content

        print(
            f"[{numero:02}] OK | "
            f"{latencia:.2f}s | "
            f"{resposta}"
        )

    except Exception as erro:

        latencia = time.perf_counter() - inicio
        falhas += 1

        print(
            f"[{numero:02}] FALHA | "
            f"{latencia:.2f}s | "
            f"{erro}"
        )


print("\n========================")
print("RELATÓRIO")
print("========================")

print(f"Chamadas: {NUM_TESTES}")
print(f"Sucessos: {sucessos}")
print(f"Falhas:   {falhas}")

if latencias:
    print(f"Latência mínima: {min(latencias):.2f}s")
    print(f"Latência média:  {statistics.mean(latencias):.2f}s")
    print(f"Latência máxima: {max(latencias):.2f}s")

    if len(latencias) > 1:
        print(
            f"Desvio padrão:   "
            f"{statistics.stdev(latencias):.2f}s"
        )