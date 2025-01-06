SELECT s.year, l.name, cl.name as club_name, p.id_player, p.name, p.lastname, sum(pa.minute_out - pa.minute_in) as participation_minutes, count(pp.id_match) as matches
FROM(((((((PLAYER as p JOIN PLAYER_PARTICIPATION as pp on p.id_player = pp.id_player) JOIN PARTICIPATION as pa on pp.id_participation = pa.id_participation) JOIN TEAM_PLAYER as tp on tp.id_player = p.id_player)JOIN TEAM_PER_SEASON as t on t.id_team_per_season = tp.id_team_per_season)JOIN CLUB as cl on cl.EPO_id = t.EPO_id)JOIN LEAGUE as l on l.id_league = t.id_league)join season as s on s.id_season = t.id_season)
GROUP BY p.id_player
ORDER BY l.id_league,participation_minutes desc, p.lastname ASC;
--LIMIT 10;