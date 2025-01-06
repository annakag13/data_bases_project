from gc import callbacks
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
#from admin import *
from connect import *
from crud import *
import sqlite3

database = 'benglish.db'

class ChampionshipApp:
    def __init__(self):
        # Αρχικό Παράθυρο
        self.root = tk.Tk()
        self.root.title("Τοπικό Πρωτάθλημα")
        self.root.geometry("800x600")
        self.root.resizable(False,False)

        # Εικόνα Φόντου
        self.bg_image = Image.open("background.png")  
        self.bg_image = self.bg_image.resize((800, 600), Image.ANTIALIAS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        # Κουμπιά για κάθε επιλογή
        button1 = tk.Button(self.root, text="Fun facts", command=self.open_window_1,bg="gold")
        button1.place(relx=0.9, rely=0.9, anchor="se")  

        button2 = tk.Button(self.root, text="Top 10 παικτών", command=self.open_window_2,bg="lawngreen")
        button2.place(relx=0.8, rely=0.9, anchor="se")  

        button3 = tk.Button(self.root, text="Ομάδες", command=self.open_window_3,bg="mediumturquoise")
        button3.place(relx=0.66, rely=0.9, anchor="se")  

        button4 = tk.Button(self.root, text="Login", command=self.open_window_4)
        button4.place(relx=0.76, rely=0.8, anchor="se")

        self.root.mainloop()

    def open_window_1(self):
        self.create_window("Fun facts",1)

    def open_window_2(self):
        self.create_window("Top 10 παικτών",2)

    def open_window_3(self):
        self.create_window("Ομάδες",3)

    def open_window_4(self):
        # Δημιουργία παραθύρου Login
        login_window = tk.Toplevel(self.root)
        login_window.title("Login")
        login_window.geometry("400x300")

        # StringVars για πεδία εισαγωγής
        username_var = tk.StringVar()
        password_var = tk.StringVar()

        # Ετικέτα και πεδίο εισαγωγής Username
        tk.Label(login_window, text="Username:").pack(pady=10)
        username_entry = tk.Entry(login_window, textvariable=username_var)
        username_entry.pack(pady=5)

        # Ετικέτα και πεδίο εισαγωγής Password
        tk.Label(login_window, text="Password:").pack(pady=10)
        password_entry = tk.Entry(login_window, textvariable=password_var, show="*")
        password_entry.pack(pady=5)

        # Συνάρτηση ελέγχου δεδομένων
        def login():
            username = username_var.get()
            password = password_var.get()

            # SQL ερώτημα
            q = {
            "table": 'USER',
            "field": ["password", "role"],
            "where": [("username", "=", "?"), ("password", "=", "?")],
            "order": None
            }
            res = readSQL(database, read(q), (username, password))

            if len(res) > 0:
                (pw, role) = res[0]
                global current_user_role, current_user
                current_user_role = role
                current_user = username
                #tk.messagebox.showinfo("Login Success", f"Welcome, {username}!")
                login_window.destroy()  # Κλείσιμο παραθύρου Login
                if username == "Admin":
                    self.open_admin_window(1)  # Άνοιγμα νέου παραθύρου
                else:
                    self.open_admin_window(2)
            else:
                tk.messagebox.showerror("Login Failed", "Wrong credentials!")

        # Κουμπί Login μέσα στο νέο παράθυρο
        login_button = tk.Button(login_window, text="Login", command=login)
        login_button.pack(pady=20)

        # Focus στο πεδίο Username
        username_entry.focus()

    def open_admin_window(self,num):
        admin_window = tk.Toplevel(self.root)
        admin_window.title("Admin Panel")
        admin_window.geometry("400x200")

        # Combobox με επιλογές
        if num == 1: 
            options = ["Εισαγωγή παίκτη σε ομάδα", "Αλλαγή password", "Δημιουργία roster_admin", "Διαγραφή roster_admin"]
        else: 
            options = ["Εισαγωγή παίκτη σε ομάδα", "Αλλαγή password"]
        selected_option = tk.StringVar()
        combobox = ttk.Combobox(admin_window, textvariable=selected_option, state="readonly")
        combobox['values'] = options
        combobox.current(0)  # Προεπιλογή πρώτης επιλογής
        combobox.pack(side=tk.LEFT, padx=10, pady=10)

        def execute_action():
            selected_action = selected_option.get()
            if selected_action == "Εισαγωγή παίκτη σε ομάδα":
                self.open_set_player_to_roster_window()
            if selected_action == "Αλλαγή password":
                self.open_change_password_window()
            if selected_action == "Δημιουργία roster_admin":
                self.open_create_user_window()
            if selected_action == "Διαγραφή roster_admin":
                self.open_delete_user_window()

        # Κουμπί Εκτέλεση
        execute_button = tk.Button(admin_window, text="Εκτέλεση", command=execute_action)
        execute_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Κουμπί Logout
        def logout():
            admin_window.destroy()
            messagebox.showinfo("Logout", "You have been logged out!")

        logout_button = tk.Button(admin_window, text="Logout", command=logout)
        logout_button.pack(side=tk.LEFT, padx=20, pady=10)

    def create_window(self, title, num):
        self.root.withdraw()
        new_window = tk.Toplevel(self.root)
        new_window.title(title)
        new_window.geometry("800x630")
        new_window.resizable(False,False)

        new_window.protocol("WM_DELETE_WINDOW", lambda: self.on_close_new_window(new_window))
        back_button = tk.Button(new_window, text="Επιστροφή", command=lambda: self.on_close_new_window(new_window))
        back_button.pack(pady=10)


        # Φόρτωση εικόνας φόντου
        bg_image = Image.open("photo2.png")  # Αντικατάστησε με τη διαδρομή της εικόνας σου
        bg_image = bg_image.resize((800, 600), Image.ANTIALIAS)
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Ετικέτα φόντου
        bg_label = tk.Label(new_window, image=bg_photo)
        bg_label.image = bg_photo  # Κρατάμε αναφορά για να μην διαγραφεί η εικόνα
        bg_label.place(relwidth=1, relheight=1)

        self.conn = sqlite3.connect("benglish.db")

        # Ετικέτα για επιλογή ερωτήματος
        query_label = tk.Label(new_window, text="Επιλέξτε ερώτημα:", bg = "white")
        query_label.pack(pady = 5)

        # ComboBox για επιλογή ερωτήματος
        self.query_combobox = ttk.Combobox(new_window, state="readonly")
        if num == 1 :
            self.query_combobox['values'] = ["Γκολ σε όλα τα εντός", "Γκολ από αλλαγή", "Νίκες εντός σε πάνω από τους μισούς νικηφόρους αγώνες"]
        if num == 2 :
            self.query_combobox['values'] = [ "Top 10 σκόρερς", "Top 10 κίτρινων καρτών", "Top 10 κόκκινων καρτών", "Top 10 λεπτά συμμετοχής"]
        if num == 3 :
            self.query_combobox['values'] = ["Χαρακτηριστικά ομάδων", "Πρόγραμμα αγώνων", "Βαθμολογία", "Ρόστερ Ομάδων", "Ποινές",
                                "Άνοδος σε κατηγορία", "Υποβιβασμός σε κατηγορία"]
        self.query_combobox.current(0)
        self.query_combobox.pack(pady=5)

        # ComboBox για κατηγορίες
        self.category_combobox_label = tk.Label(new_window, text="Επιλέξτε κατηγορία:", bg = "white")
        self.category_combobox = ttk.Combobox(new_window, state="readonly")

        # ComboBox για επιλογή ομάδας (θα γεμίζει με βάση την κατηγορία)
        self.team_combobox_label = tk.Label(new_window, text="Επιλέξτε ομάδα:")
        self.team_combobox = ttk.Combobox(new_window, state="readonly")

        '''# ComboBox για επιλογή fun fact
        self.ff_combobox_label = tk.Label(new_window, text="Επιλέξτε fun fact:")
        self.ff_combobox = ttk.Combobox(new_window, state="readonly")
        self.ff_combobox['values'] = ["Γκολ σε όλα τα εντός", "Γκολ από αλλαγή", "Νίκες εντός σε πάνω από τους μισούς νικηφόρους αγώνες"]
        self.ff_combobox.current(0)  # Προεπιλογή πρώτου ερωτήματος
        self.query_combobox.pack(pady=5)'''

        # Combobox για επιλογή παίκτη
        self.player_action_label = tk.Label(new_window, text="Επιλέξτε ενέργεια:")
        self.player_action_combobox = ttk.Combobox(new_window, state="readonly")
        self.player_action_combobox['values'] = ["Αγώνες", "Στατιστικά"]
        self.player_action_button = tk.Button(new_window, text="Εκτέλεση", command=self.run_player_action)
        
        # Κουμπί εκτέλεσης query
        query_button = tk.Button(new_window, text="Εκτέλεση", command=lambda: self.run_query(new_window, self.conn))
        query_button.pack(pady=5)

        '''# Frame για την Treeview και το Scrollbar
        tree_frame = tk.Frame(new_window)
        tree_frame.pack(padx=30, pady=0, anchor="center", fill=tk.X)  fill=tk.BOTH, expand=True

        # Πίνακας για προβολή δεδομένων
        self.tree = ttk.Treeview(tree_frame, show="headings", height=18)  
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  
        #self.tree.place(x=50, y=150, width=700, height=300)
        #self.tree.pack(padx=30, pady=0, anchor="center", fill=tk.X)
        #self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<ButtonRelease-1>", self.on_player_selected)

        # Scrollbar στο πλάι
        scrollbar = tk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Σύνδεση της Scrollbar με την Treeview
        self.tree.configure(yscrollcommand=scrollbar.set)'''

        # Frame για την Treeview και το Scrollbar
        tree_frame = tk.Frame(new_window)
        tree_frame.pack(padx=30, pady=0, anchor="center", fill=tk.X)

        # Scrollbar στο πλάι
        scrollbar = tk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Πίνακας για προβολή δεδομένων
        self.tree = ttk.Treeview(tree_frame, show="headings", height=18, yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Σύνδεση της Scrollbar με την Treeview
        scrollbar.config(command=self.tree.yview)

        # Σύνδεση event για επιλογή στοιχείου
        self.tree.bind("<ButtonRelease-1>", self.on_player_selected)

        # Δέσιμο επιλογής query με κάποια ενέργεια
        self.query_combobox.bind("<<ComboboxSelected>>", lambda event: self.on_query_selected( self.query_combobox, self.conn))

    def on_close_new_window(self, new_window):
        # Καταστροφή του νέου παραθύρου
        new_window.destroy()
        # Επανεμφάνιση του αρχικού παραθύρου
        self.root.deiconify()

    def on_query_selected(self, query_combobox, conn):
        
        selected_query = self.query_combobox.get()

        '''if selected_query == "Fun facts":
            # Εμφάνιση ComboBox για fun facts
            self.ff_combobox_label.pack(pady=5)
            self.ff_combobox.pack(pady=5)

        else:
            # Απόκρυψη ComboBox για fun facts
            self.ff_combobox_label.pack_forget()
            self.ff_combobox.pack_forget()'''
        
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

        if (selected_query in ["Χαρακτηριστικά ομάδων", "Πρόγραμμα αγώνων", "Βαθμολογία", "Ποινές", "Top 10 σκόρερς", "Top 10 κίτρινων καρτών", "Top 10 κόκκινων καρτών","Top 10 λεπτά συμμετοχής","Γκολ σε όλα τα εντός", "Γκολ από αλλαγή", "Νίκες εντός σε πάνω από τους μισούς νικηφόρους αγώνες"]):
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

    
    def run_query(self, window, conn):
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
            ROW_NUMBER() OVER (PARTITION BY l.name ORDER BY COUNT(pg.id_goal) DESC, p.lastname) AS rank
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
            ORDER BY yellow_cards desc, p.lastname
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
            ORDER BY red_cards desc, p.lastname
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

        elif selected_query == "Γκολ σε όλα τα εντός":
            selected_category = self.category_combobox.get()
            if not selected_category:
                tk.messagebox.showerror("Σφάλμα", "Παρακαλώ επιλέξτε κατηγορία.")
                return
            '''selected_fun_fact = self.ff_combobox.get()
            print(f"Selected Fun Fact: {selected_fun_fact}")  # Για debugging'''

            #if selected_fun_fact == "Γκολ σε όλα τα εντός":
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

        elif selected_query == "Γκολ από αλλαγή":
            selected_category = self.category_combobox.get()
            if not selected_category:
                tk.messagebox.showerror("Σφάλμα", "Παρακαλώ επιλέξτε κατηγορία.")
                return
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

        elif selected_query == "Νίκες εντός σε πάνω από τους μισούς νικηφόρους αγώνες":
            selected_category = self.category_combobox.get()
            if not selected_category:
                tk.messagebox.showerror("Σφάλμα", "Παρακαλώ επιλέξτε κατηγορία.")
                return
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

    def open_set_player_to_roster_window(self):
        roster_window = tk.Toplevel(self.root)
        roster_window.title("Set Player to Roster")
        roster_window.geometry("600x400")

        # Επιλογή Season ID
        tk.Label(roster_window, text="Select Season ID:").pack(pady=5)
        season_id_var = tk.StringVar()
        season_id_entry = tk.Entry(roster_window, textvariable=season_id_var)
        season_id_entry.pack(pady=5)

        # Επιλογή Team ID
        tk.Label(roster_window, text="Select Team ID:").pack(pady=5)
        team_id_var = tk.StringVar()
        team_id_entry = tk.Entry(roster_window, textvariable=team_id_var)
        team_id_entry.pack(pady=5)

        # Συνάρτηση Εκτέλεσης
        '''def set_player_to_roster():
            season_id = season_id_var.get()
            team_id = team_id_var.get()

            season = readSQL(database, "SELECT id_season, year, start, end FROM SEASON")
            selected_start, selected_end = '', ''
            for (sid, yr, start, end) in season:
                if int(season_id) == sid:
                    selected_start = start
                    selected_end = end

            id_player = self.open_create_player_window(team_id)

            ins = {
            "table": "TEAM_PLAYER",
            "field": ["id_player", "id_team_per_season", "start_date", "end_date"],
            "value": ['?', '?', '?', '?']
            }
            writeSQL(database, insert(ins), (id_player, team_id, selected_start, selected_end))
            messagebox.showinfo("Success", "Player added to roster successfully!")
            roster_window.destroy()

        # Κουμπί Εκτέλεσης
        submit_button = tk.Button(roster_window, text="Εκτέλεση", command=set_player_to_roster)
        submit_button.pack(pady=10)'''
        def set_player_to_roster():
            season_id = season_id_var.get()
            team_id = team_id_var.get()

            season = readSQL(database, "SELECT id_season, year, start, end FROM SEASON")
            selected_start, selected_end = '', ''
            for (sid, yr, start, end) in season:
                if int(season_id) == sid:
                    selected_start = start
                    selected_end = end

            # Κλήση του παραθύρου για τη δημιουργία του παίκτη με callback
            self.open_create_player_window(team_id, handle_new_player)
    
        def handle_new_player(self, new_player_id):
            season_id = season_id_var.get()
            team_id = team_id_var.get()

            season = readSQL(database, "SELECT id_season, year, start, end FROM SEASON")
            selected_start, selected_end = '', ''
            for (sid, yr, start, end) in season:
                if int(season_id) == sid:
                    selected_start = start
                    selected_end = end

            # Προσθήκη του νέου παίκτη στην ομάδα
            ins = {
        "table": "TEAM_PLAYER",
        "field": ["id_player", "id_team_per_season", "start_date", "end_date"],
        "value": ['?', '?', '?', '?']
        }
            writeSQL(database, insert(ins), (new_player_id, team_id, selected_start, selected_end))
            messagebox.showinfo("Success", "Player added to roster successfully!")
            roster_window.destroy()
        # Κουμπί Εκτέλεσης
        submit_button = tk.Button(roster_window, text="Εκτέλεση", command=set_player_to_roster)
        submit_button.pack(pady=10)

    def open_create_player_window(self,tps_id, callback):
        create_player_window = tk.Toplevel(self.root)
        create_player_window.title("Create New Player")
        create_player_window.geometry("500x600")

        # Non-free shirts
        non_free_shirts = readSQL(database, '''
        SELECT pl.shirt_number, pl.name
        FROM PLAYER pl
        LEFT JOIN TEAM_PLAYER tp ON tp.id_player = pl.id_player
        WHERE tp.id_team_per_season = ?
        ''', (tps_id,))
        non_free = [f"{shirt}" for (shirt, nam) in non_free_shirts]

        # Εμφάνιση μη διαθέσιμων αριθμών
        tk.Label(create_player_window, text=f"Non-available shirts: {', '.join(non_free)}").pack(pady=5)

        # Πεδία για εισαγωγή δεδομένων
        labels = ["Player Name", "Last Name", "Birthday (yyyy-mm-dd)", "Nationality (*=Ελλάδα)", "Position (*=μέσος)", "Shirt Number"]
        entries = {}
        for label in labels:
            tk.Label(create_player_window, text=label).pack(pady=5)
            entry = tk.Entry(create_player_window)
            entry.pack(pady=5)
            entries[label] = entry

        # Συνάρτηση Εκτέλεσης
        def execute_create_player():
            name = entries["Player Name"].get()
            last = entries["Last Name"].get()
            birth = entries["Birthday (yyyy-mm-dd)"].get()
            natio = entries["Nationality (*=Ελλάδα)"].get()
            pos = entries["Position (*=μέσος)"].get()
            shirt_num = entries["Shirt Number"].get()

            if natio == "*":
                natio = "Ελλάδα"
            if pos == "*":
                pos = "μέσος"

            # Βρες το μέγιστο id_player
            max_id_player = readSQL(database, 'SELECT id_player FROM PLAYER ORDER BY id_player DESC LIMIT 1')
            max_id = max_id_player[0][0] if max_id_player else 0

            # Εισαγωγή δεδομένων στη βάση
            ins = {
            "table": "PLAYER",
            "field": ["id_player", "name", "lastname", "birthday", "nationality", "position", "shirt_number"],
            "value": ['?', '?', '?', '?', '?', '?', '?']
            }
            writeSQL(database, insert(ins), (max_id + 1, name, last, birth, natio, pos, shirt_num))
            messagebox.showinfo("Success", "Player created successfully!")
            callback(self,max_id + 1)
            create_player_window.destroy()
            #return max_id + 1

        # Κουμπί Εκτέλεσης
        execute_button = tk.Button(create_player_window, text="Create Player", command=execute_create_player)
        execute_button.pack(pady=10)

    def open_change_password_window(self):
        # Δημιουργία παραθύρου
        change_password_window = tk.Toplevel(self.root)
        change_password_window.title("Change Password")
        change_password_window.geometry("400x200")

        # Ετικέτα και πεδίο εισαγωγής για νέο password
        tk.Label(change_password_window, text="Enter new password:").pack(pady=10)
        password_entry = tk.Entry(change_password_window, show="*")
        password_entry.pack(pady=10)

        # Συνάρτηση εκτέλεσης της αλλαγής password
        def execute_change_password():
            new_password = password_entry.get()  # Παίρνουμε το νέο password από το Entry

            if not new_password:  # Αν δεν εισαχθεί τίποτα
                messagebox.showerror("Error", "Password cannot be empty!")
                return

            # Ενημέρωση password στη βάση
            set_pass = {
            "table": "USER",
            "set": [('password', '?')],
            "where": [('username', '=', '?')]
            }
            writeSQL(database, update(set_pass), (new_password, current_user))  # Ενημερώνουμε τη βάση
            messagebox.showinfo("Success", "Password changed successfully!")  # Εμφάνιση επιτυχίας
            change_password_window.destroy()  # Κλείσιμο παραθύρου

        # Δημιουργία κουμπιού για αλλαγή password
        change_button = tk.Button(change_password_window, text="Change Password", command=execute_change_password)
        change_button.pack(pady=10)

    def open_create_user_window(self):
        # Δημιουργία παραθύρου
        create_user_window = tk.Toplevel(self.root)
        create_user_window.title("Create Roster Admin")
        create_user_window.geometry("400x300")

        # Έλεγχος αν ο τρέχων χρήστης είναι admin
        if current_user_role != "admin":
            messagebox.showerror("Error", "You do not have permission to create a roster admin!")
            create_user_window.destroy()
            return

        # Ετικέτες και πεδία για username και password
        tk.Label(create_user_window, text="Enter username:").pack(pady=10)
        username_entry = tk.Entry(create_user_window)
        username_entry.pack(pady=10)

        tk.Label(create_user_window, text="Enter password:").pack(pady=10)
        password_entry = tk.Entry(create_user_window, show="*")
        password_entry.pack(pady=10)

        # Συνάρτηση για τη δημιουργία του χρήστη
        def execute_create_user():
            username = username_entry.get()
            password = password_entry.get()

            if not username or not password:
                messagebox.showerror("Error", "Both fields are required!")
                return

            # Έλεγχος αν υπάρχει ήδη το username
            existing = readSQL(database, "SELECT username FROM USER WHERE username = ?", (username,))
            if len(existing) > 0:
                messagebox.showerror("Error", "Username already exists!")
                return

            # Δημιουργία του νέου χρήστη
            new_user = {
            "table": "USER",
            "field": ["username", "password", "role"],
            "value": ["?", "?", "?"]
            }
            writeSQL(database, insert(new_user), (username, password, "roster_admin"))
            messagebox.showinfo("Success", "Roster admin created successfully!")
            create_user_window.destroy()

        # Κουμπί καταχώρησης
        create_button = tk.Button(create_user_window, text="Create Roster Admin", command=execute_create_user)
        create_button.pack(pady=20)

    def open_delete_user_window(self):
        # Δημιουργία παραθύρου
        delete_user_window = tk.Toplevel(self.root)
        delete_user_window.title("Delete Roster Admin")
        delete_user_window.geometry("400x200")

        # Έλεγχος αν ο τρέχων χρήστης είναι admin
        if current_user_role != "admin":
            messagebox.showerror("Error", "You do not have permission to delete a roster admin!")
            delete_user_window.destroy()
            return

        # Ετικέτες και πεδία για το username
        tk.Label(delete_user_window, text="Enter username of roster_admin to delete:").pack(pady=10)
        username_entry = tk.Entry(delete_user_window)
        username_entry.pack(pady=10)

        # Συνάρτηση για τη διαγραφή του χρήστη
        def execute_delete_user():
            username = username_entry.get()

            if not username:
                messagebox.showerror("Error", "Username is required!")
                return

            # Διαγραφή του χρήστη
            usr = {
            "table": "USER",
            "where": [("username", "=", "?")]
            }
            result = writeSQL(database, delete(usr), (username,))
        
            if result:
                messagebox.showinfo("Success", f"User '{username}' deleted successfully!")
            else:
                messagebox.showerror("Error", f"User '{username}' could not be found or deleted.")
        
            delete_user_window.destroy()

        # Κουμπί διαγραφής
        delete_button = tk.Button(delete_user_window, text="Delete Roster Admin", command=execute_delete_user)
        delete_button.pack(pady=20)
        
# Εκκίνηση της εφαρμογής
app = ChampionshipApp()
