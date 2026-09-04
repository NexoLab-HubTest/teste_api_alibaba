import pokebase as pb


def buscar_pokemon(nome: str) -> dict:
    """
    Busca um Pokémon na PokéAPI utilizando a biblioteca pokebase
    e normaliza os dados relevantes para o projeto.
    """

    nome = nome.strip().lower()

    if not nome:
        raise ValueError("O nome do Pokémon não pode estar vazio.")

    try:
        pokemon = pb.pokemon(nome)

        tipos = [
            tipo.type.name
            for tipo in pokemon.types
        ]

        habilidades = [
            habilidade.ability.name
            for habilidade in pokemon.abilities
        ]

        stats = {
            stat.stat.name: stat.base_stat
            for stat in pokemon.stats
        }

        dados = {
            "id": pokemon.id,
            "nome": pokemon.name,
            "altura": pokemon.height,
            "peso": pokemon.weight,
            "tipos": tipos,
            "habilidades": habilidades,
            "stats": stats,
        }

        return dados

    except Exception as erro:
        raise RuntimeError(
            f"Não foi possível buscar o Pokémon '{nome}'."
        ) from erro