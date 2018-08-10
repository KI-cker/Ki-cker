from kicker.agents import KeyboardAgent
from Application import Application

agent = KeyboardAgent()
app = Application(agent)

app.run()
