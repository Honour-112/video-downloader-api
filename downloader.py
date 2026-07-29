import os
import uuid
import yt_dlp

def get_video_info(url: str):
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "extract_flat": False,
    }

def download_video(url: str, format_id: str):

    download_id = str(uuid.uuid4())

    output = f"app/downloads/{download_id}.%(ext)s"

    ydl_opts = {
        "format": format_id,
        "outtmpl": output,
        "merge_output_format": "mp4",
        "noplaylist": True,
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        ydl.download([url])

        info = ydl.extract_info(url, download=False)

        filename = ydl.prepare_filename(info)

        if filename.endswith(".webm"):
            filename = filename[:-5] + ".mp4"

        return filename

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    formats = []

    for f in info.get("formats", []):
        if not f.get("format_id"):
            continue

        formats.append({
            "format_id": f.get("format_id"),
            "quality": f.get("format_note") or f.get("height"),
            "height": f.get("height"),
            "ext": f.get("ext"),
            "filesize": f.get("filesize"),
            "fps": f.get("fps"),
            "vcodec": f.get("vcodec"),
            "acodec": f.get("acodec"),
        })

    return {
        "title": info.get("title"),
        "uploader": info.get("uploader"),
        "thumbnail": info.get("thumbnail"),
        "duration": info.get("duration"),
        "formats": formats
    }