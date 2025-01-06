/*SELECT s.year, l.name, mw.round, m.match_date, cl.name, p.name, p.lastname, ((mr.goal_home_over + mr.goal_guest_against) || ' - ' || (mr.goal_guest_over + mr.goal_home_against)) as score, (pa.minute_out - pa.minute_in) as minutes_of_participation, count(pg.id_goal), SUM(CASE WHEN pc.id_card = 1 THEN 1 ELSE 0 END) AS yellow_cards, SUM(CASE WHEN pc.id_card = 2 THEN 1 ELSE 0 END) AS red_cards
FROM((((((((((((MATCH as m JOIN MATCHWEEK as mw on m.id_matchweek = mw.id_matchweek)JOIN SEASON as s on mw.id_season = s.id_season)JOIN league as l on l.id_league = mw.id_league)JOIN TEAM_PER_SEASON as t on (t.id_team_per_season = m.id_team_home or t.id_team_per_season = m.id_team_guest))join club as cl on cl.EPO_id = t.EPO_id) JOIN TEAM_PLAYER as tp on tp.id_team_per_season = t.id_team_per_season) join PLAYER as p on p.id_player = tp.id_player)JOIN PLAYER_GOAL as pg on pg.id_player = p.id_player)JOIN PLAYER_CARD as pc on pc.id_player = p.id_player)JOIN MATCH_RESULT as mr on m.id_match = mr.id_match)JOIN PLAYER_PARTICIPATION as pp on pp.id_player = p.id_player) JOIN PARTICIPATION as pa on pp.id_participation = pa.id_participation)
GROUP BY cl.name;*/
CREATE VIEW MATCHES_PLAYERS AS
SELECT 
    s.year, 
    l.name AS league_name, 
	m.id_match,
    m.match_date, 
    cl.name AS club_name, 
	t.id_team_per_season,
	p.id_player,
    p.name AS player_name, 
    p.lastname AS player_lastname, 
    ((mr.goal_home_over + mr.goal_guest_against) || ' - ' || (mr.goal_guest_over + mr.goal_home_against)) AS score, 
    (pa.minute_out - pa.minute_in) AS minutes_of_participation, 
	SUM(CASE WHEN pg.id_goal = 1 THEN 1 ELSE 0 END) AS goals_over,
	SUM(CASE WHEN pg.id_goal = 2 THEN 1 ELSE 0 END) AS goals_against,
    SUM(CASE WHEN pc.id_card = 1 THEN 1 ELSE 0 END) AS yellow_cards, 
    SUM(CASE WHEN pc.id_card = 2 THEN 1 ELSE 0 END) AS red_cards,
	CASE 
        WHEN pa.minute_in = 0 THEN 'βασικός' 
        ELSE 'αλλαγή' 
    END AS player_status
FROM 
    MATCH AS m
    JOIN MATCHWEEK AS mw ON m.id_matchweek = mw.id_matchweek
    JOIN SEASON AS s ON mw.id_season = s.id_season
    JOIN LEAGUE AS l ON l.id_league = mw.id_league
    JOIN TEAM_PER_SEASON AS t ON (t.id_team_per_season = m.id_team_home OR t.id_team_per_season = m.id_team_guest)
    JOIN CLUB AS cl ON cl.EPO_id = t.EPO_id
    JOIN TEAM_PLAYER AS tp ON tp.id_team_per_season = t.id_team_per_season
    JOIN PLAYER AS p ON p.id_player = tp.id_player
    LEFT JOIN PLAYER_GOAL AS pg ON pg.id_player = p.id_player AND pg.id_match = m.id_match
    LEFT JOIN PLAYER_CARD AS pc ON pc.id_player = p.id_player AND pc.id_match = m.id_match
    JOIN MATCH_RESULT AS mr ON m.id_match = mr.id_match
    JOIN PLAYER_PARTICIPATION AS pp ON pp.id_player = p.id_player AND pp.id_match = m.id_match
    JOIN PARTICIPATION AS pa ON pp.id_participation = pa.id_participation
GROUP BY 
    s.year, 
    l.name, 
    m.match_date, 
	m.id_match,
    cl.name, 
	t.id_team_per_season,
    p.id_player
ORDER BY 
    p.id_player--s.year, l.name, m.match_date, m.id_match, cl.name, p.lastname;