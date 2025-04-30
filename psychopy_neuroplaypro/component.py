from psychopy.experiment.components.basecomponent import BaseComponent
import os

class NeuroPlayComponent(BaseComponent):
    categories = ['EEG']
    iconFile = os.path.join(os.path.dirname(__file__), 'resources', 'icon.png')
    
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
        buff.writeIndentedLines(f\"\"\"\n# Start NeuroPlay recording\nimport requests, os, datetime\n\"\"\")
        buff.writeIndentedLines(f\"\"\"\nsave_folder = {self.params['saveFolder']['val']}\nfile_prefix = {self.params['filePrefix']['val']}\nauto_timestamp = {self.params['autoTimestamp']['val']}\nif auto_timestamp:\n    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')\n    filename = f\"{file_prefix}_{{timestamp}}.edf\"\nelse:\n    filename = f\"{file_prefix}.edf\"\nfull_path = os.path.join(save_folder, filename)\n\ntry:\n    os.makedirs(save_folder, exist_ok=True)\n    response = requests.post('{self.url}', json={{\"command\": \"startRecord\", \"path\": full_path}})\n    if not response.ok:\n        print(f\"[NeuroPlay] Failed to start: {{response.text}}\")\nexcept Exception as e:\n    print(f\"[NeuroPlay] Exception: {{e}}\")\n\"\"\")
    
    def writeRoutineEndCode(self, buff):
        buff.writeIndentedLines(f\"\"\"\n# Stop NeuroPlay recording\ntry:\n    response = requests.post('{self.url}', json={{\"command\": \"stopRecord\"}})\n    if not response.ok:\n        print(f\"[NeuroPlay] Failed to stop: {{response.text}}\")\nexcept Exception as e:\n    print(f\"[NeuroPlay] Exception: {{e}}\")\n\"\"\")
