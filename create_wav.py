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


    def int_or_str(text):
        """Helper function for argument parsing."""
        try:
            return int(text)
        except ValueError:
            return text

    # parser = argparse.ArgumentParser(description=__doc__)
    # # parser.add_argument(
    # #     '-l', '--list-devices', action='store_true',
    # #     help='show list of audio devices and exit')
    # # parser.add_argument(
    # #     '-d', '--device', type=int_or_str,
    # #     help='input device (numeric ID or substring)')
    # # parser.add_argument(
    # #     '-r', '--samplerate', type=int, help='sampling rate')
    # # parser.add_argument(
    # #     '-c', '--channels', type=int, default=1, help='number of input channels')
    # # parser.add_argument(
    # #     'filename', nargs='?', metavar='FILENAME',
    # #     help='audio file to store recording ')
    # # parser.add_argument(
    # #     '-t', '--subtype', type=str, help='sound file subtype (e.g. "PCM_24")')
    class Args:
        pass

    args = Args
    args.filename = str(name) + '.wav'

    try:
        import sounddevice as sd
        import soundfile as sf
        import numpy  # Make sure NumPy is loaded before it is used in the callback
        assert numpy  # avoid "imported but unused" message (W0611)

        # if args.list_devices:
        #     print(sd.query_devices())
        #     parser.exit(0)
        # if args.samplerate is None:
        device_info = sd.query_devices(None, 'input')
        #     # soundfile expects an int, sounddevice provides a float:
        samplerate = int(device_info['default_samplerate'])
        # if args.filename is None:
        filename = str(name) + '.wav'
            # args.filename = tempfile.mktemp(prefix=name,
            #                                 suffix='.wav', dir='')
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
    # except Exception as e:
    #     # parser.exit(type(e).__name__ + ': ' + str(e))