from ActividadLimpiadores import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

def agent_portrayal(agent):

    if(agent.type == "Celda"):
        portrayal = {"Shape": "circle",
                    "Filled": "true",
                    "Layer": 0,
                    "Color": "grey",
                    "r": 0.8}
        if not agent.is_dirty: #Negro cuando están sucios
            print("celda limpia")
            portrayal["Color"] = "#FFFFFF" #Blanco al limpiarse
        else:
            portrayal["Color"] = "grey" #Blanco al limpiarse

    else:
        portrayal = {"Shape": "circle",
                    "Filled": "true",
                    "Layer": 1,
                    "Color": "red",
                    "r": 0.5}


    return portrayal

ancho = 50
alto = 50
n_agents = 20
percentage_dirty = 0.8
steps = 500

grid = CanvasGrid(agent_portrayal, ancho, alto, 750, 750)
server = ModularServer(LimpiadoresModel,
                       [grid],
                       "Modelo de limpiadore",
                       {"width":ancho, "height":alto, "N_limpiadores": n_agents, 
                       "percentage_dirty": percentage_dirty, "max_steps": steps})
server.port = 8521 # The default
server.launch()