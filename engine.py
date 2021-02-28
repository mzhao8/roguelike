# responsible for drawing the map

from typing import Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov


from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler


class Engine:
    # takes 4 args: entities, event handler, game map, and player
    # entities is a set (of entities), which behaves kind of like a list that enforces uniqueness. That is, we can’t add an Entity to the set twice, whereas a list would allow that. In our case, having an entity in entities twice doesn’t make sense. Moved to gamemap
    # event handler is the same event_handler that we used in main.py. It will handle our events.
    # player is the player Entity. We have a separate reference to it outside of entities for ease of access. We’ll need to access player a lot more than a random entity in entities.
    def __init__(
        self,
        event_handler: EventHandler,
        game_map: GameMap,
        player: Entity,
    ):
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        self.update_fov()

    def handle_enemy_turns(self) -> None:
        for entity in self.game_map.entities - {self.player}:
            print(f"The {entity.name} wonders when it will get a real turn.")

    # pass events through and iterate through them
    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(
                self, self.player
            )  # passing Engine to the action, providing it context to do what we want
            self.handle_enemy_turns()
            self.update_fov()  # Update the FOV before the players next action

    def update_fov(self) -> None:
        """
        Recompute the visible area based on the players point of view.
        """
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        # If a tile is 'visible' it should be added to 'explored
        self.game_map.explored |= self.game_map.visible

    # handles drawing our screen. iterate through self.entities, and print them in their proper locations, present the context, and clear the console
    def render(self, console: Console, context: Context) -> None:
        # game map render method draws it onto the screen
        self.game_map.render(console)

        context.present(console)

        console.clear()
