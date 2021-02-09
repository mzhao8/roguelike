# responsible for drawing the map

from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console


from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler


class Engine:
    # takes 3 args: entities, event handler, and player
    # entities is a set (of entities), which behaves kind of like a list that enforces uniqueness. That is, we can’t add an Entity to the set twice, whereas a list would allow that. In our case, having an entity in entities twice doesn’t make sense.
    # event handler is the same event_handler that we used in main.py. It will handle our events.
    # player is the player Entity. We have a separate reference to it outside of entities for ease of access. We’ll need to access player a lot more than a random entity in entities.
    def __init__(
        self,
        entities: Set[Entity],
        event_handler: EventHandler,
        game_map: GameMap,
        player: Entity,
    ):
        self.entities = entities
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player

    # pass events through and iterate through them
    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue
            action.perform(self, self.player)

    # handles drawing our screen. iterate through self.entities, and print them in their proper locations, present the context, and clear the console
    def render(self, console: Console, context: Context) -> None:
        # game map render method draws it onto the screen
        self.game_map.render(console)
        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)

        console.clear()
