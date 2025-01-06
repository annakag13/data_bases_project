/*SELECT r.league1, GROUP_CONCAT(' (' || r.name || ' , ' || r.id || ')') AS promoted_teams, (r.league1 || ' -> ' || (SELECT l.name
																													FROM LEAGUE AS l 
																													WHERE l.id_league = l1.id_league - 1))AS leagues
FROM RANKING AS r 
JOIN LEAGUE AS l1 ON r.league1 = l1.name
WHERE r.id = (SELECT r1.id
            FROM RANKING AS r1
            WHERE r1.league1 = r.league1
            ORDER BY r1.points DESC, (r1.goal_over - r1.goal_against) DESC -- Το καλύτερο goal difference
            LIMIT 1) AND r.league1 <> 'Α' -- Εξαιρεί την πρώτη κατηγορία (δεν έχουμε άνοδο από Α)			  
GROUP BY r.league1;*/

--Ίσως στη μεγάλη βάση να πρέπει να βάλουμε να ελέχει αν έχει τελειώσει η κανονική περίοδος της σεζόν, δηλαδή αν ο αριθμός των ματς για όλες τις ομάδες είναι ίσος με τον συνολικό.

WITH RankedTeams AS (
    SELECT id, league1, name, ROW_NUMBER() OVER (PARTITION BY league1 ORDER BY points DESC, (goal_over - goal_against) DESC, goal_over DESC) AS rank
    FROM RANKING
)
SELECT r.league1, GROUP_CONCAT(' (' || r.name || ' , ' || r.id || ')') AS promoted_teams, (r.league1 || ' -> ' || COALESCE(l_next.name, ''))AS leagues
FROM RankedTeams AS r
JOIN LEAGUE AS l1 ON r.league1 = l1.name
LEFT JOIN LEAGUE AS l_next ON l_next.id_league = l1.id_league - 1
WHERE r.rank = 1 AND r.league1 <> 'Α'
GROUP BY r.league1, l1.id_league;