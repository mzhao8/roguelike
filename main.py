#!/user/bin/env
import copy

import tcod

from engine import Engine
import entity_factories
from procgen import generate_dungeon


def main() -> None:
    # Variables for screen size
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    max_monsters_per_room = 2

    # telling tcod which font to use
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player=player)

    engine.game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        max_monsters_per_room=max_monsters_per_room,
        engine=engine,
    )

    engine.update_fov()

    # Creates the screen with a title
    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True,
    ) as context:

        # Creates our console, which is what we'll be drawing to
        # order argument affects order of x and y variables in numpy (underlying library tcod uses)
        # Numpy accesses 2D arrays in y, x order. Setting at "F", we change this to x, y instead
        root_console = tcod.Console(screen_width, screen_height, order="F")

        # Game loop, a loop that doesn't end until we close the screen
        while True:

            engine.render(console=root_console, context=context)

            engine.event_handler.handle_events()


if __name__ == "__main__":
    main()