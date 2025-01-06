BEGIN TRANSACTION;
DROP TABLE IF EXISTS "SEASON";
CREATE TABLE IF NOT EXISTS "SEASON"(
	"id_season" INTEGER NOT NULL DEFAULT '0',
	"start" date DEFAULT NULL,
	"end" date DEFAULT NULL,
	"year" varchar(4) DEFAULT NULL,
	PRIMARY KEY ("id_season")
);

DROP TABLE IF EXISTS "LEAGUE_PER_SEASON";
CREATE TABLE IF NOT EXISTS "LEAGUE_PER_SEASON"(
	"id_season" INTEGER NOT NULL DEFAULT '0',
	"id_league" INTEGER NOT NULL DEFAULT '0',
	CONSTRAINT "περιλαμβάνει_περίοδο" FOREIGN KEY("id_season") REFERENCES "SEASON"("id_season") ON UPDATE CASCADE,
	CONSTRAINT "περιλαμβάνει_κατηγ" FOREIGN KEY("id_league") REFERENCES "LEAGUE"("id_league") ON UPDATE CASCADE,
	PRIMARY KEY("id_season","id_league")
);

DROP TABLE IF EXISTS "COACH";
CREATE TABLE IF NOT EXISTS "COACH"(
	"name" varchar(15) NOT NULL DEFAULT '',
	"lastname" varchar(20) NOT NULL DEFAULT '',
	"id_team_per_season" INTEGER NOT NULL DEFAULT '0',
	"start_date" date DEFAULT NULL,
	"end_date" date DEFAULT NULL,
	CONSTRAINT "προπονητής_id_ομ" FOREIGN KEY("id_team_per_season") REFERENCES "TEAM_PER_SEASON"("id_team_per_season") ON DELETE SET DEFAULT ON UPDATE CASCADE,
	PRIMARY KEY("name","lastname","id_team_per_season")
);

