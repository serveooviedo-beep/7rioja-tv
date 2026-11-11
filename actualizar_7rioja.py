from pathlib import Path
import subprocess
import sys
from urllib.parse import urlparse

VIDEO_PAGE = 'https://www.dailymotion.com/video/x8dhao1'
OUTPUT = Path(__file__).with_name('7Rioja_master.m3u8')

def extract(fmt):
    cmd = [sys.executable, '-m', 'yt_dlp', '--no-warnings', '--socket-timeout', '15', '--retries', '2', '-g', '-f', fmt, VIDEO_PAGE]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=120)
    urls = [line.strip() for line in result.stdout.splitlines() if line.strip().startswith('https://')]
    if len(urls) != 1 or '.m3u8' not in urlparse(urls[0]).path:
        raise RuntimeError(f'Formato {fmt}: se esperaba una única URL HLS, obtenidas {len(urls)}')
    return urls[0]


def main():
    video = extract('hls-4')
    audio = extract('hls-group_A2-und')
    playlist = ('#EXTM3U\n'
                '#EXT-X-VERSION:6\n'
                '#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="audio",NAME="Espanol",LANGUAGE="es",DEFAULT=YES,AUTOSELECT=YES,URI="' + audio + '"\n'
                '#EXT-X-STREAM-INF:BANDWIDTH=6500000,RESOLUTION=1920x1080,CODECS="avc1.640028,mp4a.40.2",AUDIO="audio"\n'
                + video + '\n')
    OUTPUT.write_text(playlist, encoding='utf-8', newline='\n')
    print(f'Archivo generado: {OUTPUT.name}')

if __name__ == '__main__':
    main()
