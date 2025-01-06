import random
from pprint import pprint

from connect import *
from combos import *
from match_events import *
from match_dates import *

# setup
number_of_teams = 36
number_of_players = 18
database = 'benglish.db'


first = [
    'Γιώργος', 'Ηλίας', 'Αποστόλης','Δημήτρης', 'Λευτέρης', 'Φάνης','Ξενοφών', 
    'Λεωνίδας', 'Λέων', 'Μάριος', 'Νίκος', 'Τάκης','Πίπης', 'Μάνος', 'Πέτρος', 
    'Κωνσταντίνος', 'Ίωνας','Ανδρέας', 'Προκόπης', 'Γιάννης', 'Χρόνης', 'Θανάσης',
    'Χαρούλης','Τρίφωνας', 'Παύλος', 'Σπύρος', 'Παύλος', 'Γαβριήλ', 'Σαμουήλ', 
    'Τζώρτης', 'Μπάμπης', 'Λάμπης', 'Τόνυ', 'Μίκης', 'Σάκης', 'Γεώργιος', 'Κώστας', 'Πάρις',
    'Τζίμης', 'Φαίδωνας', 'Λάμπρος', 'Στάθης', 'Φίλιππος', 'Άρης', 'Αριστείδης', 'Όμηρος',
    'Οδυσσέας', 'Θέμης', 'Θεμιστοκλής', 'Περικλής', 'Άλκης', 'Ιάσσωνας', 'Ορφέας', 'Δημοσθένης',
    'Μαρίνος', 'Θάνος', 'Μανούσος', 'Μάρκελος', 'Μίλτος', 'Πρίαμος','Ίκαρος', 'Νότης', 'Άγης', 
    'Προκόπης', 'Ζήνωνας', 'Σώτος', 'Στέλιος', 'Λουκάς', 'Παντελής', 'Νεκτάριος', 'Άκης', 
    'Ζάχος', 'Ζαχαρίας', 'Ηρακλής', 'Ιούλιος', 'Στράτος', 'Στρατής', 'Παυσανίας', 'Ανέστης', 
    'Μάρκος', 'Πλάτωνας', 'Άγγελος','Γιάννης', 'Κώστας', 'Δημήτρης', 'Αλέξανδρος', 'Παναγιώτης', 
    'Ανδρέας', 'Στέφανος','Αναστάσιος',  'Βασίλειος',  'Χαράλαμπος',  'Εμμανουήλ',  'Σπυρίδων', 
    'Ιωάννης','Πέτρος','Γιάννης','Γιάννης','Γιάννης','Γιάννης','Γιώργος','Γιώργος','Γιώργος',
    'Δημήτρης','Δημήτρης','Δημήτρης','Ανδρέας','Ανδρέας','Κώστας','Κώστας'
];
last = [
    'Γιατζόγλου', 'Δημητρίου', 'Ιωάννου', 'Παπαπέτρου', 'Σταματίου','Αράπογλου', 'Πεχλιβάνογλου',
    'Αποστόλου', 'Βασιλείου', 'Κυπριανού', 'Χριστοδούλου', 'Τσακάλωφ', 'Σαράφογλου', 'Αγγελόγλου', 
    'Χατζηιωάννου', 'Χατζηδημητρίου', 'Χατζηχριστοδούλου', 'Χατζηαποστόλου','Κόντογλου', 'Εμμανουήλ',
    'Χατζηβασιλείου', 'Παπασταματίου', 'Παπαιωάννου', 'Παπαδημητρίου', 'Σπύρου', 'Παπασπύρου',
    'Παπαποστόλου', 'Παπαβασιλείου', 'Κωνσταντίνου', 'Παπακωνσταντίνου', 'Χατζησπύρου',
    'Αθανασίου', 'Παπαθανασίου', 'Αλεξίου', 'Χατζηαλεξίου', 'Ευσταθίου','Καλύμνου', 'Μάρκου', 
    'Χατζηευσταθίου', 'Προκοπίου', 'Σωτηρίου', 'Παπασωτηρίου', 'Ντυνάν','Χατζημάρκου', 'Θησέου', 
    'Πολυχρονίου', 'Στεργίου', 'Σακελλαρίου', 'Φωτίου', 'Χάτζι','Ραφαήλ', 'Πλάτωνος',
    'Οικονόμου', 'Παπαοικονόμου', 'Ελευθερίου', 'Χατζηελευθερίου', 'Σιμεών',  'Στάνκογλου',
    'Ιωσήφ', 'Μιχαήλ', 'Ιακώβου', 'Ναθαναήλ', 'Ματθαίου', 'Χατζηματθαίου', 'Παπαδόπουλος', 
    'Σίγμα', 'Κάππας', 'Γαβριήλ','Γεωργίου', 'Χατζηγεωργίου', 'Παπαγεωργίου', 'Χατζηνικολάου',
    'Παπαμιχαήλ','Γαβρίλογλου', 'Καραμανώφ', 'Χατζηιακώβου','Τριανταφύλλου', 'Γρηγορίου', 'Χατζηφωτίου',
    'Καραγεωργίου', 'Σωτηρίου', 'Αντωνίου', 'Παπαχρήστου', 'Δημητρίου', 'Παπαδόπουλος', 'Νικολάου','Σταματόπουλος',
    'Αναστασίου','Μακρής', 'Κωνσταντίνου','Παπαδημητρίου', 'Αθανασίου', 'Παναγιωτόπουλος','Διαμαντόπουλος',
    'Καραγιάννης','Παπαδόπουλος', 'Μακρής','Παπαδόπουλος', 'Ιωάννου', 'Δημητρίου', 'Μιχαηλίδης', 'Αναγνωστόπουλος',
    'Παπακωνσταντίνου','Γεωργίου','Κυριακίδης', 'Αλεξίου', 'Παπαδόπουλος', 'Σταματόπουλος', 'Αναστασίου', 'Μακρής',
    'Κωνσταντίνου','Παπαδημητρίου','Παπαδόπουλος', 'Αθανασίου', 'Παναγιωτόπουλος', 'Διαμαντόπουλος','Καραγιάννης',
    'Παπαδόπουλος','Ιωάννου','Δημητρίου','Μιχαηλίδης', 'Αναγνωστόπουλος','Μενδρινός', 'Ιωαννίδης', 'Καγιάφας',
    'Κωσταντέλιας', 'Λιάβας', 'Μπουζούκης', 'Χατζηγιοβάνης', 'Τζόλης', 'Καίσαρης', 'Ιωάνου', 'Οικονόμου', 'Ευαγγέλου'
];
mid = [
    'Εμμ', 'Τζο', 'Νώε', 'Διο', 'Ενι', 'Αμι', 'Αμο', 'Βασ', 'Κλέων', 'Λέων', 'Ζώης',
    'Ιω.', 'Γεω', 'Στεφ', 'Προ', 'Λευτ', 'Ευκ', 'Δημ', 'Μιχ', 'Τολ',
    'Emm', 'Joe', 'Noe', 'Jul', 'Eni', 'Ami', 'Amo', 'Dio', 'Bas', 'Cle', 'Dos', 'Eni',
    'Fri', 'Oli', 'Nic', 'Joe', 'Kim', 'Los', 'Mae', 'Faz', 'Foo', 'Man', 'Zion', 'Son',
    'Bo', 'Kim', 'Leo', 'Andy', 'Ed', 'Lan', 'Wan', 'Emo', 'Doe', 'Xio', 'Cis', 'Not', 'Nor',
    'Faw', 'Geo', 'Glow', 'So', 'Spy', 'Pi', 'Noe', 'Dr', 'Nate', 'Sam', 'Da', 'Nio',
    'Ent', 'For', 'Zen', 'Sa', 'Cre', 'Piu', 'Xor', 'Nom', 'St', 'Jr', 'Mr', 'Sir',
    'Abr', 'Abs', 'And', 'Any', 'Klo', 'Par', 'Froy'
];
deprecated_team = [
    'Παναχαϊκή',
    'Ατρόμητος Πατρών',
    'Θύελλα Πατρών',
    'Δόξα Παραλίας',
    'Αναγέννηση Πατρών',
    'Απόλλων Εγλυκάδας',
    'ΑΕ Αρόης',
    'Πανμοβριακός Ριόλου',
    'Αχαϊκή',
    'Διαγόρας Βραχνεΐκων',
    'Αστέρας Τσουκαλεΐκων',
    'Πείρος Ισώματος',
    'ΑΟ Δρεπάνου',
    'Παραλιακός',
    'ΑΕ Ροϊτίκων',
    'ΑΟ Σαραβαλίου',
    'ΑΟ Ζαβλανίου',
    'ΑΟ Καστριτσίου',
    'ΑΟ Μιντιλογλίου',
    'ΑΟ Ρίου',
    'Αντιριακός'
    'ΑΟ Αγυιάς',
    'ΑΟ Βραχνέικων',
    'ΑΟ Κάτω Ανατολικός',
    'ΑΟ Παραλίας',
    'ΑΟ Ριόλου',
    'ΑΟ Εγλυκάδας',
    'ΑΟ Αρόης',
    'ΑΟ Ισώματος',
    'ΑΟ Δρεπάνου',
    'ΑΟ Πάτρας',
    'ΑΟ Ροϊτίκων',
    'ΑΟ Σαραβαλίου',
    'ΑΟ Ζαβλανίου',
    'ΑΟ Καστριτσίου',
    'ΑΟ Μιντιλογλίου',
    'Έπος Αγυιάς',
    'Κεραυνός Βραχνέικων',
    'Άνω Ανατολικός',
    'Αγάπη Παραλίας',
    'Δύναμη Ριόλου',
    'Λύκοι Εγλυκάδας',
    'Πολεμιστές Αρόης',
    'Νέα Θύελα Ραφήνας',
    'Τϋχη Δρεπάνου',
    'Φίλοι Πάτρας',
    'Τσακάλια Ροϊτίκων',
    'Λατρεία Σαραβαλίου',
];
area = [
    'Αθήνα', 'Εξάρχεια', 'Νέα Φιλαδέλφια', 'Πειραιάς', 'Νέος Κόσμος', 'Περιστέρι',
    'Καλλιθέα', 'Φάληρο', 'Ζωγράφου', 'Δροσιά Αττικής', 'Πικέρμι', 'Ραφήνα',
    'Σούνιο', 'Νέα Σμύρνη', 'Νέα Ιωνία', 'Ελούντα Κρήτης', 'Μικρολίμανο', 'Αθήνα',
    'Πλατεία Βικτωρίας', 'Δραπετσώνα', 'Ίλιον', 'Ρέντης', 'Ιλλύσια', 'Καισαριανή',
    'Κηφισιά', 'Μοσχάτο', 'Πετράλωνα', 'Άγιος Νικόλαος Αττικής', 'Πατήσια',
    'Μοναστηράκι', 'Θησείο', 'Σεπόλια', 'Θεσσαλονίνη', 'Λαδάδικα Θεσσαλονίκης',
    'Τούμπα', 'Αμπελόκηποι Θεσσαλονίκης', 'Αμπελόκηποι Αττικής', 'Λουτράκι',
    'Μενεμένη', 'Νεάπολη Θεσσαλονίκης', 'Χαριλάου, Θεσσαλονίκη', 'Καλαμαριά',
    'Πανόραμα Θεσσαλονίκης', 'Πάτρα', 'Ηράκλειο Κρήτης', 'Άγιος Νικόλας Λασιθίου',
    'Δράμα', 'Καλαμάτα', 'Σπάρτη', 'Ρέθυμνο', 'Τρίκαλα', 'Βόλος', 'Καβάλα',
    'Τρίπολη', 'Πύργος Ηλίας', 'Ρόδος', 'Κως', 'Τήνος', 'Γλυφάδα', 'Βούλα', 'Αθήνα',
    'Κόρινθος', 'Αλεξανδρούπολη', 'Ναύπλιο', 'Ιωάννινα', 'Άρτα', 'Κέρκυρα',
    'Ζάκυνθος', 'Αιγάλεω', 'Χαλάνδρι', 'Μαρούσι', 'Νίκαια', 'Ελευσίνα', 'Αίγιο',
    'Αγρίνιο', 'Μεσολόγγι', 'Νεάπολη Λακωνίας', 'Χανιά', 'Σητεία', 'Σάμος',
    'Ξάνθη', 'Σέρρες', 'Βέροια', 'Κατερίνη', 'Καρδίτσα', 'Λάρισα', 'Λέσβος',
    'Νάξος', 'Άργος', 'Σαντορίνη', 'Αθήνα', 'Θεσσαλονίνη', 'Λάρισσα', 'Φιρά',
    'Ντράφι', 'Ρίο', 'Χαλκίδα', 'Θήβα', 'Λούτσα'
];
position = [
    "αμυντικός","αμυντικός",
    "μέσος","μέσος",
    "επιθετικός"
]
nationality = [
    'Ελλάδα', 'Ελλάδα', 'Ελλάδα',
    'Σερβία', 'Ελλάδα',
    'Κύπρος', 'Αλβανία',  'Ελλάδα',
    'Ελλάδα', 'Ελλάδα', 'Κύπρος',
    'Νιγηρία', 'Ελλάδα'
]

