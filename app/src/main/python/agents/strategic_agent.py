from agents.planet_wars_agent import PlanetWarsPlayer
from core.game_state import GameState, Action, Player

class strategic_agent(PlanetWarsPlayer):
    def __init__(self):
        super().__init__()
        self.last_strategy = None  

    def get_agent_type(self) -> str:
        return "StrategicAgent"

    def get_action(self, game_state: GameState) -> Action:
        my_planets = [p for p in game_state.planets if p.owner == self.player]
        enemy_planets = [p for p in game_state.planets if p.owner != self.player]
        neutral_planets = [p for p in game_state.planets if p.owner == Player.Neutral]
        
        my_total_ships = sum(p.n_ships for p in my_planets)
        enemy_total_ships = sum(p.n_ships for p in enemy_planets)
        
        diff = my_total_ships - enemy_total_ships
        
        if diff > 15:
            strategy = "OFFENSIVE"
        elif diff < -15:
            strategy = "DEFENSIVE"
        else:
            strategy = self.last_strategy if self.last_strategy else "EXPANSION"

        
        if strategy != self.last_strategy:
            print(f"[Agent {self.player}] Strategy changed to: {strategy}")
            self.last_strategy = strategy

        
        if strategy == "OFFENSIVE":
            target = min(enemy_planets, key=lambda p: p.n_ships) if enemy_planets else None
            source = max(my_planets, key=lambda p: p.n_ships) if my_planets else None
            if target and source and source.n_ships > 10:
                return Action(player_id=self.player, source_planet_id=source.id, 
                              destination_planet_id=target.id, num_ships=int(source.n_ships * 0.5))

        elif strategy == "DEFENSIVE":
            weakest_mine = min(my_planets, key=lambda p: p.n_ships) if my_planets else None
            strongest_mine = max(my_planets, key=lambda p: p.n_ships) if my_planets else None
            if weakest_mine and strongest_mine and strongest_mine.id != weakest_mine.id and strongest_mine.n_ships > 10:
                return Action(player_id=self.player, source_planet_id=strongest_mine.id, 
                              destination_planet_id=weakest_mine.id, num_ships=10)

        elif strategy == "EXPANSION":
            target = min(neutral_planets, key=lambda p: p.n_ships) if neutral_planets else None
            source = max(my_planets, key=lambda p: p.n_ships) if my_planets else None
            if target and source and source.n_ships > 5:
                return Action(player_id=self.player, source_planet_id=source.id, 
                              destination_planet_id=target.id, num_ships=target.n_ships + 1)

        return Action.do_nothing()