DROP TABLE IF EXISTS "CLUB";
CREATE TABLE IF NOT EXISTS "CLUB"(
	"name" varchar(30) NOT NULL DEFAULT '',
	"EPS_id" INTEGER DEFAULT NULL,
	"EPO_id" INTEGER DEFAULT NULL, 
	"city" varchar(20) NOT NULL DEFAULT '',
	"phone" INTEGER DEFAULT NULL,
	"establish_date" date DEFAULT NULL,
	PRIMARY KEY("EPO_id")
);
DROP TABLE IF EXISTS "ARENA";
CREATE TABLE IF NOT EXISTS "ARENA"(
	"name" varchar(30) NOT NULL DEFAULT '',
	"id_arena" INTEGER NOT NULL DEFAULT '0',
	"city" varchar(20) NOT NULL DEFAULT '',
	"address"  varchar(25) DEFAULT NULL,
	"type" varchar(30) NOT NULL DEFAULT '' CHECK("type" in ("Συνθετικός χλοοτάπητας","Φυσικός χλοοτάπητας","Ξερό")),
	PRIMARY KEY("id_arena")
);
DROP TABLE IF EXISTS "MATCHWEEK";
CREATE TABLE IF NOT EXISTS "MATCHWEEK"(
	"id_matchweek" INTEGER NOT NULL DEFAULT '0',
	"round" INTEGER NOT NULL DEFAULT '0' CHECK("round" BETWEEN 1 AND 30),
	"id_season" INTEGER NOT NULL DEFAULT '0',
	"id_league" INTEGER NOT NULL DEFAULT '0',
	"start_date" date DEFAULT NULL,
	"end_date" date DEFAULT NULL,
	CONSTRAINT "αγωνιστική_περίοδο" FOREIGN KEY("id_season") REFERENCES "SEASON"("id_season") ON UPDATE CASCADE,
	CONSTRAINT "αγωνιστική_κατηγ" FOREIGN KEY("id_league") REFERENCES "LEAGUE"("id_league") ON UPDATE CASCADE,
	PRIMARY KEY("id_matchweek")
);
DROP TABLE IF EXISTS "LEAGUE";
CREATE TABLE IF NOT EXISTS "LEAGUE"(
	"name" varchar(1) NOT NULL CHECK("name" IN ('Α','Β','Γ')),
	"id_league" INTEGER NOT NULL DEFAULT '0',
	"group" varchar(2) NOT NULL CHECK("group" IN ('Α')),
	PRIMARY KEY("id_league")
);
DROP TABLE IF EXISTS "TEAM_PER_SEASON";
CREATE TABLE IF NOT EXISTS "TEAM_PER_SEASON"(
	"id_team_per_season" INTEGER NOT NULL DEFAULT '0',
	"id_season" INTEGER NOT NULL DEFAULT '0',
	"id_league" INTEGER NOT NULL DEFAULT '0',
	"EPO_id" INTEGER DEFAULT NULL,
	"id_arena" INTEGER NOT NULL DEFAULT '0',
	CONSTRAINT "ομάδα_ανά_σεζόν_περίοδος" FOREIGN KEY("id_season") REFERENCES "SEASON"("id_season") ON UPDATE CASCADE,
	CONSTRAINT "ομάδα_ανά_σεζόν_κατηγ" FOREIGN KEY("id_league") REFERENCES "LEAGUE"("id_league") ON UPDATE CASCADE,
	CONSTRAINT "ομάδα_ανά_σεζόν_ον_σωματείου" FOREIGN KEY("EPO_id") REFERENCES "CLUB"("EPO_id") ON UPDATE CASCADE,
	CONSTRAINT "ομάδα_ανά_σεζόν_id_γηπέδου" FOREIGN KEY("id_arena") REFERENCES "ARENA"("id_arena") ON UPDATE CASCADE,
	PRIMARY KEY("id_team_per_season")
);
DROP TABLE IF EXISTS "PUNISHMENT";
CREATE TABLE IF NOT EXISTS "PUNISHMENT"(
	"id_punishment" INTEGER NOT NULL DEFAULT '0',
	"reason" text DEFAULT '',
	"duration" TEXT NOT NULL DEFAULT '',
	"money_penalty" INTEGER DEFAULT '0',
	"points_penalty" INTEGER DEFAULT '0',
	PRIMARY KEY("id_punishment")
	CHECK (
		(reason = 'βίαιη συμπεριφορά' AND 
		 points_penalty >= 3 AND 
		 money_penalty >= 500)
		OR
		(reason = 'υβριστική συμπεριφορά' AND 
		 points_penalty >= 1 AND 
		 money_penalty < 500)
		OR
		(reason NOT IN ('βίαιη συμπεριφορά', 'υβριστική συμπεριφορά')) -- Αν η reason δεν είναι καμία από αυτές, δεν υπάρχουν περιορισμοί
	)
);
DROP TABLE IF EXISTS "TEAM_PUNISHMENT";
CREATE TABLE IF NOT EXISTS "TEAM_PUNISHMENT"(
	"id_team_per_season" INTEGER NOT NULL DEFAULT '0',
	"id_punishment" INTEGER NOT NULL DEFAULT '0',
	"punishment_date" date NOT NULL DEFAULT '',
	CONSTRAINT "λαμβάνει_id_ομ" FOREIGN KEY("id_team_per_season") REFERENCES "TEAM_PER_SEASON"("id_team_per_season") ON DELETE SET DEFAULT ON UPDATE CASCADE,
	CONSTRAINT "λαμβάνει_id_punishment" FOREIGN KEY("id_punishment") REFERENCES "PUNISHMENT"("id_punishment") ON UPDATE CASCADE,
	PRIMARY KEY("id_team_per_season","id_punishment")
);
DROP TABLE IF EXISTS "TEAM_PLAYER";
CREATE TABLE IF NOT EXISTS "TEAM_PLAYER"(
	"id_team_per_season" INTEGER NOT NULL DEFAULT '0',
	"id_player" INTEGER NOT NULL DEFAULT '0',
	"start_date" date DEFAULT NULL,
	"end_date" date DEFAULT NULL,
	CONSTRAINT "ανήκει_σε_id_ομ" FOREIGN KEY("id_team_per_season") REFERENCES "TEAM_PER_SEASON"("id_team_per_season") ON DELETE SET DEFAULT ON UPDATE CASCADE,
	CONSTRAINT "ανήκει_σε_id_ποδοσφ" FOREIGN KEY("id_player") REFERENCES "PLAYER"("id_player") ON UPDATE CASCADE,
	PRIMARY KEY("id_team_per_season","id_player")
);
DROP TABLE IF EXISTS "PLAYER_GOAL";
CREATE TABLE IF NOT EXISTS "PLAYER_GOAL" (
	"id_match" INTEGER NOT NULL DEFAULT '0',
	"id_player" INTEGER NOT NULL DEFAULT '0',
	"id_goal" INTEGER NOT NULL DEFAULT '0',
	"minute" INTEGER NOT NULL DEFAULT '' CHECK("minute" BETWEEN 0 AND 90),
	CONSTRAINT "πετυχαίνει_αγώνα" FOREIGN KEY("id_match") REFERENCES "MATCH"("id_match") ON UPDATE CASCADE,
	CONSTRAINT "πετυχαίνει_ποδοσφαίριστή" FOREIGN KEY("id_player") REFERENCES "PLAYER"("id_player") ON UPDATE CASCADE,
	CONSTRAINT "πετυχαίνει_γκολ" FOREIGN KEY("id_goal") REFERENCES "GOAL"("id_goal") ON UPDATE CASCADE,
	PRIMARY KEY ("id_match","id_player","id_goal","minute")
);
DROP TABLE IF EXISTS "GOAL";
CREATE TABLE IF NOT EXISTS "GOAL" (
	"id_goal" INTEGER NOT NULL DEFAULT '0',
	"type" INTEGER NOT NULL DEFAULT '' CHECK("type" in ("γκολ_υπέρ","αυτογκόλ")),
	PRIMARY KEY ("id_goal")
);
DROP TABLE IF EXISTS "PLAYER_CARD";
CREATE TABLE IF NOT EXISTS "PLAYER_CARD" (
	"id_match" INTEGER NOT NULL DEFAULT '0',
	"id_player" INTEGER NOT NULL DEFAULT '0',
	"id_card" INTEGER NOT NULL DEFAULT '0',
	"minute" INTEGER NOT NULL DEFAULT ''CHECK("minute" BETWEEN 0 AND 90),
	CONSTRAINT "δέχεται_αγώνα" FOREIGN KEY("id_match") REFERENCES "MATCH"("id_match") ON UPDATE CASCADE,
	CONSTRAINT "δέχεται_ποδοσφαίριστή" FOREIGN KEY("id_player") REFERENCES "PLAYER"("id_player") ON UPDATE CASCADE,
	CONSTRAINT "δέχεται_γκολ" FOREIGN KEY("id_card") REFERENCES "CARD"("id_card") ON UPDATE CASCADE,
	PRIMARY KEY ("id_match","id_player","id_card","minute")
);
DROP TABLE IF EXISTS "CARD";
CREATE TABLE IF NOT EXISTS "CARD" (
	"id_card" INTEGER NOT NULL DEFAULT '0',
	"type" varchar(10) NOT NULL DEFAULT '' CHECK("type" in ("κίτρινη","κόκκινη")),
	PRIMARY KEY ("id_card")
);
DROP TABLE IF EXISTS "PLAYER_PARTICIPATION";
CREATE TABLE IF NOT EXISTS "PLAYER_PARTICIPATION" (
	"id_match" INTEGER NOT NULL DEFAULT '0',
	"id_player" INTEGER NOT NULL DEFAULT '0', 
	"id_participation" INTEGER NOT NULL DEFAULT '0',
	CONSTRAINT "έχει_αγώνα" FOREIGN KEY("id_match") REFERENCES "MATCH"("id_match") ON UPDATE CASCADE,
	CONSTRAINT "έχει_ποδοσφαίριστή" FOREIGN KEY("id_player") REFERENCES "PLAYER"("id_player") ON UPDATE CASCADE,
	CONSTRAINT "έχει_συμμετοχή" FOREIGN KEY("id_participation") REFERENCES "PARTICIPATION"("id_participation") ON UPDATE CASCADE,
	PRIMARY KEY ("id_match","id_player","id_participation")
);
DROP TABLE IF EXISTS "PARTICIPATION";
CREATE TABLE IF NOT EXISTS "PARTICIPATION" (
	"id_participation" INTEGER NOT NULL DEFAULT '0',
	"minute_in" INTEGER NOT NULL DEFAULT ''CHECK("minute_in" BETWEEN 0 AND 90),
	"minute_out" INTEGER NOT NULL DEFAULT ''CHECK("minute_out" BETWEEN 1 AND 90),
	PRIMARY KEY ("id_participation")
);
DROP TABLE IF EXISTS "PLAYER";
CREATE TABLE IF NOT EXISTS "PLAYER" (
	"id_player" INTEGER NOT NULL DEFAULT '0',
	"name" varchar(15) NOT NULL DEFAULT '',
	"lastname" varchar(15) NOT NULL DEFAULT '',
	"player_number" INTEGER NOT NULL DEFAULT '',
	"birthday" date NOT NULL DEFAULT '',
	"nationality" varchar(15) NOT NULL DEFAULT '',
	"shirt_number" INTEGER NOT NULL DEFAULT '' CHECK("shirt_number" BETWEEN 1 and 99),
	"height" REAL NOT NULL DEFAULT '',
	"position" varchar(15) NOT NULL DEFAULT '' CHECK("position" in ("τερματοφύλακας","αμυντικός","μέσος","επιθετικός")),
	PRIMARY KEY ("id_player")
);
DROP TABLE IF EXISTS "MATCH";
CREATE TABLE IF NOT EXISTS "MATCH" (
	"id_match" INTEGER NOT NULL DEFAULT '0',
	"id_matchweek" INTEGER NOT NULL DEFAULT '0',
	"match_date" date NOT NULL DEFAULT '',
	"match_time" time NOT NULL DEFAULT '',
	"id_team_home" INTEGER NOT NULL DEFAULT '0'CHECK("id_team_home" != "id_team_guest"),
	"id_team_guest" INTEGER NOT NULL DEFAULT '0',
	"referee" varchar(30) NOT NULL DEFAULT '',
	"assistant_referee1" varchar(30) NOT NULL DEFAULT '',
	"assistant_referee2" varchar(30) NOT NULL DEFAULT '',
	CONSTRAINT "αγώνας_αγωνιστική" FOREIGN KEY("id_matchweek") REFERENCES "MATCHWEEK"("id_matchweek") ON UPDATE CASCADE,
	CONSTRAINT "αγώνας_ομάδα_εντός" FOREIGN KEY("id_team_home") REFERENCES "TEAM_PER_SEASON"("id_team_per_season") ON UPDATE CASCADE,
	CONSTRAINT "αγώνας_ομάδα_εκτός" FOREIGN KEY("id_team_guest") REFERENCES "TEAM_PER_SEASON"("id_team_per_season") ON UPDATE CASCADE,
	PRIMARY KEY ("id_match")
);
CREATE TRIGGER check_team_categories
BEFORE INSERT ON "MATCH"
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'Οι ομάδες δεν ανήκουν στην ίδια κατηγορία')
    WHERE (SELECT l.name 
           FROM (TEAM_PER_SEASON AS tp JOIN LEAGUE AS l on tp.id_league = l.id_league)
           WHERE tp.id_team_per_season = NEW."id_team_home") 
          != 
          (SELECT l1.name 
           FROM (TEAM_PER_SEASON AS tp1 JOIN LEAGUE AS l1 on tp1.id_league = l1.id_league) 
           WHERE tp1.id_team_per_season = NEW."id_team_guest");
