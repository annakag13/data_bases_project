CREATE VIEW MATCH_RESULT AS
SELECT m.id_match, m.id_team_home, m.id_team_guest,COALESCE((SELECT count(pg.id_goal)
													FROM ((PLAYER_GOAL as pg JOIN GOAL as g on pg.id_goal = g.id_goal) JOIN TEAM_PLAYER as tp on tp.id_player = pg.id_player)
													WHERE tp.id_team_per_season = m.id_team_home AND g.type = "γκολ_υπέρ" AND pg.id_match = m.id_match
													GROUP BY pg.id_match),0) as goal_home_over,
													COALESCE((SELECT count(pg1.id_goal)
													FROM ((PLAYER_GOAL as pg1 JOIN GOAL as g1 on pg1.id_goal = g1.id_goal) JOIN TEAM_PLAYER as tp1 on tp1.id_player = pg1.id_player)
													WHERE tp1.id_team_per_season = m.id_team_home AND g1.type = "αυτογκόλ" AND pg1.id_match = m.id_match
													GROUP BY pg1.id_match),0) as goal_home_against,
													COALESCE((SELECT count(pg2.id_goal)
													FROM ((PLAYER_GOAL as pg2 JOIN GOAL as g2 on pg2.id_goal = g2.id_goal) JOIN TEAM_PLAYER as tp2 on tp2.id_player = pg2.id_player)
													WHERE tp2.id_team_per_season = m.id_team_guest AND g2.type = "γκολ_υπέρ" AND pg2.id_match = m.id_match
													GROUP BY pg2.id_match),0) as goal_guest_over,
													COALESCE((SELECT count(pg3.id_goal)
													FROM ((PLAYER_GOAL as pg3 JOIN GOAL as g3 on pg3.id_goal = g3.id_goal) JOIN TEAM_PLAYER as tp3 on tp3.id_player = pg3.id_player)
													WHERE tp3.id_team_per_season = m.id_team_guest AND g3.type = "αυτογκόλ" AND pg3.id_match = m.id_match
													GROUP BY pg3.id_match),0) as goal_guest_against
FROM MATCH as m