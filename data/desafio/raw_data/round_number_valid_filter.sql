
select g.tournamentcode, g.seriescode, g.groupcode
from 	
	game as g,
		(select tournamentcode, seriescode, max(roundorder) as round_max
			from gameround
			group by tournamentcode, seriescode
		) as rmax,
		(select tournamentcode, seriescode, groupcode, max(roundorder) as r_order
			from gameround
			group by tournamentcode, seriescode, groupcode
		) as rgroup
		
where
	g.tournamentcode = rmax.tournamentcode and
	g.tournamentcode = rgroup.tournamentcode and
	
	g.seriescode = rmax.seriescode and
	g.seriescode = rgroup.seriescode and

	g.groupcode = rgroup.groupcode and
	
	rmax.round_max = rgroup.r_order --apenas jogos com o mesmo número de rodadas que o máximo da série
	
order by tournamentcode, seriescode;
