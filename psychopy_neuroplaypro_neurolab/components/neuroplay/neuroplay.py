from psychopy.experiment.components.basecomponent import BaseComponent
import os

class NeuroPlayComponent(BaseComponent):
    categories = ['EEG']
    iconFile = os.path.join(os.path.dirname(__file__), 'classic', 'icon.png')

    def __init__(self, exp, parentName, name='neuroplay',
                 saveFolder='data', filePrefix='recording', autoTimestamp=True,
                 startType='time (s)', startVal='0', stopType='duration (s)', stopVal=''):
        super().__init__(exp, parentName, name=name,
                         startType=startType, startVal=startVal,
                         stopType=stopType, stopVal=stopVal)
        self.type = 'neuroplay'
        self.url = "http://127.0.0.1:2336"
        self.order += ['saveFolder', 'filePrefix', 'autoTimestamp']
        self.params['saveFolder'] = {'val': saveFolder, 'valType': 'code', 'updates': 'constant'}
        self.params['filePrefix'] = {'val': filePrefix, 'valType': 'code', 'updates': 'constant'}
        self.params['autoTimestamp'] = {'val': autoTimestamp, 'valType': 'bool', 'updates': 'constant'}

    def writeRoutineStartCode(self, buff):
        buff.writeIndentedLines(f"""
# NeuroPlay START recording
import requests, os, datetime
save_folder = {self.params['saveFolder']['val']}
file_prefix = {self.params['filePrefix']['val']}
auto_timestamp = {self.params['autoTimestamp']['val']}
if auto_timestamp:
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{file_prefix}_{{timestamp}}.edf"
else:
    filename = f"{file_prefix}.edf"
full_path = os.path.join(save_folder, filename)

try:
    os.makedirs(save_folder, exist_ok=True)
    requests.post('{self.url}', json={{"command": "startRecord", "path": full_path}})
except Exception as e:
    print(f"[NeuroPlay] Exception: {{e}}")
""")

    def writeRoutineEndCode(self, buff):
        buff.writeIndentedLines(f"""
# NeuroPlay STOP recording
try:
    requests.post('{self.url}', json={{"command": "stopRecord"}})
except Exception as e:
    print(f"[NeuroPlay] Exception: {{e}}")
""")
