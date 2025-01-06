/*WITH result as(
SELECT t.id_team_per_season as id, cl.name as name,l.name as league1, ((SELECT count(mr.id_match)
					 FROM MATCH_RESULT as mr
					 WHERE mr.id_team_home = t.id_team_per_season AND (mr.goal_home_over + mr.goal_guest_against)>(mr.goal_guest_over + mr.goal_home_against))
					 +
					 (SELECT count(mr1.id_match)
					 FROM MATCH_RESULT as mr1
					 WHERE mr1.id_team_guest = t.id_team_per_season AND (mr1.goal_home_over + mr1.goal_guest_against)<(mr1.goal_guest_over + mr1.goal_home_against))) as win,
				((SELECT count(mr2.id_match)
					 FROM MATCH_RESULT as mr2
					 WHERE mr2.id_team_home = t.id_team_per_season AND (mr2.goal_home_over + mr2.goal_guest_against)<(mr2.goal_guest_over + mr2.goal_home_against))
					 +
					 (SELECT count(mr3.id_match)
					 FROM MATCH_RESULT as mr3
					 WHERE mr3.id_team_guest = t.id_team_per_season AND (mr3.goal_home_over + mr3.goal_guest_against)>(mr3.goal_guest_over + mr3.goal_home_against))) as defeat,
				((SELECT count(mr4.id_match)
					 FROM MATCH_RESULT as mr4
					 WHERE mr4.id_team_home = t.id_team_per_season AND (mr4.goal_home_over + mr4.goal_guest_against)=(mr4.goal_guest_over + mr4.goal_home_against))
					 +
					 (SELECT count(mr5.id_match)
					 FROM MATCH_RESULT as mr5
					 WHERE mr5.id_team_guest = t.id_team_per_season AND (mr5.goal_home_over + mr5.goal_guest_against)=(mr5.goal_guest_over + mr5.goal_home_against))) as draw,
				(SELECT count(m.id_match)
				FROM match as m 
				WHERE m.id_team_home = t.id_team_per_season or m.id_team_guest = t.id_team_per_season) as matches,				
				(COALESCE((SELECT SUM(mres.goal_home_over + mres.goal_guest_against)
						   FROM MATCH_RESULT AS mres
						   WHERE mres.id_team_home = t.id_team_per_season), 0)
				+
				 COALESCE((SELECT SUM(mres1.goal_guest_over + mres1.goal_home_against)
						  FROM MATCH_RESULT AS mres1
						  WHERE mres1.id_team_guest = t.id_team_per_season), 0)) AS goal_over,
				 (COALESCE((SELECT SUM(mres2.goal_guest_over + mres2.goal_home_against)
						   FROM MATCH_RESULT AS mres2
						   WHERE mres2.id_team_home = t.id_team_per_season), 0)
				+
				  COALESCE((SELECT SUM(mres3.goal_home_over + mres3.goal_guest_against)
						  FROM MATCH_RESULT AS mres3
						  WHERE mres3.id_team_guest = t.id_team_per_season), 0)) AS goal_against
FROM ((TEAM_PER_SEASON as t join CLUB as cl on t.EPO_id = cl.EPO_id) JOIN LEAGUE as l on t.id_league = l.id_league))
--CREATE VIEW "RANKING" AS
SELECT r.id, r.name, r.league1, r.matches, (3 * r.win + 1 * r.draw - COALESCE((SELECT SUM(p.points_penalty) 
																			  FROM TEAM_PUNISHMENT AS tp 
																			  JOIN PUNISHMENT AS p ON tp.id_punishment = p.id_punishment
																			  WHERE tp.id_team_per_season = r.id), 0)) AS points, r.win, r.defeat, r.draw, r.goal_over, r.goal_against
FROM result AS r
ORDER BY league1, points DESC;*/
/*CREATE VIEW RANKING AS
SELECT 
	r.year,
	r.league1,
    r.id, 
    r.name, 
    r.matches, 
    (3 * r.win + 1 * r.draw - COALESCE((SELECT SUM(p.points_penalty) 
                                         FROM TEAM_PUNISHMENT AS tp 
                                         JOIN PUNISHMENT AS p ON tp.id_punishment = p.id_punishment
                                         WHERE tp.id_team_per_season = r.id), 0)) AS points, 
    r.win, 
    r.defeat, 
    r.draw, 
    r.goal_over, 
    r.goal_against
FROM (
    SELECT 
        s.year,t.id_team_per_season AS id, 
        cl.name AS name, 
        l.name AS league1,
        ((SELECT COUNT(mr.id_match)
          FROM MATCH_RESULT AS mr
          WHERE mr.id_team_home = t.id_team_per_season AND 
                (mr.goal_home_over + mr.goal_guest_against) > (mr.goal_guest_over + mr.goal_home_against)) +
         (SELECT COUNT(mr1.id_match)
          FROM MATCH_RESULT AS mr1
          WHERE mr1.id_team_guest = t.id_team_per_season AND 
                (mr1.goal_home_over + mr1.goal_guest_against) < (mr1.goal_guest_over + mr1.goal_home_against))) AS win,
        ((SELECT COUNT(mr2.id_match)
          FROM MATCH_RESULT AS mr2
          WHERE mr2.id_team_home = t.id_team_per_season AND 
                (mr2.goal_home_over + mr2.goal_guest_against) < (mr2.goal_guest_over + mr2.goal_home_against)) +
         (SELECT COUNT(mr3.id_match)
          FROM MATCH_RESULT AS mr3
          WHERE mr3.id_team_guest = t.id_team_per_season AND 
                (mr3.goal_home_over + mr3.goal_guest_against) > (mr3.goal_guest_over + mr3.goal_home_against))) AS defeat,
        ((SELECT COUNT(mr4.id_match)
          FROM MATCH_RESULT AS mr4
          WHERE mr4.id_team_home = t.id_team_per_season AND 
                (mr4.goal_home_over + mr4.goal_guest_against) = (mr4.goal_guest_over + mr4.goal_home_against)) +
         (SELECT COUNT(mr5.id_match)
          FROM MATCH_RESULT AS mr5
          WHERE mr5.id_team_guest = t.id_team_per_season AND 
                (mr5.goal_home_over + mr5.goal_guest_against) = (mr5.goal_guest_over + mr5.goal_home_against))) AS draw,
        (SELECT COUNT(m.id_match)
         FROM MATCH AS m 
         WHERE m.id_team_home = t.id_team_per_season OR m.id_team_guest = t.id_team_per_season) AS matches,				
        (COALESCE((SELECT SUM(mres.goal_home_over + mres.goal_guest_against)
                   FROM MATCH_RESULT AS mres
                   WHERE mres.id_team_home = t.id_team_per_season), 0) +
         COALESCE((SELECT SUM(mres1.goal_guest_over + mres1.goal_home_against)
                   FROM MATCH_RESULT AS mres1
                   WHERE mres1.id_team_guest = t.id_team_per_season), 0)) AS goal_over,
        (COALESCE((SELECT SUM(mres2.goal_guest_over + mres2.goal_home_against)
                   FROM MATCH_RESULT AS mres2
                   WHERE mres2.id_team_home = t.id_team_per_season), 0) +
         COALESCE((SELECT SUM(mres3.goal_home_over + mres3.goal_guest_against)
                   FROM MATCH_RESULT AS mres3
                   WHERE mres3.id_team_guest = t.id_team_per_season), 0)) AS goal_against
    FROM TEAM_PER_SEASON AS t
    JOIN CLUB AS cl ON t.EPO_id = cl.EPO_id
    JOIN LEAGUE AS l ON t.id_league = l.id_league
	JOIN SEASON AS s ON t.id_season = s.id_season
) AS r 
ORDER BY r.year, r.league1, points DESC;*/
CREATE VIEW RANKING AS
WITH MatchStats AS (
    SELECT 
        t.id_team_per_season AS id,
        -- Νίκες
        SUM(CASE 
                WHEN mr.id_team_home = t.id_team_per_season 
                     AND (mr.goal_home_over + mr.goal_guest_against) > (mr.goal_guest_over + mr.goal_home_against) THEN 1
                WHEN mr.id_team_guest = t.id_team_per_season 
                     AND (mr.goal_home_over + mr.goal_guest_against) < (mr.goal_guest_over + mr.goal_home_against) THEN 1
                ELSE 0
            END) AS win,
        -- Ήττες
        SUM(CASE 
                WHEN mr.id_team_home = t.id_team_per_season 
                     AND (mr.goal_home_over + mr.goal_guest_against) < (mr.goal_guest_over + mr.goal_home_against) THEN 1
                WHEN mr.id_team_guest = t.id_team_per_season 
                     AND (mr.goal_home_over + mr.goal_guest_against) > (mr.goal_guest_over + mr.goal_home_against) THEN 1
                ELSE 0
            END) AS defeat,
        -- Ισοπαλίες
        SUM(CASE 
                WHEN (mr.id_team_home = t.id_team_per_season OR mr.id_team_guest = t.id_team_per_season) 
                     AND (mr.goal_home_over + mr.goal_guest_against) = (mr.goal_guest_over + mr.goal_home_against) THEN 1
                ELSE 0
            END) AS draw,
        -- Σύνολο Αγώνων
        COUNT(mr.id_match) AS matches,
        -- Γκολ Υπέρ
        SUM(CASE 
                WHEN mr.id_team_home = t.id_team_per_season THEN (mr.goal_home_over + mr.goal_guest_against)
                WHEN mr.id_team_guest = t.id_team_per_season THEN (mr.goal_guest_over + mr.goal_home_against)
                ELSE 0
            END) AS goal_over,
        -- Γκολ Κατά
        SUM(CASE 
                WHEN mr.id_team_home = t.id_team_per_season THEN (mr.goal_guest_over + mr.goal_home_against)
                WHEN mr.id_team_guest = t.id_team_per_season THEN (mr.goal_home_over + mr.goal_guest_against)
                ELSE 0
            END) AS goal_against
    FROM TEAM_PER_SEASON AS t
    LEFT JOIN MATCH_RESULT AS mr ON t.id_team_per_season IN (mr.id_team_home, mr.id_team_guest)
    GROUP BY t.id_team_per_season
),
Penalties AS (
    SELECT 
        tp.id_team_per_season, 
        SUM(p.points_penalty) AS points_penalty
    FROM TEAM_PUNISHMENT AS tp
    JOIN PUNISHMENT AS p ON tp.id_punishment = p.id_punishment
    GROUP BY tp.id_team_per_season
),
TeamInfo AS (
    SELECT 
        t.id_team_per_season AS id, 
        cl.name AS name, 
        l.name AS league1, 
        s.year
    FROM TEAM_PER_SEASON AS t
    JOIN CLUB AS cl ON t.EPO_id = cl.EPO_id
    JOIN LEAGUE AS l ON t.id_league = l.id_league
    JOIN SEASON AS s ON t.id_season = s.id_season
)
SELECT 
    ti.year,
    ti.league1,
    ti.id,
    ti.name,
    ms.matches,
    (3 * ms.win + ms.draw - COALESCE(p.points_penalty, 0)) AS points,
    ms.win,
    ms.defeat,
    ms.draw,
    ms.goal_over,
    ms.goal_against
FROM TeamInfo AS ti
LEFT JOIN MatchStats AS ms ON ti.id = ms.id
LEFT JOIN Penalties AS p ON ti.id = p.id_team_per_season
ORDER BY ti.year, ti.league1, points DESC;





