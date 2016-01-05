select t.tournamentcode, t.country, t.refyear, t.gamename, validGames.seriescode, series.seriesorder as fase, validGames.groupcode,
	drama_position.measurevalue as dramaPosition, drama_points.measurevalue as dramaPoints, drama_paths.measurevalue as dramaPaths
from
	(select g.tournamentcode, g.seriescode, g.groupcode, gr.roundcode , count(grr.playercode) as last_round_player_qty
	from 	
		game as g,
		gameround as gr,
		gameroundresult as grr,
			(select tournamentcode, seriescode, max(roundorder) as round_max
				from gameround
				group by tournamentcode, seriescode
			) as rmax,
			(select tournamentcode, seriescode, groupcode, max(roundorder) as r_order
				from gameround
				group by tournamentcode, seriescode, groupcode
			) as rgroup
			
	where
		g.tournamentcode = gr.tournamentcode and
		g.tournamentcode = grr.tournamentcode and
		g.tournamentcode = rmax.tournamentcode and
		g.tournamentcode = rgroup.tournamentcode and
		
		g.seriescode = gr.seriescode and
		g.seriescode = grr.seriescode and
		g.seriescode = rmax.seriescode and
		g.seriescode = rgroup.seriescode and

		g.groupcode = gr.groupcode and
		g.groupcode = grr.groupcode and
		g.groupcode = rgroup.groupcode and
		
		gr.roundcode = grr.roundcode and 
		
		gr.roundorder = rmax.round_max and --para obter o código da última rodada
		rmax.round_max = rgroup.r_order --apenas jogos com o mesmo número de rodadas que o máximo da série
		
	group by
		g.tournamentcode, g.seriescode, g.groupcode, gr.roundcode
	having
		count(grr.playercode) > 1 --apenas jogos com mais de um jogador na última rodada
	order by tournamentcode, seriescode) as validGames,

	tournament as t,
	series,
	(select tournamentcode, seriescode, groupcode, measurevalue 
	from 
		measures as m,
		(select measurecode, max(measureversion) as measure_version 
		from measures
		group by measurecode) as max_version

	where 
		m.measurecode = max_version.measurecode and
		m.measureversion = max_version.measure_version and
		m.measuredescription = 'Drama by position') as drama_position,

	(select tournamentcode, seriescode, groupcode, measurevalue 
	from 
		measures as m,
		(select measurecode, max(measureversion) as measure_version 
		from measures
		group by measurecode) as max_version

	where 
		m.measurecode = max_version.measurecode and
		m.measureversion = max_version.measure_version and
		m.measuredescription = 'Drama by points') as drama_points,

	(select tournamentcode, seriescode, groupcode, measurevalue 
	from 
		measures as m,
		(select measurecode, max(measureversion) as measure_version 
		from measures
		group by measurecode) as max_version

	where 
		m.measurecode = max_version.measurecode and
		m.measureversion = max_version.measure_version and
		m.measuredescription = 'Drama by paths') as drama_paths
	
where
	t.tournamentcode = validGames.tournamentcode and
	t.tournamentcode = series.tournamentcode and
	t.tournamentcode = drama_position.tournamentcode and
	t.tournamentcode = drama_points.tournamentcode and
	t.tournamentcode = drama_paths.tournamentcode and
	
	validGames.seriescode = series.seriescode and
	validGames.seriescode = drama_position.seriescode and
	validGames.seriescode = drama_points.seriescode and
	validGames.seriescode = drama_paths.seriescode and
	
	validGames.groupcode = drama_position.groupcode and
	validGames.groupcode = drama_points.groupcode and
	validGames.groupcode = drama_paths.groupcode
	
order by
	tournamentcode, series.seriesorder;
	
