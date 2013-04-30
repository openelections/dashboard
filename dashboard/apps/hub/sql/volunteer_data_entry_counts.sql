select * from hub_elecdata e
/*

select u.username, count(e.id)
from hub_elecdata e
join auth_user u on e.user_id = u.id 
group by 1
order by 2 desc
--where 
--e.state_id not in ('VA', 'OH', 'FL')
;


/* Team Serdar */
select u.username, count(e.id)
from hub_elecdata e
join auth_user u on e.user_id = u.id 
where u.username in ('dtonyan', 'apalazzolo', 'avestal','anovikova', 'chopkins')
group by 1
order by 2 desc
;

/* Team Derek */
select u.username, count(e.id)
from hub_elecdata e
join auth_user u on e.user_id = u.id 
where u.username in ('sschaver', 'dhill', 'ewyogle', 'jkao', 'jmax')
group by 1
order by 2 desc
;

/* grant total */
select count(*) from hub_elecdata;

/* total by volunteers */
select u.username, count(e.id)
from hub_elecdata e
join auth_user u on e.user_id = u.id 
where e.state_id not in ('VA', 'DC', 'OH', 'FL',)

/* total for the day */
select u.username, count(e.id)
from hub_elecdata e
join auth_user u on e.user_id = u.id 
where e.state_id not in ('VA', 'DC', 'OH', 'FL', 'ME')
;