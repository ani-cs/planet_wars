from agents.planet_wars_agent import PlanetWarsPlayer
from core.game_state import GameState, GameParams, Action, Player

class observing_agent(PlanetWarsPlayer):
    def __init__(self):
        super().__init__()
        self.last_strategy = None  

    def get_agent_type(self) -> str:
        return "Shooty Mc Shoot"

    def get_action(self, game_state: GameState) -> Action:
        my_planets = [p for p in game_state.planets if p.owner == self.player]
        enemy_planets = [p for p in game_state.planets if p.owner != self.player and p.owner != Player.Neutral]
        
        my_total_ships = sum(p.n_ships for p in my_planets)
        enemy_total_ships = sum(p.n_ships for p in enemy_planets)
        
        diff = my_total_ships - enemy_total_ships

        #radius = min(GameParams.height, GameParams.width) * 0.25
        radius = 120
       
    
        if diff > 30:
            strategy = "OFFENSIVE"
        elif diff < -30:
            strategy = "DEFENSIVE"
        else:
            strategy = self.last_strategy if self.last_strategy else "DEFENSIVE"

        
        if strategy != self.last_strategy:
            print(f"[Agent {self.player}] Strategy changed to: {strategy}")
            self.last_strategy = strategy

        
        if strategy == "OFFENSIVE":
            target = None
            #Take my 10 planets with the most ships
            my_planets.sort(key=lambda p: p.n_ships)
            top10_sources = my_planets[:10]
            for s in top10_sources:
                #Look at nearby planets for possible targets
                neighbours = [p for p in game_state.planets if s.position.distance(p.position) < radius]
                for n in neighbours: 
                    #Select target with high growth rate and few ships
                    if n.owner != self.player:
                        if n.owner == Player.Neutral:
                            ships_needed = n.n_ships +1
                            if s.n_ships > ships_needed:
                                if target is None or n.growth_rate/n.n_ships > target.growth_rate/target.n_ships:
                                    target = n
                                    source = s
                                    if n.n_ships is None: num_ships = 25
                                    else: num_ships = ships_needed
                        else:
                            ships_needed = (n.n_ships + n.growth_rate * s.position.distance(n.position))*1.1
                            if s.n_ships > ships_needed:
                                if target is None or n.growth_rate/n.n_ships > target.growth_rate/target.n_ships:
                                    target = n
                                    source = s
                                    if n.n_ships is None: num_ships = s.n_ships *0.7
                                    else: num_ships = ships_needed
            if target is None: return Action.do_nothing()
            return Action(player_id=self.player, source_planet_id=source.id, destination_planet_id=target.id, num_ships=num_ships)

        elif strategy == "DEFENSIVE":
            target = None
            #Sort sources for many ships and high growth rate
            my_planets.sort(key=lambda p: (p.n_ships * p.growth_rate))
            for s in my_planets:
                #Look at nearby planets for possible targets
                neighbours = [p for p in game_state.planets if s.position.distance(p.position) < radius]
                for n in neighbours:
                    #Select target with high growt rate and few ships
                    if n.owner != self.player:
                        if n.owner == Player.Neutral:
                            ships_needed = n.n_ships +1
                            if s.n_ships > ships_needed:
                                if target is None or n.growth_rate/n.n_ships > target.growth_rate/target.n_ships:
                                    target = n
                                    source = s
                                    if n.n_ships is None: num_ships = 25
                                    else: num_ships = ships_needed
                        else:
                            ships_needed = (n.n_ships + n.growth_rate * s.position.distance(n.position))*1.05
                            if s.n_ships > ships_needed:
                                if target is None or n.growth_rate/n.n_ships > target.growth_rate/target.n_ships:
                                    target = n
                                    source = s
                                    if n.n_ships is None: num_ships = s.n_ships *0.7
                                    else: num_ships = ships_needed
                #Always select first source with available targets
                if target is not None:
                    return Action(player_id=self.player, source_planet_id=source.id, destination_planet_id=target.id, num_ships=num_ships)
            return Action.do_nothing()


        return Action.do_nothing()