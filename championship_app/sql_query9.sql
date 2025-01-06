SELECT s.year, l.name, p.id_player, p.name, p.lastname, count(pc.id_card) as yellow_cards, cl.name as club_name
FROM(((((((PLAYER as p JOIN PLAYER_CARD as pc on p.id_player = pc.id_player) JOIN CARD as c on pc.id_card = c.id_card) JOIN TEAM_PLAYER as tp on tp.id_player = p.id_player)JOIN TEAM_PER_SEASON as t on t.id_team_per_season = tp.id_team_per_season)JOIN CLUB as cl on cl.EPO_id = t.EPO_id)JOIN LEAGUE as l on l.id_league = t.id_league)join season as s on s.id_season = t.id_season)
WHERE c.type = "κίτρινη"
GROUP BY p.id_player
ORDER BY l.id_league, yellow_cards desc, p.lastname;