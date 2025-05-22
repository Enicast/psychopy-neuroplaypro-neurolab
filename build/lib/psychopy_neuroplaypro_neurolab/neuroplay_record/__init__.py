from pathlib import Path
from psychopy.experiment.components import BaseComponent, Param, getInitVals

WS_OBJ = 'ws_neuro'

class NeuroplayRecordingComponent(BaseComponent):
    categories = ['EEG']
    targets = ['PsychoPy']
    iconFile = Path(__file__).parent / 'classic' / 'icon.png'
    tooltip = 'Trigger recording in NeuroPlayPro'
    plugin = "psychopy-neuroplaypro-neurolab"

    def __init__(self, exp, parentName, name='neuroplay_rec'):
        super().__init__(exp, parentName, name=name,
                         startType='time (s)', startVal=0,
                         stopType='duration (s)', stopVal=0.1,
                         startEstim='', durationEstim='',
                         saveStartStop=False)
        self.type = 'NeuroplayRecording'
        self.exp.requireImport(importName='websocket', importFrom='websocket-client')
        self.params['url'] = Param('ws://localhost:11234', valType='str', inputType='str',
                                   updates='constant', label='WebSocket URL')
        self.params['message'] = Param('TRIGGER', valType='str', inputType='str',
                                       updates='constant', label='Trigger')

    def writeInitCode(self, buff):
        inits = getInitVals(self.params, 'PsychoPy')
        buff.writeIndentedLines(f"{WS_OBJ} = websocket.create_connection({inits['url']})")

    def writeRoutineStartCode(self, buff):
        inits = getInitVals(self.params, 'PsychoPy')
        buff.writeIndentedLines(f"{WS_OBJ}.send({inits['message']})")

    def writeExperimentEndCode(self, buff):
        buff.writeIndentedLines("try:")
        buff.setIndentLevel(1, True)
        buff.writeIndentedLines(f"{WS_OBJ}.close()")
        buff.setIndentLevel(-1, True)
        buff.writeIndentedLines("except:\n    pass")

    def writeInitCodeJS(self, buff):
        buff.writeIndentedLines("// Not supported in JS")

    def writeFrameCode(self, buff): pass
    def writeRoutineEndCode(self, buff): pass
    def writeExperimentEndCodeJS(self, buff): pass
