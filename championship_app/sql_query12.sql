SELECT mp.year, mp.id_player, mp.player_name, mp.player_lastname, sum(mp.goals_over), sum(mp.goals_against), sum(mp.yellow_cards), sum(mp.red_cards), sum(mp.minutes_of_participation), count(mp.id_match)
FROM MATCHES_PLAYERS as mp 
GROUP BY mp.year, mp.id_player;
--ORDER BY mp.id_player;
--HAVING sum(mp.goals_over)>0