shirt = [
    ['01', "τερματοφύλακας"], ['02', "αμυντικός"],['03', "αμυντικός"],
    ['04', "αμυντικός"], ['05', "αμυντικός"], ['06', "μέσος"], ['07', "μέσος"],
    ['08', "μέσος"], ['09', "μέσος"],['10', "επιθετικός"],['11', "επιθετικός"],
    ['12', "αμυντικός"],['13', "μέσος"],['14', "επιθετικός"],['15', "τερματοφύλακας"],
    ['16', ""],['17', ""],['18', ""],['19', ""],['20', ""],['21', ""],['22', ""],
    ['23', ""],['24', ""],
]
"""
pos_yellow_card = [
    0,0,1,1,0,0,0,0,0
    ]
pos_red_card = [
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
    ]
"""
    
def randItem(list):
    return list[ random.randint(0, len(list)-1) ]


def randDate(): # yyyy-mm-dd
    y = str(random.randint(1992, 2006))
    m = random.randint(1,12)
    if m<10:
        ms = '0'+ str(m)
    else:
        ms = str(m)
    d = random.randint(1,28)
    if d<10:
        ds = '0'+ str(d)
    else:
        ds = str(d)

    return y +'-'+ ms +'-'+ ds

def player(index, team_id):
    name = randItem(first)
    lastname = randItem(last)
    birthday = randDate()
    height = str(random.randint(145,204)/100)
    pos = shirt[index][1]
    if pos == "":
        pos = randItem(position)

    return {
        "id_player": (team_id+1) * 20 + index,
        "name": name,
        "lastname": lastname,
        "birthday": birthday,
        "nationality": randItem(nationality),
        "shirt_number": shirt[index][0],
        "height": height,
        "position": pos
    }

