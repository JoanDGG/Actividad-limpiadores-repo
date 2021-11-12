from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

class LimpiadorAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class CeldaAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class LimpiadoresModel(Model):
    """A model with some number of agents."""
    def __init__(self, N_limpiadores, N_celdas, width, height):
        self.num_agents = N_limpiadores
        self.num_celdas = N_celdas
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True

        # Create agents
        for i in range(self.num_agents):
            a = CeldaAgent(i, self)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        # Create agents
        for i in range(self.num_agents):
            a = LimpiadorAgent(i, self)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            self.grid.place_agent(a, (1, 1))