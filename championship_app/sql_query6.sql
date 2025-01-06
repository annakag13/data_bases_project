SELECT l.name, GROUP_CONCAT(' (' || t.id_team_per_season || ' , ' || t.EPO_id || ' , ' || cl.name || ')') as teams
FROM ((TEAM_PER_SEASON as t join CLUB as cl on t.EPO_id = cl.EPO_id) JOIN LEAGUE as l on t.id_league = l.id_league)
GROUP BY l.name