clubs = []

def create_types():
    # card 
    writeSQL(database, '''
            INSERT INTO CARD (id_card, type)
            VALUES (?, ?), (?, ?);
        ''', (1, "κίτρινη", 2, "κόκκινη")
    )
    # goal types
    writeSQL(database, '''
            INSERT INTO GOAL (id_goal, type)
            VALUES (?, ?), (?, ?);
        ''', (1, "γκολ_υπέρ", 2, "αυτογκόλ")
    )

teamsSql = readSQL(database,'''
    SELECT
        tps.id_team_per_season, tps.EPO_id,
        c.name, c.city,
        s.start, s.end
        FROM TEAM_PER_SEASON AS tps
        LEFT JOIN CLUB c ON c.EPO_id = tps.EPO_id
        LEFT JOIN SEASON s ON s.id_season = tps.id_season
    ''')

seas = [
    (0, ''),
    (1, '2023-09-01'),
    (2, '2024-09-04'),
    (3, '2025-09-02')
]

goalH = [0,1,1,1,1,2,2,2,2,3,3,3,4,4,5]
goalG = [0,0,1,1,1,1,1,1,2,2,2,2,3,3,4]


substitutes_per_match = 3

champ = []
for i in range(24, 36):
   row = teamsSql[i] 
   champ.append(row)
   print(row)

