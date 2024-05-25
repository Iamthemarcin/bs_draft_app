import os 
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'power_draft.settings')
app = Celery("power_draft")
app.config_from_object("django.conf:settings", namespace = "CELERY")


#function to update the brawlers played and their winrate on current ranked maps.
@app.task
def update_db(ammount_of_battlelogs):
    from picks_manager.views import ManageDB
    m = ManageDB()
    m.update_map_list_and_winrate(ammount_of_battlelogs)
    print('hello?')
    return

app.autodiscover_tasks()