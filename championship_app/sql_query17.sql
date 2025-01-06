SELECT mp.year, mp.id_match, mp.league_name, mp.id_player,  mp.player_name,  mp.player_lastname
FROM MATCHES_PLAYERS AS mp
WHERE mp.player_status = 'αλλαγή' AND mp.goals_over >= 1 --AND mp.score <> '0 - 0'
GROUP BY mp.id_match;