END;
/*CREATE TRIGGER check_player_eligibility
AFTER INSERT ON "PLAYER_PARTICIPATION"
FOR EACH ROW
BEGIN
  =-- Ενημέρωση του δικαιώματος συμμετοχής αν υπάρχει κόκκινη κάρτα στην προηγούμενη αγωνιστική
  UPDATE "PLAYER_PARTICIPATION"
  SET "δικαίωμα_συμμετοχής" = 0
  WHERE "id_player" = NEW."id_player"
    AND EXISTS (
      SELECT 1
      FROM "CARD" AS K
      JOIN "PLAYER_CARD" AS Δ ON K."id_card" = Δ."id_card"
      JOIN "MATCH" AS A ON A."id_match" = Δ."id_match"
      WHERE Δ."id_player" = NEW."id_player"
        AND K."type" = 'κόκκινη'
        AND A."round" = (
          SELECT "round" - 1
          FROM "MATCH"
          WHERE "id_match" = NEW."id_match"
        )
    );
END;*/
END;	

INSERT INTO "SEASON" ("id_season", "start", "end", "year") VALUES
(1, '2023-09-01', '2024-05-31', '2023'),
(2, '2024-09-01', '2025-05-31', '2024'),
(3, '2025-09-01', '2026-05-31', '2025');
INSERT INTO "ARENA" ("name", "id_arena", "city", "address", "type") VALUES
('Παναχαϊκή', 1, 'Πάτρα', 'Οδός Παναχαϊκής 1', 'Φυσικός χλοοτάπητας'),
('ΑΕΚ Πατρών', 2, 'Πάτρα', 'Οδός ΑΕΚ 2', 'Συνθετικός χλοοτάπητας'),
('Ατρόμητος Πατρών', 3, 'Πάτρα', 'Οδός Ατρόμητου 3', 'Φυσικός χλοοτάπητας'),
('Θύελλα Πατρών', 4, 'Πάτρα', 'Οδός Θύελλας 4', 'Ξερό'),
('Δόξα Παραλίας', 5, 'Πάτρα', 'Οδός Δόξας 5', 'Συνθετικός χλοοτάπητας'),
('Αναγέννηση Πατρών', 6, 'Πάτρα', 'Οδός Αναγέννησης 6', 'Φυσικός χλοοτάπητας'),
('Απόλλων Εγλυκάδας', 7, 'Πάτρα', 'Οδός Απόλλωνα 7', 'Ξερό'),
('ΑΕ Αρόης', 8, 'Πάτρα', 'Οδός Αρόης 8', 'Συνθετικός χλοοτάπητας'),
('Πανμοβριακός Ριόλου', 9, 'Ριόλος', 'Οδός Πανμοβριακού 9', 'Φυσικός χλοοτάπητας'),
('Αχαϊκή', 10, 'Κάτω Αχαΐα', 'Οδός Αχαϊκής 10', 'Ξερό'),
('Διαγόρας Βραχνεΐκων', 11, 'Βραχνέικα', 'Οδός Διαγόρα 11', 'Συνθετικός χλοοτάπητας'),
('Αστέρας Τσουκαλεΐκων', 12, 'Τσουκαλέικα', 'Οδός Αστέρα 12', 'Φυσικός χλοοτάπητας'),
('Πείρος Ισώματος', 13, 'Ισώματα', 'Οδός Πείρου 13', 'Ξερό'),
('ΑΟ Δρεπάνου', 14, 'Δρέπανο', 'Οδός Δρεπάνου 14', 'Συνθετικός χλοοτάπητας'),
('ΑΟ Πάτρας', 15, 'Πάτρα', 'Οδός ΑΟ Πάτρας 15', 'Φυσικός χλοοτάπητας'),
('ΑΕ Ροϊτίκων', 16, 'Ροΐτικα', 'Οδός ΑΕ Ροϊτίκων 16', 'Ξερό'),
('ΑΟ Σαραβαλίου', 17, 'Σαραβάλι', 'Οδός ΑΟ Σαραβαλίου 17', 'Συνθετικός χλοοτάπητας'),
('ΑΟ Ζαβλανίου', 18, 'Ζαβλάνι', 'Οδός ΑΟ Ζαβλανίου 18', 'Φυσικός χλοοτάπητας'),
('ΑΟ Καστριτσίου', 19, 'Καστρίτσι', 'Οδός ΑΟ Καστριτσίου 19', 'Ξερό'),
('ΑΟ Μιντιλογλίου', 20, 'Μιντιλόγλι', 'Οδός ΑΟ Μιντιλογλίου 20', 'Συνθετικός χλοοτάπητας'),
('ΑΟ Ρίου', 21, 'Ρίο', 'Οδός ΑΟ Ρίου 21', 'Φυσικός χλοοτάπητας'),
('ΑΟ Αγυιάς', 22, 'Αγυιά', 'Οδός ΑΟ Αγυιάς 22', 'Ξερό'),
('ΑΟ Βραχνέικων', 23, 'Βραχνέικα', 'Οδός ΑΟ Βραχνέικων 23', 'Συνθετικός χλοοτάπητας'),
('ΑΟ Κάτω Αχαΐας', 24, 'Κάτω Αχαΐα', 'Οδός ΑΟ Κάτω Αχαΐας 24', 'Φυσικός χλοοτάπητας'),
('ΑΟ Παραλίας', 25, 'Παραλία', 'Οδός ΑΟ Παραλίας 25', 'Ξερό'),
('ΑΟ Ριόλου', 26, 'Ριόλος', 'Οδός ΑΟ Ριόλου 26', 'Συνθετικός χλοοτάπητας'),
('ΑΟ Εγλυκάδας', 27, 'Εγλυκάδα', 'Οδός ΑΟ Εγλυκάδας 27', 'Φυσικός χλοοτάπητας'),
('ΑΟ Αρόης', 28, 'Αρόη', 'Οδός ΑΟ Αρόης 28', 'Ξερό'),
('ΑΟ Ισώματος', 29, 'Ισώματα', 'Οδός ΑΟ Ισώματος 29', 'Συνθετικός χλοοτάπητας'),
('ΑΟ Δρεπάνου', 30, 'Δρέπανο', 'Οδός ΑΟ Δρεπάνου 30', 'Φυσικός χλοοτάπητας'),
('ΑΟ Πάτρας', 31, 'Πάτρα', 'Οδός ΑΟ Πάτρας 31', 'Ξερό'),
('ΑΟ Ροϊτίκων', 32, 'Ροΐτικα', 'Οδός ΑΟ Ροϊτίκων 32', 'Συνθετικός χλοοτάπητας'),
('ΑΟ Σαραβαλίου', 33, 'Σαραβάλι', 'Οδός ΑΟ Σαραβαλίου 33', 'Φυσικός χλοοτάπητας'),
('ΑΟ Ζαβλανίου', 34, 'Ζαβλάνι', 'Οδός ΑΟ Ζαβλανίου 34', 'Ξερό'),
('ΑΟ Καστριτσίου', 35, 'Καστρίτσι', 'Οδός ΑΟ Καστριτσίου 35', 'Συνθετικός χλοοτάπητας'),
('ΑΟ Μιντιλογλίου', 36, 'Μιντιλόγλι', 'Οδός ΑΟ Μιντιλογλίου 36', 'Φυσικός χλοοτάπητας');
INSERT INTO "LEAGUE" ("name", "id_league", "group") VALUES
('Α', 1, 'Α'),
('Β', 2, 'Α'),
('Γ', 3, 'Α');
INSERT INTO "CLUB" ("name", "EPS_id", "EPO_id", "city", "phone", "establish_date") VALUES
('Παναχαϊκή', 1, 101, 'Πάτρα', 2610223344, '1891-06-14'),
('ΑΕΚ Πατρών', 1, 102, 'Πάτρα', 2610223345, '1929-05-01'),
('Ατρόμητος Πατρών', 1, 103, 'Πάτρα', 2610223346, '1926-03-25'),
('Θύελλα Πατρών', 1, 104, 'Πάτρα', 2610223347, '1930-04-10'),
('Δόξα Παραλίας', 1, 105, 'Πάτρα', 2610223348, '1950-09-15'),
('Αναγέννηση Πατρών', 1, 106, 'Πάτρα', 2610223349, '1960-11-20'),
('Απόλλων Εγλυκάδας', 1, 107, 'Πάτρα', 2610223350, '1970-02-18'),
('ΑΕ Αρόης', 1, 108, 'Πάτρα', 2610223351, '1980-07-22'),
('Πανμοβριακός Ριόλου', 1, 109, 'Ριόλος', 2610223352, '1990-08-30'),
('Αχαϊκή', 1, 110, 'Κάτω Αχαΐα', 2610223353, '1920-12-05'),
('Διαγόρας Βραχνεΐκων', 1, 111, 'Βραχνέικα', 2610223354, '1960-01-15'),
('Αστέρας Τσουκαλεΐκων', 1, 112, 'Τσουκαλέικα', 2610223355, '1975-04-05'),
('Πείρος Ισώματος', 1, 113, 'Ισώματα', 2610223356, '1985-06-10'),
('ΑΟ Δρεπάνου', 1, 114, 'Δρέπανο', 2610223357, '1995-09-25'),
('ΑΟ Πάτρας', 1, 115, 'Πάτρα', 2610223358, '2000-03-12'),
('ΑΕ Ροϊτίκων', 1, 116, 'Ροΐτικα', 2610223359, '2005-07-18'),
('ΑΟ Σαραβαλίου', 1, 117, 'Σαραβάλι', 2610223360, '2010-11-22'),
('ΑΟ Ζαβλανίου', 1, 118, 'Ζαβλάνι', 2610223361, '2015-02-28'),
('ΑΟ Καστριτσίου', 1, 119, 'Καστρίτσι', 2610223362, '2020-05-15'),
('ΑΟ Μιντιλογλίου', 1, 120, 'Μιντιλόγλι', 2610223363, '2021-08-20'),
('ΑΟ Ρίου', 1, 121, 'Ρίο', 2610223364, '2022-10-30'),
('ΑΟ Αγυιάς', 1, 122, 'Αγυιά', 2610223365, '2023-01-10'),
('ΑΟ Βραχνέικων', 1, 123, 'Βραχνέικα', 2610223366, '2023-03-25'),
('ΑΟ Κάτω Αχαΐας', 1, 124, 'Κάτω Αχαΐα', 2610223367, '2023-06-15'),
('ΑΟ Παραλίας', 1, 125, 'Παραλία', 2610223368, '2023-09-05'),
('ΑΟ Ριόλου', 1, 126, 'Ριόλος', 2610223369, '2023-11-20'),
('ΑΟ Εγλυκάδας', 1, 127, 'Εγλυκάδα', 2610223370, '2024-02-10'),
('ΑΟ Αρόης', 1, 128, 'Αρόη', 2610223371, '2024-04-25'),
('ΑΟ Ισώματος', 1, 129, 'Ισώματα', 2610223372, '2024-07-15'),
('ΑΟ Δρεπάνου', 1, 130, 'Δρέπανο', 2610223373, '2024-09-30'),
('ΑΟ Πάτρας', 1, 131, 'Πάτρα', 2610223374, '2024-12-10'),
('ΑΟ Ροϊτίκων', 1, 132, 'Ροΐτικα', 2610223375, '2025-02-20'),
('ΑΟ Σαραβαλίου', 1, 133, 'Σαραβάλι', 2610223376, '2025-05-05'),
('ΑΟ Ζαβλανίου', 1, 134, 'Ζαβλάνι', 2610223377, '2025-07-25'),
('ΑΟ Καστριτσίου', 1, 135, 'Καστρίτσι', 2610223378, '2025-10-10'),
('ΑΟ Μιντιλογλίου', 1, 136, 'Μιντιλόγλι', 2610223379, '2025-12-30');
INSERT INTO "TEAM_PER_SEASON" ("id_team_per_season", "id_season",  "id_league",  "EPO_id", "id_arena") VALUES
-- Κατηγορία Α
(1, 1,  1,  101, 1),
(2, 1,  1,  102,  2),
(3, 1,  1,  103,  3),
(4, 1,  1,  104,  4),
(5, 1,  1,  105,  5),
(6, 1,  1,  106,  6),
(7, 1,  1,  107,  7),
(8, 1,  1,  108,  8),
(9, 1,  1,  109,  9),
(10, 1,  1,  110,  10),
(11, 1,  1,  111,  11),
(12, 1,  1,  112,  12),

