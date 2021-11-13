from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

class LimpiadorAgent(Agent):
    """ An agent that cleans dirty cells."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def step(self):
        # Revisar si la celda está sucia o limpia.
        pass

class CeldaAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass


class LimpiadoresModel(Model):
    """A model with some number of agents."""
    def __init__(self, N_limpiadores, percentage_dirty: float, max_steps, width, height):
        self.num_agents = N_limpiadores
        self.num_celdas = int(width * height * percentage_dirty)
        self.max_steps = max_steps
        self.current_steps = 0
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True

        # Create Cell agents
        for i in range(self.num_celdas):
            a = CeldaAgent(i, self)
            #self.schedule.add(a) There's no need to activate the 
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        # Create cleaning agents
        for i in range(self.num_agents):
            a = LimpiadorAgent(i, self)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            self.grid.place_agent(a, (1, 1))

    def step(self):
        """ Advance the model by one step"""
        self.schedule.step()
        self.current_steps += 1