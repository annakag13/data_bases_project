/*SELECT s.year, l.name, p.id_player, p.name, p.lastname, count(pg.id_goal) as goals_over, cl.name as club_name
FROM(((((((PLAYER as p JOIN PLAYER_GOAL as pg on p.id_player = pg.id_player) JOIN GOAL as g on pg.id_goal = g.id_goal) JOIN TEAM_PLAYER as tp on tp.id_player = p.id_player)JOIN TEAM_PER_SEASON as t on t.id_team_per_season = tp.id_team_per_season)JOIN CLUB as cl on cl.EPO_id = t.EPO_id)JOIN LEAGUE as l on l.id_league = t.id_league)join season as s on s.id_season = t.id_season)
WHERE g.type = "γκολ_υπέρ"
GROUP BY p.id_player
ORDER BY l.name,count(pg.id_goal) desc*/
WITH RankedPlayers AS (
    SELECT 
        s.year, 
        l.name AS league_name, 
        p.id_player, 
        p.name AS player_name, 
        p.lastname, 
        COUNT(pg.id_goal) AS goals_over, 
        cl.name AS club_name,
        ROW_NUMBER() OVER (PARTITION BY l.name ORDER BY COUNT(pg.id_goal) DESC,p.lastname) AS rank
    FROM PLAYER AS p
    JOIN PLAYER_GOAL AS pg ON p.id_player = pg.id_player
    JOIN GOAL AS g ON pg.id_goal = g.id_goal
    JOIN TEAM_PLAYER AS tp ON tp.id_player = p.id_player
    JOIN TEAM_PER_SEASON AS t ON t.id_team_per_season = tp.id_team_per_season
    JOIN CLUB AS cl ON cl.EPO_id = t.EPO_id
    JOIN LEAGUE AS l ON l.id_league = t.id_league
    JOIN SEASON AS s ON s.id_season = t.id_season
    WHERE g.type = "γκολ_υπέρ"
    GROUP BY s.year, l.name, p.id_player, p.name, p.lastname, cl.name
)
SELECT 
    year, 
    league_name, 
    id_player, 
    player_name, 
    lastname, 
    goals_over, 
    club_name
FROM RankedPlayers
WHERE rank <= 10
ORDER BY league_name, rank;