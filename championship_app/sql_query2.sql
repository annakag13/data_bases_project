--Α τρόπος (ανάλογα με το τι θέλουμε)
SELECT cl.name,p.id_player, p.name, p.lastname, strftime('%Y', p.birthday) as year_of_birth, p.position
FROM (((TEAM_PER_SEASON as t JOIN CLUB as cl on cl.EPO_id = t.EPO_id) join TEAM_PLAYER as tp on t.id_team_per_season = tp.id_team_per_season) JOIN PLAYER as p on tp.id_player = p.id_player)
ORDER BY cl.name, p.lastname;
/*--Β τρόπος
SELECT cl.name AS team_name,t.id_team_per_season,GROUP_CONCAT(p.lastname || ' ' || p.name || ' (' || strftime('%Y', p.birthday)  || ', ' || p.position || ')', ', ' ORDER BY p.lastname) AS players
FROM (((TEAM_PER_SEASON as t JOIN CLUB as cl on cl.EPO_id = t.EPO_id) join TEAM_PLAYER as tp on t.id_team_per_season = tp.id_team_per_season) JOIN PLAYER as p on tp.id_player = p.id_player)
GROUP BY cl.name,t.id_team_per_season
ORDER BY t.id_team_per_season;