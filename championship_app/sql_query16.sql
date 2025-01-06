/*SELECT DISTINCT l.name AS league_name, cl.name AS club_name --μόνο για εντός έδρας ματς
FROM TEAM_PER_SEASON AS t
JOIN CLUB AS cl ON t.EPO_id = cl.EPO_id
JOIN LEAGUE AS l ON t.id_league = l.id_league
WHERE NOT EXISTS (
    SELECT 1
    FROM MATCH AS m
    WHERE m.id_team_home = t.id_team_per_season
      AND NOT EXISTS (
          SELECT 1
          FROM MATCH_RESULT AS mr
          WHERE mr.id_match = m.id_match
            AND mr.id_team_home = t.id_team_per_season
            AND mr.goal_home_over > 0
      )
)
AND EXISTS (
    SELECT 1
    FROM MATCH AS m2
    WHERE m2.id_team_home = t.id_team_per_season
);*/
SELECT DISTINCT l.name AS league_name, cl.name AS club_name
FROM (TEAM_PER_SEASON AS t JOIN CLUB AS cl ON t.EPO_id = cl.EPO_id JOIN LEAGUE AS l ON t.id_league = l.id_league)
WHERE NOT EXISTS (
    SELECT 1
    FROM MATCH AS m
    WHERE (m.id_team_home = t.id_team_per_season) --OR m.id_team_guest = t.id_team_per_season)
      AND NOT EXISTS (
          SELECT 1
          FROM MATCH_RESULT AS mr
          WHERE mr.id_match = m.id_match
            AND (
                (mr.id_team_home = t.id_team_per_season AND mr.goal_home_over > 0)
                /*OR
                (mr.id_team_guest = t.id_team_per_season AND mr.goal_guest_over > 0)*/
            )
      )
)
AND EXISTS ( --για να διασφαλίζει ότι έχει συμμετάσχει σε ματς (όταν θα μπουν τα δεδομένα λογικά δεν θα χρειάζεται)
    SELECT 1
    FROM MATCH AS m2
    WHERE m2.id_team_home = t.id_team_per_season OR m2.id_team_guest = t.id_team_per_season
);							   
