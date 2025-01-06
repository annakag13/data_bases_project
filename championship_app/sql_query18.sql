SELECT r.league1, r.id,r.name,((r.win * 100)/r.matches) as percentage_win,((select count(mr.id_match)
																 FROM MATCH_RESULT as mr
																 WHERE (mr.id_team_home = r.id and (mr.goal_home_over + mr.goal_guest_against > mr.goal_guest_over + mr.goal_home_against))) *100/r.win) as percentage_home_win
FROM RANKING as r 
GROUP BY r.id
HAVING ((r.win * 100)/r.matches)>=50;