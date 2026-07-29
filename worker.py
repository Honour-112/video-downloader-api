from app.jobs import update_job


def process_download(job_id, url, format_id):

    update_job(
        job_id,
        status="downloading",
        progress=10
    )

    # yt-dlp download goes here

    update_job(
        job_id,
        status="finished",
        progress=100
    )