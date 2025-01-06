SELECT cl.name, cl.EPO_id, p.reason, p.duration, p.money_penalty, p.points_penalty, tp.punishment_date
FROM((((TEAM_PER_SEASON as t JOIN CLUB as cl on t.EPO_id = cl.EPO_id)JOIN TEAM_PUNISHMENT as tp on tp.id_team_per_season = t.id_team_per_season)JOIN PUNISHMENT as p on p.id_punishment = tp.id_punishment)JOIN LEAGUE as l on l.id_league = t.id_league)
ORDER BY cl.name;