def create_schedule(season_id, league_id):
    writeSQL(database, '''
        DELETE FROM MATCHWEEK WHERE id_season = ? AND id_league = ?
        ''', (season_id, league_id)
    )
    min_mw = (season_id * 10 + league_id) * 100 -1
    max_mw = (season_id * 10 + league_id) * 100 + 99
    writeSQL(database, '''
        DELETE FROM MATCH WHERE id_matchweek > ? AND id_matchweek < ?
        ''', (min_mw, max_mw)
    )

    matchweeks = schedule_champ(champ)
    round = 0
    for mw in matchweeks:
        round = round + 1
        id_matchweek = (season_id * 10 + league_id) * 100 + round
        weekdates = matchdays_of_round(seas[season_id][1], round)
        writeSQL(database, '''
            INSERT INTO MATCHWEEK(
                 id_matchweek, round, id_season, id_league,
                 start_date, end_date
            ) VALUES (?, ?, ?, ?, ?, ?)
            ''',(
                id_matchweek,
                round,
                season_id,
                league_id,
                weekdates[0],
                weekdates[1]
            ))
        gmi = 0
        for gm in mw:
            gmi = gmi +1
            ref0 = randItem(first)+ " "+ randItem(last);
            ref1 = randItem(first)+ " "+ randItem(last);
            ref2 = randItem(first)+ " "+ randItem(last);
            id_match = id_matchweek * 10 + gmi
            writeSQL(database, '''
                INSERT INTO MATCH (id_match, id_matchweek, match_date, match_time,
                    id_team_home, id_team_guest,
                    referee, assistant_referee1, assistant_referee2 )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',(
                    id_match,
                    id_matchweek,
                    weekdates[0],
                    '16:00',
                    gm[0], gm[1],
                    ref0, ref1, ref2
                ))


def create_team_players():  # fill PLAYER and TEAM_PLAYER tables
    for ti in range(0, number_of_teams):    # from ARENA
        players = []

        for i in range(0, number_of_players):
            plr = player(i, teamsSql[ti][0])
            writeSQL(database,'''
                INSERT INTO PLAYER (
                    "id_player",
                    "name",
                    "lastname",
                    "birthday",
                    "nationality",
                    "shirt_number",
                    "height",
                    "position"
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                plr["id_player"],
                plr["name"],
                plr["lastname"],
                plr["birthday"],
                plr["nationality"],
                plr["shirt_number"],
                plr["height"],
                plr["position"]
            ))
            players.append(plr);

        clubs.append({
            "id_team_per_season": teamsSql[ti][0],
            "name": teamsSql[ti][2],
            "players": players,
            "start_date": teamsSql[ti][4],
            "end_date": teamsSql[ti][5],
        })
        for p in players:
            writeSQL(database,'''
                INSERT INTO TEAM_PLAYER (
                    id_team_per_season,
                    id_player,
                    start_date,
                    end_date
                    ) VALUES (?, ?, ?, ?)
                ''', (
                        teamsSql[ti][0],
                        p["id_player"],
                        teamsSql[ti][4],
                        teamsSql[ti][5]
                )
            )

    #pprint(clubs)

