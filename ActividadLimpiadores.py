from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation

"""
Description:
A program that manages the classes for a model of agents that cleans the grid full of dirty cells.

Autors:
Daniel Garcia Barajas
Joan Daniel Guerrero Garcia
Luis Ignacio Ferro Salinas

Last day of modification:
November 12th, 2021

"""

class CleaningAgent(Agent):
    """ An agent that cleans dirty cells."""
    def __init__(self, uniqueId, model):
        """
        Description: Initialize variables
        Parameters:
        - uniqueId: Represents an unique identificator for the specific agent 
        - model: Represents the model that the agent will follow

        Returns: None
        """
        super().__init__(uniqueId, model)
        self.type = "CleaningAgent"

    def move(self):
        """
        Description: Move the agent to an adyacent cell in the grid
        Parameters:
        - self: Represents the instance of this object

        Returns: None
        """
        possibleSteps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        newPosition = self.random.choice(possibleSteps)
        self.model.grid.move_agent(self, newPosition)

    def step(self):
        """
        Description: Describes the behaviour of the agent in each step
        Parameters:
        - self: Represents the instance of this object

        Returns: None
        """
        # Check if the cell is dirty or not
        presentInCell = self.model.grid.get_cell_list_contents([self.pos])
        if len(presentInCell) > 1:
            agentTypes = [agent.type for agent in presentInCell]
            cellInCell = "Cell" in agentTypes
            if cellInCell:
                cellInCellList = [agent for agent in presentInCell if agent.type == "Cell"]
                if cellInCellList[0].isDirty:
                    cellInCellList[0].isDirty = False
                else:
                    self.move()
            else:
                self.move()
        else:
            self.move()


class CellAgent(Agent):
    """ An agent that represents a dirty cell."""
    def __init__(self, uniqueId, model):
        """
        Description: Initialize variables
        Parameters:
        - uniqueId: Represents an unique identificator for the specific agent 
        - model: Represents the model that the agent will follow

        Returns: None
        """
        super().__init__(uniqueId, model)
        self.type = "Cell"
        self.isDirty = True

    def step(self):
        pass


class CleaningModel(Model):
    """A model with some number of agents."""
    def __init__(self, nCleaningAgents, percentageDirty: float, maxSteps, width, height):
        """
        Description: Initialize variables
        Parameters:
        - nCleaningAgents: Number of cleaning agents in the model
        - percentageDirty: Percentage of the dirty cells in the grid
        - maxSteps: Maximum number of steps that the model will process
        - width: The width of the grid
        - height: The height of the grid

        Returns: None
        """
        self.numAgents = nCleaningAgents
        self.numDirtyCells = int(width * height * percentageDirty)
        print(f"Hay {self.numDirtyCells} celdas sucias")
        self.maxSteps = maxSteps
        self.currentSteps = 0
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.running = True

        # Create Cell agents
        cellsFilled = 0
        cellsId = 0
        while cellsFilled < self.numDirtyCells:
            agent = CellAgent(cellsId, self)
            row = self.random.randrange(self.grid.width)
            col = self.random.randrange(self.grid.height)
            cellListContent = self.grid.get_cell_list_contents([(row, col)])
            agentTypes = [agent.type for agent in cellListContent]
            cellInCell = "Cell" in agentTypes
            if not cellInCell:
                self.grid.place_agent(agent, (row, col))
                cellsFilled += 1
                cellsId += 1
      
        # Create cleaning agents
        for i in range(self.numAgents):
            agent = CleaningAgent(i, self)
            self.schedule.add(agent)
            # Add the agent to a random grid cell
            self.grid.place_agent(agent, (1, 1))

    def step(self):
        """
        Description: Advance the model by one step
        Parameters:
        - self: Represents the instance of this object

        Returns: None
        """
        if (self.currentSteps < self.maxSteps):
            self.schedule.step()
            self.currentSteps += 1
        else:
            print("Ya se llego al numero maximo de pasos")
