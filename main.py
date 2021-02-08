#!/user/bin/env
import tcod

from actions import EscapeAction, MovementAction
from input_handlers import EventHandler


def main() -> None:
    # Variables for screen size
    screen_width = 80
    screen_height = 50

    # Keep track of player's position at all times
    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    # telling tcod which font to use
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler()

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

            # This line tells the program to put the @ symbol on the screen in it's proper place at coordinate [x,y]
            root_console.print(x=player_x, y=player_y, string="@")

            # Context.present updates the screen with what we've told it to display
            context.present(root_console)

            root_console.clear()

            # gives us a way to exit the program by hitting the x button on console's window
            for event in tcod.event.wait():

                action = event_handler.dispatch(event)

                if action is None:
                    continue

                if isinstance(action, MovementAction):
                    player_x += action.dx
                    player_y += action.dy

                elif isinstance(action, EscapeAction):
                    raise SystemExit()


if __name__ == "__main__":
    main()