from .views import ManageDB 

def update_db():
    scan_ammount = 3
    Manager = ManageDB()
    scanned_games = Manager.update_map_list_and_winrate(scan_ammount)
    print(f"scanned {scanned_games} ranked games")