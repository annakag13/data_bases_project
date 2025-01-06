import sqlite3
import tkinter as tk
from tkinter import ttk


class ChampionshipApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Τοπικό Πρωτάθλημα")
        self.root.geometry("800x600")
        
        # Σύνδεση με τη βάση δεδομένων
        self.conn = sqlite3.connect("benglish.db")
        
        # Επιλογή query μέσω ComboBox
        self.query_label = tk.Label(root, text="Επιλέξτε ερώτημα:")
        self.query_label.pack(pady=5)
        
        self.query_combobox = ttk.Combobox(root, state="readonly")
        self.query_combobox['values'] = ["Χαρακτηριστικά ομάδων", "Πρόγραμμα αγώνων", "Βαθμολογία", "Ρόστερ Ομάδων", "Ποινές", "Top 10 σκόρερς", "Top 10 κίτρινων καρτών", "Top 10 κόκκινων καρτών", "Top 10 λεπτά συμμετοχής","Άνοδος σε κατηγορία","Υποβιβασμός σε κατηγορία","Fun facts"]
        self.query_combobox.current(0)  # Προεπιλογή πρώτου ερωτήματος
        self.query_combobox.pack(pady=5)
        self.query_combobox.bind("<<ComboboxSelected>>", self.on_query_selected)

        # ComboBox για κατηγορίες
        self.category_combobox_label = tk.Label(root, text="Επιλέξτε κατηγορία:")
        self.category_combobox = ttk.Combobox(root, state="readonly")

        # ComboBox για επιλογή ομάδας (θα γεμίζει με βάση την κατηγορία)
        self.team_combobox_label = tk.Label(root, text="Επιλέξτε ομάδα:")
        self.team_combobox = ttk.Combobox(root, state="readonly")

        # ComboBox για επιλογή fun fact
        self.ff_combobox_label = tk.Label(root, text="Επιλέξτε fun fact:")
        self.ff_combobox = ttk.Combobox(root, state="readonly")
        self.ff_combobox['values'] = ["Γκολ σε όλα τα εντός", "Γκολ από αλλαγή", "Νίκες εντός σε πάνω από τους μισούς νικηφόρους αγώνες"]
        self.ff_combobox.current(0)  # Προεπιλογή πρώτου ερωτήματος
        self.query_combobox.pack(pady=5)
        self.query_combobox.bind("<<ComboboxSelected>>", self.on_query_selected)

        # Combobox για επιλογή παίκτη
        self.player_action_label = tk.Label(root, text="Επιλέξτε ενέργεια:")
        self.player_action_combobox = ttk.Combobox(root, state="readonly")
        self.player_action_combobox['values'] = ["Αγώνες", "Στατιστικά"]
        self.player_action_button = tk.Button(root, text="Εκτέλεση", command=self.run_player_action)
        
        # Κουμπί εκτέλεσης query
        self.query_button = tk.Button(root, text="Εκτέλεση", command=self.run_query)
        self.query_button.pack(pady=10)
        
        # Πίνακας για την προβολή δεδομένων
        self.tree = ttk.Treeview(root, show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<ButtonRelease-1>", self.on_player_selected)

    def on_query_selected(self, event):
        
        selected_query = self.query_combobox.get()

        if selected_query == "Fun facts":
            # Εμφάνιση ComboBox για fun facts
            self.ff_combobox_label.pack(pady=5)
            self.ff_combobox.pack(pady=5)

        else:
            # Απόκρυψη ComboBox για fun facts
            self.ff_combobox_label.pack_forget()
            self.ff_combobox.pack_forget()
        
        if selected_query == "Ρόστερ Ομάδων" :
            # Εμφάνιση ComboBox για ομάδες
            self.team_combobox_label.pack(pady=5)
            self.team_combobox.pack(pady=5)
            
            # Γέμισμα του ComboBox με τις διαθέσιμες ομάδες
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM CLUB ORDER BY name")
            teams = [row[0] for row in cursor.fetchall()]
            self.team_combobox['values'] = teams
            if teams:
                self.team_combobox.current(0)  # Επιλογή πρώτης ομάδας

        else:
            # Απόκρυψη ComboBox για ομάδες
            self.team_combobox_label.pack_forget()
            self.team_combobox.pack_forget()

        if (selected_query in ["Χαρακτηριστικά ομάδων", "Πρόγραμμα αγώνων", "Βαθμολογία", "Ποινές", "Top 10 σκόρερς", "Top 10 κίτρινων καρτών", "Top 10 κόκκινων καρτών","Top 10 λεπτά συμμετοχής","Fun facts"]):
            # Εμφάνιση ComboBox για κατηγορίες
            self.category_combobox_label.pack(pady=5)
            self.category_combobox.pack(pady=5)
        
            # Γέμισμα του ComboBox με τις διαθέσιμες κατηγορίες
            cursor = self.conn.cursor()
            cursor.execute("SELECT DISTINCT name FROM LEAGUE ORDER BY name")
            categories = [row[0] for row in cursor.fetchall()]
            self.category_combobox['values'] = categories
            if categories:
                self.category_combobox.current(0)  # Προεπιλογή πρώτης κατηγορίας

        else:
            # Απόκρυψη ComboBox για κατηγορίες
            self.category_combobox_label.pack_forget()
            self.category_combobox.pack_forget() 

        # Απόκρυψη Combobox και κουμπιού για παίκτη
        self.player_action_label.pack_forget()
        self.player_action_combobox.pack_forget()
        self.player_action_button.pack_forget()

    def on_player_selected(self, event):
        # Έλεγχος ότι το ενεργό query είναι "Ρόστερ Ομάδων"
        if self.query_combobox.get() != "Ρόστερ Ομάδων":
            return
        # Παίρνουμε το επιλεγμένο στοιχείο
        selected_item = self.tree.focus()
        if not selected_item:
            return

        player_data = self.tree.item(selected_item, "values")
        if len(player_data) < 2:  # Έλεγχος ότι έχουμε επαρκή δεδομένα
            return

        self.selected_player_id = player_data[0] #Το id του παίκτη
        self.selected_player_name = player_data[1]  # Το όνομα του παίκτη
        self.selected_player_lastname = player_data[2]  # Το επώνυμο του παίκτη
    
        # Εμφάνιση Combobox και κουμπιού
        self.player_action_label.pack(pady=5)
        self.player_action_combobox.pack(pady=5)
        self.player_action_button.pack(pady=5)

        # Απόκρυψη ComboBox για ομάδες
        self.team_combobox_label.pack_forget()
        self.team_combobox.pack_forget()

    
    def run_query(self):
        """Εκτέλεση query ανάλογα με την επιλογή του χρήστη."""
        # Καθορισμός query ανάλογα με την επιλογή στο ComboBox
        selected_query = self.query_combobox.get()
        results = []
        columns = []

        if selected_query == "Υποβιβασμός σε κατηγορία":
            cursor = self.conn.cursor()

            query = """
            WITH RankedTeams AS (
            SELECT id, league1, name, ROW_NUMBER() OVER (PARTITION BY league1 ORDER BY points ASC, (goal_over - goal_against) ASC, goal_over DESC) AS rank
            FROM RANKING
            )
            SELECT r.name AS relegated_teams, (r.league1 || ' -> ' || COALESCE(l_next.name, ''))AS leagues
            FROM RankedTeams AS r
            JOIN LEAGUE AS l1 ON r.league1 = l1.name
            LEFT JOIN LEAGUE AS l_next ON l_next.id_league = l1.id_league + 1
            WHERE r.rank = 1 AND r.league1 <> 'Γ'
            GROUP BY r.league1, l1.id_league;
            """
            columns = ["Ομάδες σε υποβιβασμό", "Κατηγορίες"]
            cursor.execute(query)
            results = cursor.fetchall()

        if selected_query == "Άνοδος σε κατηγορία":
            cursor = self.conn.cursor()

            query = """
            WITH RankedTeams AS (
            SELECT id, league1, name, ROW_NUMBER() OVER (PARTITION BY league1 ORDER BY points DESC, (goal_over - goal_against) DESC, goal_over DESC) AS rank
            FROM RANKING
            )
        SELECT r.name AS promoted_teams, (r.league1 || ' -> ' || COALESCE(l_next.name, ''))AS leagues
        FROM RankedTeams AS r
        JOIN LEAGUE AS l1 ON r.league1 = l1.name
        LEFT JOIN LEAGUE AS l_next ON l_next.id_league = l1.id_league - 1
        WHERE r.rank = 1 AND r.league1 <> 'Α'
        GROUP BY r.league1, l1.id_league;
            """
            columns = ["Ομάδες σε άνοδο", "Κατηγορίες"]
            cursor.execute(query)
            results = cursor.fetchall()
        
        if selected_query == "Χαρακτηριστικά ομάδων":
            selected_category = self.category_combobox.get()
            if not selected_category:
                tk.messagebox.showerror("Σφάλμα", "Παρακαλώ επιλέξτε κατηγορία.")
                return
    
            # Γέμισμα του ComboBox με τις ομάδες που ανήκουν στην επιλεγμένη κατηγορία
            cursor = self.conn.cursor()
    
            # Ερώτημα για τα χαρακτηριστικά της επιλεγμένης κατηγορίας
            query = """
    SELECT  cl.name AS team_name, a.name AS arena_name, 
           (SELECT COUNT(DISTINCT tp_inner.id_player)
            FROM TEAM_PLAYER AS tp_inner 
            WHERE tp_inner.id_team_per_season = t.id_team_per_season) AS player_count,
           GROUP_CONCAT(c.coach_info, ', ') AS coaches
    FROM ((((TEAM_PER_SEASON AS t JOIN CLUB as cl on t.EPO_id = cl.EPO_id)
            JOIN LEAGUE as l on l.id_league = t.id_league)
            JOIN  ARENA AS a ON t.id_arena = a.id_arena)
            JOIN (SELECT DISTINCT id_team_per_season, 
                         name || ' ' || lastname || ' (' || start_date || ' - ' || IFNULL(end_date, 'Present') || ')' AS coach_info
                  FROM COACH) AS c 
            ON t.id_team_per_season = c.id_team_per_season)
    WHERE l.name = ?
    GROUP BY t.id_team_per_season
    ORDER BY t.id_team_per_season;
    """
            columns = ["Όνομα Ομάδας", "Γήπεδο",  "Αριθμός Ποδοσφαιριστών", "Προπονητές"]
            cursor.execute(query, (selected_category,))
            results = cursor.fetchall()
        
        elif selected_query == "Πρόγραμμα αγώνων":
            selected_category = self.category_combobox.get()
            if not selected_category:
                tk.messagebox.showerror("Σφάλμα", "Παρακαλώ επιλέξτε κατηγορία.")
                return
    
            # Γέμισμα του ComboBox με τις ομάδες που ανήκουν στην επιλεγμένη κατηγορία
            query = """
            SELECT ml.round, cl1.name as team_home, cl2.name as team_guest, a.name as arena_name, m.match_time, m.match_date, ((mr.goal_home_over + mr.goal_guest_against) || ' - ' || (mr.goal_guest_over + mr.goal_home_against)) as score, m.referee, m.assistant_referee1, m.assistant_referee2
            FROM ((((((((MATCH as m JOIN MATCHWEEK as ml on m.id_matchweek = ml.id_matchweek)JOIN league as l on ml.id_league = l.id_league) JOIN TEAM_PER_SEASON as t on t.id_team_per_season = m.id_team_home)JOIN CLUB as cl1 on cl1.EPO_id = t.EPO_id)join TEAM_PER_SEASON as t1 on t1.id_team_per_season = m.id_team_guest)JOIN CLUB as cl2 on cl2.EPO_id = t1.EPO_id) JOIN ARENA as a on a.id_arena = t.id_arena) JOIN MATCH_RESULT  as mr on mr.id_match = m.id_match)
            WHERE l.name = ?;

            """
            columns = [ "Αγωνιστική", "Γηπεδούχος Ομάδα", "Φιλοξενούμενη Ομάδα", "Γήπεδο", "Ώρα αγώνα","Ημερομηνία αγώνα", "Σκορ", "Διαιτητής", "Α'βοηθός", "Β' βοηθός"]
            cursor = self.conn.cursor()
            cursor.execute(query, (selected_category,))
            results = cursor.fetchall()

        elif selected_query == "Βαθμολογία":
            selected_category = self.category_combobox.get()
            if not selected_category:
                tk.messagebox.showerror("Σφάλμα", "Παρακαλώ επιλέξτε κατηγορία.")
                return
            query = """
            SELECT year,  name, matches, points, win, defeat, draw, goal_over, goal_against
            FROM RANKING
            WHERE league1 = ?;
            """
            columns = ["Σεζόν","Ομάδα","Αγώνες", "Βαθμοί", "Νίκες", "Ήττες", "Ισοπαλίες", "Γκολ Υπέρ", "Γκολ Κατά"]
            cursor = self.conn.cursor()
            cursor.execute(query, (selected_category,))
            results = cursor.fetchall()

        elif selected_query == "Ρόστερ Ομάδων":
           # Ανάκτηση της επιλεγμένης ομάδας
            selected_team = self.team_combobox.get()
        
            if not selected_team:
                # Αν δεν έχει επιλεγεί ομάδα, εμφάνιση μηνύματος λάθους
                tk.messagebox.showerror("Σφάλμα", "Παρακαλώ επιλέξτε ομάδα για να δείτε το ρόστερ.")
                return
        
        # Query για το ρόστερ της συγκεκριμένης ομάδας
            query = """
                SELECT  p.id_player, p.name, p.lastname, strftime('%Y', p.birthday) as year_of_birth, p.position
                FROM (((TEAM_PER_SEASON as t JOIN CLUB as cl on cl.EPO_id = t.EPO_id)
                    JOIN TEAM_PLAYER as tp on t.id_team_per_season = tp.id_team_per_season)
                    JOIN PLAYER as p on tp.id_player = p.id_player)
                 WHERE cl.name = ?
                ORDER BY p.lastname;
            """
            columns = ["Id","Όνομα", "Επίθετο", "Έτος γέννησης", "Θέση"]
        
            cursor = self.conn.cursor()
            cursor.execute(query, (selected_team,))
            results = cursor.fetchall()

        elif selected_query == "Ποινές":
            selected_category = self.category_combobox.get()
            if not selected_category:
                tk.messagebox.showerror("Σφάλμα", "Παρακαλώ επιλέξτε κατηγορία.")
                return
            query = """
            SELECT cl.name, cl.EPO_id, p.reason, p.duration, p.money_penalty, p.points_penalty, tp.punishment_date
            FROM((((TEAM_PER_SEASON as t JOIN CLUB as cl on t.EPO_id = cl.EPO_id)JOIN TEAM_PUNISHMENT as tp on tp.id_team_per_season = t.id_team_per_season)JOIN PUNISHMENT as p on p.id_punishment = tp.id_punishment)JOIN LEAGUE as l on l.id_league = t.id_league)
            WHERE l.name = ?
            ORDER BY cl.name;
            """   
            columns = ["Ομάδα", "ΕΠΟ Id", "Αιτιολογία", "Διάρκεια", "Χρηματικό πρόστιμο", "Βαθμοί ποινής", "Ημερομηνία επιβολής"]

            cursor = self.conn.cursor()
            cursor.execute(query, (selected_category,))
            results = cursor.fetchall()

        elif selected_query == "Top 10 σκόρερς":
            selected_category = self.category_combobox.get()
            if not selected_category:
                tk.messagebox.showerror("Σφάλμα", "Παρακαλώ επιλέξτε κατηγορία.")
                return
            query = """
            WITH RankedPlayers AS (
        SELECT 
            s.year, 
            l.name AS league_name, 
            p.id_player, 
            p.name AS player_name, 
            p.lastname, 
            COUNT(pg.id_goal) AS goals_over, 
            cl.name AS club_name,
            ROW_NUMBER() OVER (PARTITION BY l.name ORDER BY COUNT(pg.id_goal) DESC) AS rank
        FROM PLAYER AS p
            JOIN PLAYER_GOAL AS pg ON p.id_player = pg.id_player
            JOIN GOAL AS g ON pg.id_goal = g.id_goal
            JOIN TEAM_PLAYER AS tp ON tp.id_player = p.id_player
            JOIN TEAM_PER_SEASON AS t ON t.id_team_per_season = tp.id_team_per_season
            JOIN CLUB AS cl ON cl.EPO_id = t.EPO_id
            JOIN LEAGUE AS l ON l.id_league = t.id_league
            JOIN SEASON AS s ON s.id_season = t.id_season
        WHERE g.type = "γκολ_υπέρ"
        GROUP BY s.year, l.name, p.id_player, p.name, p.lastname, cl.name
        )
        SELECT 
            year, 
            player_name, 
            lastname, 
            goals_over, 
            club_name
        FROM RankedPlayers
        WHERE rank <= 10 and league_name = ?
        ORDER BY league_name, rank;
            """
            columns = ["Σεζόν",  "Όνομα", "Επίθετο", "Γκολ", "Ομάδα"]

            cursor = self.conn.cursor()
            cursor.execute(query, (selected_category,))
            results = cursor.fetchall()

        elif selected_query == "Top 10 κίτρινων καρτών":
            selected_category = self.category_combobox.get()
            if not selected_category:
                tk.messagebox.showerror("Σφάλμα", "Παρακαλώ επιλέξτε κατηγορία.")
                return
            query = """
            SELECT s.year, p.name, p.lastname, count(pc.id_card) as yellow_cards, cl.name as club_name
            FROM(((((((PLAYER as p JOIN PLAYER_CARD as pc on p.id_player = pc.id_player) JOIN CARD as c on pc.id_card = c.id_card) JOIN TEAM_PLAYER as tp on tp.id_player = p.id_player)JOIN TEAM_PER_SEASON as t on t.id_team_per_season = tp.id_team_per_season)JOIN CLUB as cl on cl.EPO_id = t.EPO_id)JOIN LEAGUE as l on l.id_league = t.id_league)join season as s on s.id_season = t.id_season)
            WHERE c.type = "κίτρινη" and l.name = ?
            GROUP BY p.id_player
            ORDER BY yellow_cards desc
            LIMIT 10;
            """
            columns = ["Σεζόν", "Όνομα", "Επίθετο", "Κίτρινες κάρτες", "Ομάδα"]

            cursor = self.conn.cursor()
            cursor.execute(query, (selected_category,))
            results = cursor.fetchall()

        elif selected_query == "Top 10 κόκκινων καρτών":
            selected_category = self.category_combobox.get()
            if not selected_category:
                tk.messagebox.showerror("Σφάλμα", "Παρακαλώ επιλέξτε κατηγορία.")
                return
            query = """
            SELECT s.year, p.name, p.lastname, count(pc.id_card) as red_cards, cl.name as club_name
            FROM(((((((PLAYER as p JOIN PLAYER_CARD as pc on p.id_player = pc.id_player) JOIN CARD as c on pc.id_card = c.id_card) JOIN TEAM_PLAYER as tp on tp.id_player = p.id_player)JOIN TEAM_PER_SEASON as t on t.id_team_per_season = tp.id_team_per_season)JOIN CLUB as cl on cl.EPO_id = t.EPO_id)JOIN LEAGUE as l on l.id_league = t.id_league)join season as s on s.id_season = t.id_season)
            WHERE c.type = "κόκκινη" and l.name =?
            GROUP BY p.id_player
            ORDER BY red_cards desc
            LIMIT 10;
            """
            columns = ["Σεζόν", "Όνομα", "Επίθετο", "Κόκκινες κάρτες", "Ομάδα"]

            cursor = self.conn.cursor()
            cursor.execute(query, (selected_category,))
            results = cursor.fetchall()

        elif selected_query == "Top 10 λεπτά συμμετοχής":
            selected_category = self.category_combobox.get()
            if not selected_category:
                tk.messagebox.showerror("Σφάλμα", "Παρακαλώ επιλέξτε κατηγορία.")
                return
            query = """
            SELECT s.year, cl.name as club_name, p.name, p.lastname, sum(pa.minute_out - pa.minute_in) as participation_minutes, count(pp.id_match) as matches
            FROM(((((((PLAYER as p JOIN PLAYER_PARTICIPATION as pp on p.id_player = pp.id_player) JOIN PARTICIPATION as pa on pp.id_participation = pa.id_participation) JOIN TEAM_PLAYER as tp on tp.id_player = p.id_player)JOIN TEAM_PER_SEASON as t on t.id_team_per_season = tp.id_team_per_season)JOIN CLUB as cl on cl.EPO_id = t.EPO_id)JOIN LEAGUE as l on l.id_league = t.id_league)join season as s on s.id_season = t.id_season)
            WHERE l.name = ?
            GROUP BY p.id_player 
            ORDER BY participation_minutes desc, p.lastname ASC
            LIMIT 10;
            """
            columns = ["Σεζόν", "Ομάδα", "Όνομα", "Επίθετο", "Λεπτά συμμετοχής", "Αγώνες που αγωνίστηκε"]

            cursor = self.conn.cursor()
            cursor.execute(query, (selected_category,))
            results = cursor.fetchall()

        elif selected_query == "Fun facts":
            selected_category = self.category_combobox.get()
            if not selected_category:
                tk.messagebox.showerror("Σφάλμα", "Παρακαλώ επιλέξτε κατηγορία.")
                return
            selected_fun_fact = self.ff_combobox.get()
            print(f"Selected Fun Fact: {selected_fun_fact}")  # Για debugging

            if selected_fun_fact == "Γκολ σε όλα τα εντός":
                query = """
        SELECT DISTINCT cl.name AS club_name
        FROM (TEAM_PER_SEASON AS t 
              JOIN CLUB AS cl ON t.EPO_id = cl.EPO_id 
              JOIN LEAGUE AS l ON t.id_league = l.id_league)
        WHERE l.name = ? and NOT EXISTS (
            SELECT 1
            FROM MATCH AS m
            WHERE m.id_team_home = t.id_team_per_season
              AND NOT EXISTS (
                  SELECT 1
                  FROM MATCH_RESULT AS mr
                  WHERE mr.id_match = m.id_match
                    AND (
                        (mr.id_team_home = t.id_team_per_season AND mr.goal_home_over > 0)
                    )
              )
        )
        AND EXISTS (
            SELECT 1
            FROM MATCH AS m2
            WHERE m2.id_team_home = t.id_team_per_season 
               OR m2.id_team_guest = t.id_team_per_season
        );
        """
                columns = ["Ομάδες"]
                cursor = self.conn.cursor()
                cursor.execute(query, (selected_category,))
                results = cursor.fetchall()

            if selected_fun_fact == "Γκολ από αλλαγή":
                query = """
                SELECT mp.year, mp.id_match, mp.id_player,  mp.player_name,  mp.player_lastname
                FROM MATCHES_PLAYERS AS mp
                WHERE mp.player_status = 'αλλαγή' AND mp.goals_over >= 1 AND mp.league_name = ?
                GROUP BY mp.id_match;
                """
                columns = ["Σεζόν", "Id ματς", "Id παίκτη","Όνομα","Επίθετο"]
                cursor = self.conn.cursor()
                cursor.execute(query, (selected_category,))
                results = cursor.fetchall()

            if selected_fun_fact == "Νίκες εντός σε πάνω από τους μισούς νικηφόρους αγώνες":
                query = """
                SELECT  r.name,((r.win * 100)/r.matches) as percentage_win,((select count(mr.id_match)
																 FROM MATCH_RESULT as mr
																 WHERE (mr.id_team_home = r.id and (mr.goal_home_over + mr.goal_guest_against > mr.goal_guest_over + mr.goal_home_against))) *100/r.win) as percentage_home_win
                FROM RANKING as r 
                WHERE r.league1 = ?
                GROUP BY r.id
                HAVING ((r.win * 100)/r.matches)>=50;
                """
                columns = ["Ομάδες", "Ποσοστό νικών", "Ποσοστό νικών εντός"]
                cursor = self.conn.cursor()
                cursor.execute(query, (selected_category,))
                results = cursor.fetchall()

        '''if (selected_query != "Ρόστερ Ομάδων" and selected_query != "Χαρακτηριστικά ομάδων" and selected_query != "Πρόγραμμα αγώνων" ):
        # Εκτέλεση του query
            cursor = self.conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()'''
        
        # Ανανεώνουμε τις στήλες του Treeview
        self.tree["columns"] = columns
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        
        # Καθαρισμός υπάρχοντος περιεχομένου
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Εισαγωγή αποτελεσμάτων στον πίνακα
        for row in results:
            self.tree.insert("", tk.END, values=row)

    def run_player_action(self):
        action = self.player_action_combobox.get()
        results = []
        columns = []
        if not action:
            tk.messagebox.showerror("Σφάλμα", "Παρακαλώ επιλέξτε ενέργεια.")
            return

        cursor = self.conn.cursor()

        if action == "Αγώνες":
            # Query για τους αγώνες του παίκτη
            query = """
        SELECT mp.id_match, mp.match_date, mp.score, mp.minutes_of_participation, mp.goals_over, mp.goals_against, mp.yellow_cards, mp.red_cards, mp.player_status
        FROM MATCHES_PLAYERS as mp
        WHERE mp.id_player = ? AND mp.player_name = ? AND mp.player_lastname = ?;
        """
            cursor.execute(query, (self.selected_player_id, self.selected_player_name, self.selected_player_lastname))
            columns = ["Id αγώνα","Ημερομηνία", "Σκορ", "Λεπτά συμμετοχής", "Γκολ", "Αυτογκόλ", "Κίτρινες κάρτες", "Κόκκινες κάρτες", "Ρόλος"]
            results = cursor.fetchall()

        elif action == "Στατιστικά":
        # Query για τα στατιστικά του παίκτη
            query = """
        SELECT mp.year, sum(mp.goals_over), sum(mp.goals_against), sum(mp.yellow_cards), sum(mp.red_cards), sum(mp.minutes_of_participation), count(mp.id_match)
        FROM MATCHES_PLAYERS as mp 
        WHERE mp.id_player = ? AND mp.player_name = ? AND mp.player_lastname = ?
        GROUP BY mp.year, mp.id_player;
        """
            cursor.execute(query, (self.selected_player_id, self.selected_player_name, self.selected_player_lastname))
            columns = ["Σεζόν", "Γκολ", "Αυτογκόλ", "Κίτρινες κάρτες", "Κόκκινες κάρτες", "Λεπτά συμμετοχής", "Αγώνες"]
            results = cursor.fetchall()

        else:
            tk.messagebox.showerror("Σφάλμα", "Μη έγκυρη ενέργεια.")
            return


        # Ενημέρωση πίνακα με αποτελέσματα
        self.tree["columns"] = columns
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        # Καθαρισμός υπάρχοντος περιεχομένου
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Προσθήκη νέων δεδομένων
        for row in results:
            self.tree.insert("", tk.END, values=row)


if __name__ == "__main__":
    root = tk.Tk()
    app = ChampionshipApp(root)
    root.mainloop()