from kicker.agents.neural_net_agent import NeuralNetAgent
from Application import Application

agent = NeuralNetAgent()
app = Application(agent)

app.run()
