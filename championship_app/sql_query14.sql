/*select r.league1, GROUP_CONCAT(' (' || r.name || ' , ' ||  r.id || ')') AS relegated_teams, (r.league1 || ' -> ' ||(SELECT l.name
																													FROM LEAGUE as l 
																													WHERE l.id_league = l1.id_league + 1)) as leagues
from (RANKING as r join LEAGUE as l1 on r.league1 = l1.name)
WHERE r.points = (SELECT MIN(r1.points)
				  FROM RANKING as r1
				  WHERE r1.league1 = r.league1)
GROUP BY r.league1*/
/*SELECT r.league1, 
       GROUP_CONCAT(' (' || r.name || ' , ' || r.id || ')') AS relegated_teams, 
       --CASE 
           --WHEN l1.id_league = (SELECT MAX(id_league) FROM LEAGUE) THEN 'αποκλεισμός από το τοπικό' -- ή μπορούμε απλά να μην συμπεριλάβουμε την περίπτωση της τελευταίας ομάδας της γ κατηγορίας
           (r.league1 || ' -> ' || (SELECT l.name
                                          FROM LEAGUE AS l 
                                          WHERE l.id_league = l1.id_league + 1)) as leagues
       --END AS leagues
FROM RANKING AS r 
JOIN LEAGUE AS l1 ON r.league1 = l1.name
WHERE r.points = (SELECT MIN(r1.points)
                  FROM RANKING AS r1
                  WHERE r1.league1 = r.league1) AND r.goal_over - r.goal_against = (SELECT MIN(r2.goal_over - r2.goal_against)
																					FROM RANKING AS r2
																					WHERE r2.league1 = r.league1) and (r.league1 <> 'Γ')
GROUP BY r.league1, l1.id_league;*/
/*SELECT 
    r.league1, 
    GROUP_CONCAT(' (' || r.name || ' , ' || r.id || ')') AS relegated_teams, 
    CASE 
        WHEN l1.id_league = (SELECT MAX(id_league) FROM LEAGUE) THEN 'αποκλεισμός από το τοπικό'
        ELSE (r.league1 || ' -> ' || (SELECT l.name
                                      FROM LEAGUE AS l 
                                      WHERE l.id_league = l1.id_league + 1))
    END AS leagues
FROM RANKING AS r 
JOIN LEAGUE AS l1 ON r.league1 = l1.name
WHERE 
    r.id = (SELECT r1.id
            FROM RANKING AS r1
            WHERE r1.league1 = r.league1
            ORDER BY r1.points ASC, (r1.goal_over - r1.goal_against) DESC,r1.goal_over DESC
            LIMIT 1) -- Επιλέγει τη μία ομάδα με τους λιγότερους πόντους και το μικρότερο goal difference
    AND r.league1 <> 'Γ' -- Εξαιρεί την τελευταία κατηγορία
GROUP BY r.league1, l1.id_league;*/
--Ίσως στη μεγάλη βάση να πρέπει να βάλουμε να ελέχει αν έχει τελειώσει η κανονική περίοδος της σεζόν, δηλαδή αν ο αριθμός των ματς για όλες τις ομάδες είναι ίσος με τον συνολικό.
WITH RankedTeams AS (
    SELECT id, league1, name, ROW_NUMBER() OVER (PARTITION BY league1 ORDER BY points ASC, (goal_over - goal_against) ASC, goal_over DESC) AS rank
    FROM RANKING
)
SELECT r.league1, GROUP_CONCAT(' (' || r.name || ' , ' || r.id || ')') AS relegated_teams, (r.league1 || ' -> ' || COALESCE(l_next.name, ''))AS leagues
FROM RankedTeams AS r
JOIN LEAGUE AS l1 ON r.league1 = l1.name
LEFT JOIN LEAGUE AS l_next ON l_next.id_league = l1.id_league + 1
WHERE r.rank = 1 AND r.league1 <> 'Γ'
GROUP BY r.league1, l1.id_league;