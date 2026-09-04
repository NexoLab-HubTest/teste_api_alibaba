from services.poke_service import buscar_pokemon
from services.qwen_service import analisar_pokemon


def exibir_dados(dados: dict) -> None:
    """
    Exibe os dados básicos retornados pela PokéAPI.
    """

    print("\n" + "=" * 50)
    print("DADOS OBTIDOS DA POKÉAPI")
    print("=" * 50)

    print(f"ID:          {dados['id']}")
    print(f"Nome:        {dados['nome'].title()}")
    print(f"Altura:      {dados['altura']}")
    print(f"Peso:        {dados['peso']}")
    print(f"Tipos:       {', '.join(dados['tipos'])}")
    print(
        f"Habilidades: {', '.join(dados['habilidades'])}"
    )

    print("\nStats:")

    for nome, valor in dados["stats"].items():
        print(f"  - {nome}: {valor}")


def main() -> None:
    print("=" * 50)
    print("POKÉAPI + QWEN3.8-MAX")
    print("=" * 50)

    nome = input(
        "\nDigite o nome de um Pokémon: "
    ).strip()

    try:
        print("\n[1/2] Consultando PokéAPI...")

        dados = buscar_pokemon(nome)

        exibir_dados(dados)

        print("\n[2/2] Enviando dados ao Qwen3.8-Max...")

        analise = analisar_pokemon(dados)

        print("\n" + "=" * 50)
        print("ANÁLISE DO QWEN")
        print("=" * 50)

        print(analise)

        print("\n" + "=" * 50)
        print("[OK] Fluxo concluído com sucesso.")
        print("=" * 50)

    except Exception as erro:
        print("\n" + "=" * 50)
        print("[ERRO]")
        print("=" * 50)

        print(erro)


if __name__ == "__main__":
    main()