#!/user/bin/env
import copy
import traceback

import tcod

import color
import exceptions
import input_handlers
import setup_game


def save_game(handler: input_handlers.BaseEventHandler, filename: str) -> None:
    """If curent event handler has active engine, then save it"""
    if isinstance(handler, input_handlers.EventHandler):
        handler.engine.save_as(filename)
        print("Game saved.")


def main() -> None:
    # Variables for screen size
    screen_width = 80
    screen_height = 50

    # telling tcod which font to use
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    handler: input_handlers.BaseEventHandler = setup_game.MainMenu()

    # Creates the screen with a title
    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="CRAIG'S BASEMENT",
        vsync=True,
    ) as context:

        # Creates our console, which is what we'll be drawing to
        # order argument affects order of x and y variables in numpy (underlying library tcod uses)
        # Numpy accesses 2D arrays in y, x order. Setting at "F", we change this to x, y instead
        root_console = tcod.Console(screen_width, screen_height, order="F")

        # Game loop, a loop that doesn't end until we close the screen
        try:
            while True:
                root_console.clear()
                handler.on_render(console=root_console)
                context.present(root_console)

                try:
                    for event in tcod.event.wait():
                        context.convert_event(event)
                        handler = handler.handle_events(event)
                except Exception:  # handle exceptions in game
                    traceback.print_exc()  # print error
                    # print erro to message log
                    if isinstance(handler, input_handlers.EventHandler):
                        handler.engine.message_log.add_message(
                            traceback.format_exc(), color.error
                        )
        except exceptions.QuitWithoutSaving:
            raise
        except SystemExit:  # save and quit
            save_game(handler, "savegame.sav")
            raise
        except BaseException:  # save on any other unexpected exception
            save_game(handler, "savegame.sav")
            raise


if __name__ == "__main__":
    main()