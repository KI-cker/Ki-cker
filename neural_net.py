from kicker.agents.neural_net_agent import NeuralNetAgent
from Application import Application, read_config

config = read_config()

randomness = 0.5

if 'randomness' in config:
    randomness = config['randomness']

agent = NeuralNetAgent(randomness=randomness)
app = Application(agent)

app.run()
