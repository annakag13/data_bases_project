SELECT t.id_team_per_season, cl.name AS team_name, a.name AS arena_name, l.name,(SELECT COUNT(DISTINCT tp_inner.id_player)
																					   FROM TEAM_PLAYER AS tp_inner 
																					   WHERE tp_inner.id_team_per_season = t.id_team_per_season) AS player_count,GROUP_CONCAT(c.coach_info, ', ') AS coaches
FROM ((((TEAM_PER_SEASON AS t JOIN CLUB as cl on t.EPO_id = cl.EPO_id) JOIN LEAGUE as l on l.id_league = t.id_league) JOIN  ARENA AS a ON t.id_arena = a.id_arena) JOIN (SELECT DISTINCT id_team_per_season, 
																																										name || ' ' || lastname || ' (' || start_date || ' - ' || IFNULL(end_date, 'Present') || ')' AS coach_info
																																										FROM COACH) AS c 
																																										ON t.id_team_per_season = c.id_team_per_season)
WHERE player_count <> 0
GROUP BY t.id_team_per_season
ORDER BY t.id_team_per_season;