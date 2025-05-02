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
        self.type = 'NeuroPlay'
        self.url = "http://127.0.0.1:2336"
        self.order += ['saveFolder', 'filePrefix', 'autoTimestamp']
        self.params['saveFolder'] = {'val': saveFolder, 'valType': 'code', 'updates': 'constant', 'hint': 'Folder to save EEG data'}
        self.params['filePrefix'] = {'val': filePrefix, 'valType': 'code', 'updates': 'constant', 'hint': 'Filename prefix'}
        self.params['autoTimestamp'] = {'val': autoTimestamp, 'valType': 'bool', 'updates': 'constant', 'hint': 'Append timestamp to filename'}

    def writeRoutineStartCode(self, buff):
        buff.writeIndentedLines(f"""
# Start NeuroPlay recording
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
    response = requests.post('{self.url}', json={{"command": "startRecord", "path": full_path}})
    if not response.ok:
        print(f"[NeuroPlay] Failed to start: {{response.text}}")
except Exception as e:
    print(f"[NeuroPlay] Exception: {{e}}")
""")

    def writeRoutineEndCode(self, buff):
        buff.writeIndentedLines(f"""
# Stop NeuroPlay recording
try:
    response = requests.post('{self.url}', json={{"command": "stopRecord"}})
    if not response.ok:
        print(f"[NeuroPlay] Failed to stop: {{response.text}}")
except Exception as e:
    print(f"[NeuroPlay] Exception: {{e}}")
""")
