select g.tournamentcode, g.seriescode, g.groupcode, gr.roundcode , count(grr.playercode) as last_round_player_qty
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
order by tournamentcode, seriescode;