-- Κατηγορία Β
(13, 1,  2,  113,  13),
(14, 1,  2,  114,  14),
(15, 1,  2,  115,  15),
(16, 1,  2,  116,  16),
(17, 1,  2,  117,  17),
(18, 1,  2,  118,  18),
(19, 1,  2,  119,  19),
(20, 1,  2,  120,  20),
(21, 1,  2,  121,  21),
(22, 1,  2,  122,  22),
(23, 1,  2,  123,  23),
(24, 1,  2,  124,  24),

-- Κατηγορία Γ
(25, 1,  3,  125,  25),
(26, 1,  3,  126,  26),
(27, 1,  3,  127,  27),
(28, 1,  3,  128,  28),
(29, 1,  3,  129,  29),
(30, 1,  3,   130,  30),
(31, 1,  3,   131,  31),
(32, 1,  3,   132,  32),
(33, 1,  3,   133,  33),
(34, 1,  3,   134,  34),
(35, 1,  3,   135,  35),
(36, 1,  3,   136,  36);
/*INSERT INTO "TEAM_PER_SEASON" ("id_team_per_season", "id_season", "league_name", "id_league", "name", "EPO_id", "id_arena") VALUES
-- Κατηγορία Α
(37, 2,  1,  101,  1),
(38, 2,  1,  102,  2),
(39, 2,  1,  103,  3),
(40, 2,  1,  104,  4),
(41, 2,  1,  105,  5),
(42, 2,  1,  106,  6),
(43, 2,  1,  107,  7),
(44, 2,  1,  108,  8),
(45, 2,  1,  109,  9),
(46, 2,  1,  110,  10),
(47, 2,  1,  114,  14), -- Από Κατηγορία Β
(48, 2,  1,  115,  15), -- Από Κατηγορία Β

-- Κατηγορία Β
(49, 2,  2,  111,  11), -- Από Κατηγορία Α
(50, 2,  2,  112,  12), -- Από Κατηγορία Α
(51, 2,  2,  113,  13),
(52, 2,  2,  116,  16),
(53, 2,  2,  117,  17),
(54, 2,  2,  118,  18),
(55, 2,  2,  119,  19),
(56, 2,  2,  120,  20),
(57, 2,  2,  121,  21),
(58, 2,  2,  122,  22),
(59, 2,  2,  123,  23),
(60, 2,  2,  124,  24),

-- Κατηγορία Γ
(61, 2,  3,  125,  25),
(62, 2,  3,  126,  26),
(63, 2,  3,  127,  27),
(64, 2,  3,  128,  28),
(65, 2,  3,  129,  29),
(66, 2,  3,  130,  30),
(67, 2,  3,  131,  31),
(68, 2,  3,  132,  32),
(69, 2,  3,  133,  33),
(70, 2,  3,  134,  34),
(71, 2,  3,  135,  35),
(72, 2,  3,  136,  36);