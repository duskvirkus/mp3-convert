#!/usr/bin/env bash
set -euo pipefail

SRC="/home/dusk/Music/library3/contents"
DST="/home/dusk/Music/library3/contents-mp3"

converted=0
skipped=0
failed=0

find "$SRC" -type f \( -iname "*.mp3" -o -iname "*.flac" -o -iname "*.m4a" \) | sort | while IFS= read -r src; do
    rel="${src#"$SRC"/}"
    dst="$DST/${rel%.*}.mp3"

    if [[ -f "$dst" && "$dst" -nt "$src" ]]; then
        (( skipped++ )) || true
        continue
    fi

    mkdir -p "$(dirname "$dst")"

    case "${src,,}" in
        *.mp3)
            if cp "$src" "$dst"; then
                echo "copied:    $rel"
                (( converted++ )) || true
            else
                echo "FAILED:    $rel" >&2
                (( failed++ )) || true
            fi
            ;;
        *)
            if ffmpeg -i "$src" -codec:a libmp3lame -b:a 320k -map_metadata 0 -y "$dst" -loglevel error 2>&1; then
                echo "converted: $rel"
                (( converted++ )) || true
            else
                echo "FAILED:    $rel" >&2
                rm -f "$dst"
                (( failed++ )) || true
            fi
            ;;
    esac
done

echo ""
echo "done — converted/copied: $converted, skipped: $skipped, failed: $failed"
