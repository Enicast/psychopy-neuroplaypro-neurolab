from psychopy.plugins import Plugin
from psychopy.experiment.components import registerComponent
from psychopy_neuroplay.component import NeuroPlayComponent

class NeuroPlayPlugin(Plugin):
    def onLoad(self):
        registerComponent("NeuroPlay", NeuroPlayComponent)
        print("✅ NeuroPlay plugin loaded")
