from celery import shared_task # type: ignore
from celery.utils.log import get_task_logger # type: ignore


logger = get_task_logger(__name__)

#function to update the brawlers played and their winrate on current ranked maps.
@shared_task
def update_db(ammount_of_battlelogs):
    from picks_manager.views import ManageDB, CleaningDB
    m,c = ManageDB(), CleaningDB()
    logger.info("Updating the database")
    games_checked = m.update_map_list_and_winrate(ammount_of_battlelogs)
    logger.info("{} games have been checked".format(games_checked))
    # m.update_modes()
    # c.clean_up_the_maps()
    return