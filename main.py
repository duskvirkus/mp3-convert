import shutil
import subprocess
from pathlib import Path

SRC = Path("/home/dusk/Music/library3/contents")
DST = Path("/home/dusk/Music/library3/contents-mp3")

AUDIO_EXTS = {".mp3", ".flac", ".m4a"}
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif"}

converted = 0
skipped = 0
failed = 0

for src in sorted(SRC.rglob("*")):
    if not src.is_file() or src.suffix.lower() not in AUDIO_EXTS | IMAGE_EXTS:
        continue

    rel = src.relative_to(SRC)
    is_image = src.suffix.lower() in IMAGE_EXTS
    dst = DST / rel if is_image else DST / rel.with_suffix(".mp3")

    if dst.exists() and dst.stat().st_mtime > src.stat().st_mtime:
        skipped += 1
        continue

    dst.parent.mkdir(parents=True, exist_ok=True)

    if is_image or src.suffix.lower() == ".mp3":
        shutil.copy2(src, dst)
        print(f"copied:    {rel}")
        converted += 1
    else:
        result = subprocess.run(
            [
                "ffmpeg", "-i", str(src),
                "-codec:a", "libmp3lame",
                "-b:a", "320k",
                "-map", "0",
                "-map_metadata", "0",
                "-codec:v", "copy",
                "-y", str(dst),
                "-loglevel", "error",
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"converted: {rel}")
            converted += 1
        else:
            print(f"FAILED:    {rel}")
            if result.stderr:
                print(f"           {result.stderr.strip()}")
            dst.unlink(missing_ok=True)
            failed += 1

print(f"\ndone — converted/copied: {converted}, skipped: {skipped}, failed: {failed}")
