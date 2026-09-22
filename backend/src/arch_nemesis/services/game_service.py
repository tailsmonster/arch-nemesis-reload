from arch_nemesis.database.repositories import games, messages


def create_game(title: str) -> dict:
    game = games.create_game(title)
    messages.create_message(
        game["id"],
        "system",
        "A fresh Nemesis session begins. Convince the Arch zealot to install Windows.",
    )
    return get_game_detail(game["id"])


def list_games() -> list[dict]:
    return games.list_games()


def get_game_detail(game_id: str) -> dict | None:
    game = games.get_game(game_id)
    if not game:
        return None
    game["messages"] = messages.list_messages_for_game(game_id)
    return game
