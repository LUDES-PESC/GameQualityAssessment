select g.tournamentcode, g.seriescode, g.groupcode, r_order, round_max as r_series 
from 	
game as g,
	(select tournamentcode, seriescode, max(roundorder) as round_max
		from gameround
		group by tournamentcode, seriescode
		order by tournamentcode, seriescode asc
	) as rmax,
	(select tournamentcode, seriescode, groupcode, max(roundorder) as r_order
		from gameround
		group by tournamentcode, seriescode, groupcode
		order by tournamentcode, seriescode, groupcode asc
	) as rgroup
	
where
g.tournamentcode = rmax.tournamentcode and
g.seriescode = rmax.seriescode and

g.tournamentcode = rgroup.tournamentcode and
g.seriescode = rgroup.seriescode and

g.groupcode = rgroup.groupcode and

rmax.round_max > rgroup.r_order;
