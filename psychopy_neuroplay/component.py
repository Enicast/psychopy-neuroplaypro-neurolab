from psychopy.experiment.components.base import BaseComponent

class NeuroPlayComponent(BaseComponent):
    def __init__(self, exp, parentName, name='NeuroPlay'):
        super().__init__(exp, parentName, name)
        self.type = 'NeuroPlay'
        self.url = 'http://localhost:2336'
        self.params = {}

    def writeRoutineStartCode(self, buff):
        buff.writeIndented("# Start NeuroPlay\n")

    def writeRoutineEndCode(self, buff):
        buff.writeIndented("# Stop NeuroPlay\n")
