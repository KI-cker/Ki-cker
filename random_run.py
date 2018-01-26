from kicker.agents import RandomAgent
from Application import Application

agent = RandomAgent()
app = Application(agent)

app.run()