def playersOfTeam(id_tps, round):  # id_team_per_season

    validPlayersSQL_Round1 = '''
        SELECT 
            tp.id_player, p.position
        FROM TEAM_PLAYER tp
        LEFT JOIN PLAYER p ON p.id_player = tp.id_player
        WHERE tp.id_team_per_season = ?
    '''
    validPlayersSQL = '''
        SELECT 
            tp.id_player, p.position
        FROM TEAM_PLAYER tp
        LEFT JOIN PLAYER p ON p.id_player = tp.id_player
        WHERE tp.id_team_per_season = ?
        AND tp.id_player NOT IN ( -- players witn red card in the prev round
            SELECT tp.id_player
            FROM TEAM_PLAYER tp
            LEFT JOIN PLAYER_PARTICIPATION pp ON pp.id_player = tp.id_player
            LEFT JOIN MATCH m ON m.id_match = pp.id_match
            LEFT JOIN MATCHWEEK mw ON mw.id_matchweek = m.id_matchweek
            LEFT JOIN PLAYER_CARD pc ON pc.id_player = tp.id_player AND pc.id_match = m.id_match
            WHERE (m.id_team_home = ? OR m.id_team_guest = ?)
            AND mw.round = ?    -- (round - 1)
            AND pc.id_card = ?  -- type = 2 = red-card
        )
    '''

    if round == 1:
        return readSQL(database, validPlayersSQL_Round1, (id_tps, ))
    else:
        return readSQL(database, validPlayersSQL, (id_tps, id_tps, id_tps, round-1, 2))


