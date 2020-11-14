import sys
import os
from subprocess import run
from shutil import make_archive, rmtree

from spleeter import SpleeterError
from utils import config

class BuildTrackError(Exception):
    def __init__(self, stderr):
        self.stderr  = stderr

    def __str__(self):
        return f'BuildTrackError: {str(self.stderr)}'

class RunSpleeter:
    def __init__(self):
        pass

    def startRun(self, file, stems, stemOptions, updateStatus):
        if not file:
            updateStatus('No file given to spleeter', True)
            return

        stemNo = stems.split(' ')[0]

        try:
            updateStatus('Loading Spleeter library')
            from spleeter.separator import Separator
            updateStatus('Creating Spleeter instance')
            separator = Separator(f'spleeter:{stemNo}stems')
            updateStatus('Starting file separation...')
            separator.separate_to_file(str(file).strip(), destination=config['STOREDIR'], filename_format='{filename}/{instrument}.{codec}')
        except SpleeterError as e:
            updateStatus(str(e), True)
            return
        except:
            updateStatus(sys.exc_info()[0], True)
            return

        if stemNo == '2':
            os.rename(f"{config['STOREDIR']}/{file.stem}/accompaniment.wav", f"{config['STOREDIR']}/{file.stem}/other.wav")

        if len(stemOptions[1]):
            try:
                self.buildPartialTracks(file, stemOptions[1], updateStatus)
            except BuildTrackError as e:
                updateStatus(f'Building tracks failed - {str(e)}')
                return
            except FileNotFoundError as e:
                updateStatus(str(e))
                return
            except:
                updateStatus(sys.exc_info()[0], True)
                return

        try:
            updateStatus('Removing extra files')
            self.removeExtraFiles(file, stemOptions)
            updateStatus('Zipping')
            make_archive(f"{config['STOREDIR']}/{file.stem}", 'zip', f"{config['STOREDIR']}/{file.stem}")
            rmtree(f"{config['STOREDIR']}/{file.stem}")
        except:
            updateStatus(sys.exc_info()[0], True)
            return

        updateStatus('DONE')

    def buildPartialTracks(self, file, removeLs, updateStatus):
        updateStatus('Building partial tracks')
        isoTracks = os.listdir(f"{config['STOREDIR']}/{file.stem}")
        for removeStem in removeLs:
            command = ['ffmpeg']
            command.append('-y')
            numInputs = 0
            for iso in isoTracks:
                if iso.split('.')[0] != removeStem:
                    command.append('-i')
                    command.append(f"{config['STOREDIR']}/{file.stem}/{iso}")
                    numInputs += 1
            command.append('-filter_complex')
            command.append(f'amix=inputs={numInputs}:duration=longest')
            command.append(f"{config['STOREDIR']}/{file.stem}/no_{removeStem}.wav")
            out = run(command)
            if out.returncode != 0:
                raise BuildTrackError(out.stdout + out.stderr)

    def removeExtraFiles(self, file, stemOptions):
        keepIso = list(map(lambda x: f'{x}.wav', stemOptions[0]))
        keepRem = list(map(lambda x: f'no_{x}.wav', stemOptions[1]))
        allTracks = os.listdir(f"{config['STOREDIR']}/{file.stem}")
        for t in allTracks:
            if t not in keepIso and t not in keepRem:
                os.remove(f"{config['STOREDIR']}/{file.stem}/{t}")