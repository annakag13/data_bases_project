from connect import *
from crud import *


database = 'benglish.db'
current_user_role = "guest"
current_user = ""

def login():
    global current_user_role, current_user
    username = input("Enter username: ")
    password = input("Enter password: ")

    q = {
        "table": 'USER',
        "field": [
            "password", "role"
        ],
        "where": [
            ("username", "=", "?"),
            ("password", "=", "?")
        ],
        "order": None
    }
    res = readSQL(database, read(q), (username, password))

    if len(res) > 0 :
        (pw, role) = res[0]
        current_user_role = role
        current_user = username
    else:
        print('wrong credentions; not logged in!')

    return None


def logout():
    global current_user_role, current_user
    current_user_role = "guest"
    current_user = ""
    return None


def create_user():
    global current_user_role
    if current_user_role != "admin":
        print('you can not...')
        return None
    
    username = input("Enter username of new roster_admin: ")
    existing = readSQL(database, "SELECT username FROM USER WHERE username = ?", (username, ))
    if len(existing) > 0:
        print('username exists')
        return 0
    
    password = input("Enter password of new roster_admin: ")

    new_user = {
        "table": 'USER',
        "field": [
            "username", "password", "role"
        ],
        "value": [
            "?", "?", "?"
        ]
    }
    writeSQL(database, insert(new_user), (username, password, 'roster_admin'))
    return 1

def delete_user():
    global current_user_role
    if current_user_role != "admin":
        print('you can not...')
        return None
    
    username = input("Enter username of roster_admin to delete: ")

    usr = {
        "table": 'USER',
        "where": [
            ('username', '=', "?")
        ]
    }
    writeSQL(database, delete(usr), (username, ))
    return 1

def change_password():
    global current_user
    password = input("Enter new password (DO NOT FORGET): ")
    set_pass = {
        "table": "USER",
        "set": [ ('password', '?') ],
        "where": [( 'username', '=', '?') ]
    }
    writeSQL(database, update(set_pass), (password, current_user))
    return 1

def create_player( tps_id ):
    print("\n create new player!")
    non_free_shirts = readSQL(database, '''
        SELECT pl.shirt_number, pl.name
        FROM PLAYER pl
        LEFT JOIN TEAM_PLAYER tp ON tp.id_player = pl.id_player
        WHERE tp.id_team_per_season = ?
        ''', (tps_id, ))
    non_free = []
    for (shirt, nam) in non_free_shirts:
        non_free.append(f"{shirt}")
    name = input("Player name: ")
    last = input("last name: ")
    birth = input("birthday (yyyy-mm-dd): ")
    natio = input("Nationality (* = Ellada): ")
    pos = input("position: (* = mesos) ")
    print(f"non available shirts: {', '.join(non_free)}")
    shirt_num = input("shirt number: ")
    if natio == '*':
        natio = 'Ελλάδα'
    if pos == "*":
        pos = 'μέσος'
    
    max_id_player = readSQL(database, 'SELECT id_player, name FROM PLAYER ORDER BY id_player DESC LIMIT 1')
    (max_id, nam) = max_id_player[0]

    ins = {
        "table": "PLAYER",
        "field": ["id_player", "name", "lastname", "birthday", "nationality", "position", "shirt_number"],
        "value": [ '?', '?', '?', '?', '?', '?', '?' ]
    }
    writeSQL(database, insert(ins), (max_id+1, name, last, birth, natio, pos, shirt_num))
    return max_id+1


def set_player_to_roster():
    global current_user_role

    if current_user_role == "guest":
        print('you can not...')
        return None
    
    season = readSQL(database, "SELECT id_season, year, start, end FROM SEASON")
    for (sid, year, st, end) in season:
        print(f"id: {sid} ({year})")
    season_id = input("Select Season ID: ")

    teams = readSQL(database, '''
        SELECT tps.id_team_per_season, c.name FROM CLUB c
        LEFT JOIN TEAM_PER_SEASON tps ON tps.EPO_id = c.EPO_id
        WHERE tps.id_season = ? 
        ''', (season_id, ))

    for (tps_id, club) in teams:
        print(f"id: {tps_id} ({club})")
    team_id = input("Select Team id: ")
  
    id_player = create_player(team_id)

    selected_start = ''
    selected_end = ''
    for (sid, yr, start, end) in season:
        if int(season_id) == sid:
            selected_start = start
            selected_end = end

    ins = {
        "table": "TEAM_PLAYER",
        "field": ["id_player", "id_team_per_season", "start_date", "end_date"],
        "value": ['?', '?', '?', '?' ]
    }
    writeSQL(database, insert(ins), (id_player, team_id, selected_start, selected_end))
    
    return None


# NOTE:
# RUN ONCE (on app instalation)

# closeDatabase(database)
def install():

    # create user table
    userTable = {
        "table": 'USER',
        "field": [
            ("username", "varchar(30)", True, "''", None),
            ("password", "varchar(30)", True, "'15asd!k.jhef@HABFJWYEF'", None),
            ("role", "varchar(30)", True, "''", 'CHECK("role" in ("admin","roster_admin"))')
        ],
        "primary": ["username"],
        "constraint": None
    }
    sql = create(userTable)
    writeSQL(database, sql)

    # insert default administrator
    admin = {
        "table": "USER",
        "field": ['username', 'password', 'role'],
        "value": [ '?', '?', '?' ]
    }
    writeSQL(database, insert(admin), ('Admin', '12345', 'admin'))

## instal()

def main():
    inp = main_menu()

    while inp != 0:
        if inp == 99:
            if current_user_role == 'guest':
                login()
            else:
                logout()

        elif inp == 21:
            create_user()

        elif inp == 22:
            delete_user()

        elif inp == 20:
            change_password()
        
        elif inp == 10:
            set_player_to_roster()
        
        inp = main_menu()
    
    print('Bye!')

def main_menu():
    print('choose what to do')
    print(' 0. Exit')
    print(' 1. Check roster')
    print(' ...')
    print(' 7. Statistika')
    
    if current_user_role != 'guest':
        print(' 10. insert player to roster')
        print(' 20. change password')

    if current_user_role == 'admin':
        print(' 21. create user')
        print(' 22. delete user')

    if current_user_role == 'guest':
        print(' 99. Login')
    else:
        print(' 99. Logout')
    
    selection = input("Enter selection: ")
    valid = ['1', '2', '3', '4', '10', '20', '21', '22', '99', '0' ]
    if not selection in valid:
        print(f"{selection} is not a valid choice")
        selection = main_menu()

    return int(selection)



main()