def run_matches(season, league, round):
    mw_id = (season * 10 + league) * 100 + round
    print('Matchweek:', mw_id)
    roundMatches = readSQL(database, '''
        SELECT id_team_home, id_team_guest
        FROM MATCH WHERE id_matchweek = ?
        ''', (mw_id, ))
    idxi = 0
    for match in roundMatches:
        
        homePlayers = playersOfTeam(match[0],round)
        guestPlayers = playersOfTeam(match[1],round)
        
        goalsHome = randItem(goalH)
        goalsGuest = randItem(goalG)

        idxi = idxi + 1
        id_match = mw_id * 10 + idxi
        #print(id_match)
        home_p_and_cards = participation_and_cards(homePlayers)
        away_p_and_cards = participation_and_cards(guestPlayers)
        goals_per_match = goal_achivers(home_p_and_cards["part_tbl"], away_p_and_cards["part_tbl"], goalsHome, goalsGuest)
    
    
        for i in range(0,len(home_p_and_cards["part_tbl"])) :
            id_p = home_p_and_cards["part_tbl"][i][0]
            id_participation = id_match * 1000 + id_p
            
            
            writeSQL(database, '''
                INSERT INTO PARTICIPATION (id_participation,minute_in,minute_out
                     )
                VALUES (?, ?, ?)
                ''',(
                    id_participation,
                    home_p_and_cards["part_tbl"][i][1],
                    home_p_and_cards["part_tbl"][i][2]
                ))
            
            
            writeSQL(database, '''
                INSERT INTO PLAYER_PARTICIPATION (id_match,id_player,id_participation
                     )
                VALUES (?, ?, ?)
                ''',(
                    id_match,
                    id_p,
                    id_participation
                ))
            
        for i in range(0,len(home_p_and_cards["cards"])) :
            
            writeSQL(database, '''
                INSERT INTO PLAYER_CARD (id_match,id_player,id_card,minute
                     )
                VALUES (?, ?, ?, ?)
                ''',(
                    id_match,
                    home_p_and_cards["cards"][i][0],
                    home_p_and_cards["cards"][i][1],
                    home_p_and_cards["cards"][i][2]
                ))
            

        for i in range(0,len(away_p_and_cards["part_tbl"])) :
            id_p = away_p_and_cards["part_tbl"][i][0]
            id_participation = id_match * 1000 + id_p
            
            
            writeSQL(database, '''
                INSERT INTO PARTICIPATION (id_participation,minute_in,minute_out
                     )
                VALUES (?, ?, ?)
                ''',(
                    id_participation,
                    away_p_and_cards["part_tbl"][i][1],
                    away_p_and_cards["part_tbl"][i][2]
                ))
            
            
            writeSQL(database, '''
                INSERT INTO PLAYER_PARTICIPATION (id_match,id_player,id_participation
                     )
                VALUES (?, ?, ?)
                ''',(
                    id_match,
                    id_p,
                    id_participation
                ))
            

        for i in range(0,len(away_p_and_cards["cards"])) :
            
            writeSQL(database, '''
                INSERT INTO PLAYER_CARD (id_match,id_player,id_card,minute
                     )
                VALUES (?, ?, ?, ?)
                ''',(
                    id_match,
                    away_p_and_cards["cards"][i][0],
                    away_p_and_cards["cards"][i][1],
                    away_p_and_cards["cards"][i][2]
                ))
            
        for i in range(0,len(goals_per_match)) :
            
            writeSQL(database, '''
                INSERT INTO PLAYER_GOAL (id_match,id_player,id_goal,minute
                     )
                VALUES (?, ?, ?, ?)
                ''',(
                    id_match,
                    goals_per_match[i][0],
                    goals_per_match[i][1],
                    goals_per_match[i][2]
                ))
            


def run_matchweeks(season, league):
    for i in range(1,23):
        run_matches(season, league, i) 
        print('αγωνιστική :', i)
    

## GENERATE DATA
# create_types()
#create_team_players()
#create_schedule(1,3)
#run_matches(1,1,6)
#run_matchweeks(1,3)


