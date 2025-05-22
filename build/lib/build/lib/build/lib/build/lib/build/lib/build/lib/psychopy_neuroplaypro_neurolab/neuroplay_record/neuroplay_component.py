from pathlib import Path
from psychopy.experiment.components import BaseComponent, Param, getInitVals

WS_OBJ = 'ws_neuro'


class NeuroplayRecordingComponent(BaseComponent):
    categories = ['EEG']
    targets = ['PsychoPy']
    iconFile = Path(__file__).parent / 'classic' / 'icon.png'
    tooltip = 'Mark a period of EEG'
    plugin = "psychopy-neuroplaypro-neurolab"

    def __init__(self, exp, parentName, name='neuroplay_rec'):
        super().__init__(
            exp, parentName, name=name,
            startType='time (s)', startVal=0,
            stopType='duration (s)', stopVal=1,
            startEstim='', durationEstim='',
            saveStartStop=False
        )
        self.type = 'NeuroplayRecording'

        self.exp.requireImport(importName='websocket', importFrom='websocket-client')

        self.params['url'] = Param('ws://localhost:11234', valType='str', inputType='str',
                                   updates='constant', label='WebSocket URL')
        self.params['message'] = Param('TRIGGER', valType='str', inputType='str',
                                       updates='constant', label='Message')

    def writeInitCode(self, buff):
        inits = getInitVals(self.params, 'PsychoPy')
        code = f"{WS_OBJ} = websocket.create_connection({inits['url']})\n"
        buff.writeIndentedLines(code)

    def writeRoutineStartCode(self, buff):
        inits = getInitVals(self.params, 'PsychoPy')
        code = f"{WS_OBJ}.send({inits['message']})\n"
        buff.writeIndentedLines(code)

    def writeExperimentEndCode(self, buff):
        buff.writeIndentedLines(f"try:\n")
        buff.setIndentLevel(1, relative=True)
        buff.writeIndented(f"{WS_OBJ}.close()\n")
        buff.setIndentLevel(-1, relative=True)
        buff.writeIndented("except:\n")
        buff.setIndentLevel(1, relative=True)
        buff.writeIndented("pass\n")
        buff.setIndentLevel(-1, relative=True)

    def writeInitCodeJS(self, buff):
        buff.writeIndentedLines("// NeuroPlayPro not supported in JS\n")

    def writeFrameCode(self, buff): pass
    def writeRoutineEndCode(self, buff): pass
    def writeExperimentEndCodeJS(self, buff): pass
