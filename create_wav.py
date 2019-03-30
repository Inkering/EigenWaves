#!/usr/bin/env python3
"""Create a recording with arbitrary duration.

PySoundFile (https://github.com/bastibe/PySoundFile/) has to be installed!

"""
import argparse
import tempfile
import queue
import sys
import time

def recordFile(name):

    class Args:
        pass

    args = Args
    args.filename = str(name) + '.wav'

    try:
        import sounddevice as sd
        import soundfile as sf
        import numpy  # Make sure NumPy is loaded before it is used in the callback
        assert numpy  # avoid "imported but unused" message (W0611)

    
        device_info = sd.query_devices(None, 'input')
        #     # soundfile expects an int, sounddevice provides a float:
        samplerate = int(device_info['default_samplerate'])

        filename = str(name) + '.wav'

        q = queue.Queue()

        def callback(indata, frames, time, status):
            """This is called (from a separate thread) for each audio block."""
            if status:
                print(status, file=sys.stderr)
            q.put(indata.copy())

        # Make sure the file is opened before recording anything:
        with sf.SoundFile(filename, mode='x', samplerate=samplerate,
                        channels=1, subtype=None) as file:
            with sd.InputStream(samplerate=samplerate, device=None,
                                channels=1, callback=callback):
                print('#' * 80)
                print('press Ctrl+C to stop the recording')
                print('#' * 80)
                while True:
                    file.write(q.get())

    except KeyboardInterrupt:
        print('\nRecording finished: ' + repr(args.filename))
        time.sleep(.1)
        return 1