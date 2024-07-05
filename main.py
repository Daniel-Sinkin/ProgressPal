from src.player import Player


def main():
    player = Player("Daniel")
    for rarity in player.pull_rarities(1):
        print(f"Pulled rarity: {rarity}")
        player.habit_journaling(rarity)
        print()
    print(player)

    # Serialize to dictionary
    serialized_data = player.serialize()

    # Serialize to JSON
    json_data = player.to_json()

    # Deserialize from dictionary
    new_player = Player.deserialize(serialized_data)

    # Deserialize from JSON
    another_player = Player.from_json(json_data)

    print(f"{new_player=}")
    print(f"{another_player=}")


if __name__ == "__main__":
    main()
