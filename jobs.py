import uuid
from datetime import datetime

jobs = {}


def create_job():
    job_id = str(uuid.uuid4())

    jobs[job_id] = {
        "status": "queued",
        "progress": 0,
        "file": None,
        "error": None,
        "created": datetime.utcnow()
    }

    return job_id


def get_job(job_id):
    return jobs.get(job_id)


def update_job(job_id, **kwargs):
    if job_id in jobs:
        jobs[job_id].update(kwargs)


def delete_job(job_id):
    if job_id in jobs:
        del jobs[job_id]