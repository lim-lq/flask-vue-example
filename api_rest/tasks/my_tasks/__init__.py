from api_rest.applications import celery_ins


@celery_ins.task()
def add_together(a, b):
    return {
        "result": a + b
    }
