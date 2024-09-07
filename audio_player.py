import platform
from pathlib import Path
import pyaudio
from pydub import AudioSegment
import click
import threading
import time

CHUNK = 1024


class AudioPlayer:
    def __init__(self, filename):
        self.filename = filename
        self.audio = AudioSegment.from_mp3(filename)
        self.paused = False
        self.position = 0
        self.playing = False

    def play(self):
        self.playing = True
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(self.audio.sample_width),
                        channels=self.audio.channels,
                        rate=self.audio.frame_rate,
                        output=True)

        while self.position < len(self.audio) and self.playing:
            if not self.paused:
                chunk = self.audio[self.position:self.position+CHUNK]
                stream.write(chunk.raw_data)
                self.position += CHUNK
            else:
                time.sleep(0.1)

        stream.stop_stream()
        stream.close()
        p.terminate()

    def pause(self):
        self.paused = not self.paused

    def stop(self):
        self.playing = False


def set_path_to_ffmpeg(platform_name):
    if platform_name == 'Darwin':  # macOS
        return "ffmpeg"  # this will use the system-installed ffmpeg
    elif platform_name == 'Windows':
        return str(Path(__file__).parent / "win" / "ffmpeg" / "ffmpeg.exe")
    else:
        return str(Path(__file__).parent / "linux" / "ffmpeg" / "ffmpeg")


@click.group()
def cli():
    pass


@cli.command()
@click.argument('filename', type=click.Path(exists=True))
def play(filename):
    player = AudioPlayer(filename)
    click.echo(f"Playing {filename}")
    click.echo("Commands: p (pause/resume), q (quit)")

    threading.Thread(target=player.play, daemon=True).start()

    while True:
        command = click.prompt("Enter command")
        if command == 'p':
            player.pause()
            click.echo("Paused" if player.paused else "Resumed")
        elif command == 'q':
            player.stop()
            click.echo("Quitting")
            break
        else:
            click.echo("Unknown command")


def main():
    PLATFORM_NAME = platform.system()
    PATH_TO_FFMPEG = set_path_to_ffmpeg(PLATFORM_NAME)
    AudioSegment.converter = PATH_TO_FFMPEG
    cli()


if __name__ == "__main__":
    main()
