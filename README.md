# mp3-convert

Mirrors a music library as 320kbps MP3s. FLAC and M4A files are transcoded; MP3s and cover art are copied as-is. Re-running skips files that are already up to date.

## Usage

```
uv run main.py
```

Requires `ffmpeg` on your PATH.
