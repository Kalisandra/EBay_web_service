from celery import Celery
from celery.schedules import crontab

from webapp import create_app
from webapp.favorite_searches import statistic


flask_app = create_app()
celery_app = Celery('tasks', broker='redis://localhost:6379/0')


@celery_app.task
def get_statistic_data():
    with flask_app.app_context():
        statistic.get_item_to_statistic()


@celery_app.task
def final_price_info():
    with flask_app.app_context():
        statistic.get_final_price()


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour='*/1'), get_statistic_data.s())
    sender.add_periodic_task(crontab(hour='*/1'), final_price_info.s())
