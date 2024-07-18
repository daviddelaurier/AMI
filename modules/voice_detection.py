import argparse
import sys
import struct
import wave
from threading import Thread
import pvcobra
from pvrecorder import PvRecorder


class VadStream(Thread):
    """
    AMI Voice Activity Detection Engine.
    """

    def __init__(
            self,
            library_path,
            access_key,
            output_path=None,
            input_device_index=None):
        """
        Constructor.

        :param library_path: Library path
        :param access_key: API Key
        :param output_path: Recording output path
        :param input_device_index: Select Input Device
        """

        super(VadStream, self).__init__()

        self._library_path = library_path
        self._access_key = access_key
        self._input_device_index = input_device_index
        self._output_path = output_path

    def run(self):
        """
         Creates an input audio stream, instantiates VAD engine, and monitors the audio stream for
         voice activity.
         """

        recorder = None
        wav_file = None

        try:
            cobra = pvcobra.create(access_key=self._access_key, library_path=self._library_path)
        except pvcobra.CobraInvalidArgumentError as e:
            print(e)
            raise e
        except pvcobra.CobraActivationError as e:
            print("API Key activation error")
            raise e
        except pvcobra.CobraActivationLimitError as e:
            print("API Key '%s' has reached it's rate limit" % self._access_key)
            raise e
        except pvcobra.CobraActivationRefusedError as e:
            print("API Key '%s' refused" % self._access_key)
            raise e
        except pvcobra.CobraActivationThrottledError as e:
            print("API Key '%s' has been throttled" % self._access_key)
            raise e
        except pvcobra.CobraError as e:
            print("Failed to initialize VAD engine")
            raise e

        print("VAD engine version: %s" % cobra.version)

        try:
            recorder = PvRecorder(frame_length=512, device_index=self._input_device_index)
            recorder.start()

            if self._output_path is not None:
                wav_file = wave.open(self._output_path, "w")
                wav_file.setparams((1, 2, 16000, 512, "NONE", "NONE"))

            print("VAD engine is active, listening for voice activity...")
            while True:
                pcm = recorder.read()

                if wav_file is not None:
                    wav_file.writeframes(struct.pack("h" * len(pcm), *pcm))

                voice_probability = cobra.process(pcm)
                percentage = voice_probability * 100
                bar_length = int((percentage / 10) * 3)
                empty_length = 30 - bar_length
                sys.stdout.write("\r[%3d]|%s%s|" % (
                    percentage, '█' * bar_length, ' ' * empty_length))
                sys.stdout.flush()

        except KeyboardInterrupt:
            print('Keyboard interruption detected, VAD engine is stopping...')
        finally:
            if cobra is not None:
                cobra.delete()

            if wav_file is not None:
                wav_file.close()

            if recorder is not None:
                recorder.delete()

    @classmethod
    def show_available_devices(cls):
        devices = PvRecorder.get_available_devices()
        for i in range(len(devices)):
            print('index: %d, device name: %s' % (i, devices[i]))


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--access_key',
        help='API Key')

    parser.add_argument(
        '--library_path',
        help='Absolute path to dynamic library. Default: using the library provided by `pvcobra`')

    parser.add_argument('--audio_device_index', help='Index of input audio device.', type=int, default=-1)

    parser.add_argument('--output_path', help='Absolute path to recorded audio for debugging.', default=None)

    parser.add_argument('--show_audio_devices', action='store_true')

    args = parser.parse_args()

    if args.show_audio_devices:
        VadStream.show_available_devices()
    else:
        if args.access_key is None:
            print("Missing API Key (--access_key)")
        else:
            VadStream(
                library_path=args.library_path,
                access_key=args.access_key,
                output_path=args.output_path,
                input_device_index=args.audio_device_index).run()


if __name__ == '__main__':
    main()