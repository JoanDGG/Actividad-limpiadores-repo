from ActividadLimpiadores import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

"""
Description:
Program that configure the visualization of the model CleaningModel and shows on the browser

Autors:
Daniel Garcia Barajas
Joan Daniel Guerrero Garcia
Luis Ignacio Ferro Salinas

Last day of modification:
November 12th, 2021

"""


def agentPortrayal(agent):
    """
    Description: Configure visualization of agents
    Parameters:
    - agent: the agent that will be configured

    Returns: None
    """
    if(agent.type == "Cell"):
        portrayal = {"Shape": "circle",
                    "Filled": "true",
                    "Layer": 0,
                    "Color": "grey",
                    "r": 0.8}
        if not agent.isDirty:
            portrayal["Color"] = "#FFFFFF" # White when its clean
        else:
            portrayal["Color"] = "grey" # Grey when its dirty
    else:
        portrayal = {"Shape": "circle",
                    "Filled": "true",
                    "Layer": 1,
                    "Color": "red",
                    "r": 0.5}
    return portrayal

width = int(input("Número de M espacios (ancho): "))
height = int(input("Número de N espacios (alto): "))
nAgents = int(input("Número de agentes limpiadores: "))
percentageDirty = float(input("Porcentaje de celdas inicialmente sucias (como decimal): "))
steps = int(input("Tiempo máximo de ejecución (en pasos): "))


grid = CanvasGrid(agentPortrayal, width, height, 750, 750)
server = ModularServer(CleaningModel,
                       [grid],
                       "Modelo de limpiadores",
                       {"width": width, "height": height, "nCleaningAgents": nAgents, 
                       "percentageDirty": percentageDirty, "maxSteps": steps})
server.port = 8521 # The default
server.launch()