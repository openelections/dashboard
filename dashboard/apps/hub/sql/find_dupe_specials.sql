/* Queries to pinpoint specials from same day for purposes
of collapsing into a single record.

See PivotalTracker for details: 
	https://www.pivotaltracker.com/story/show/50862749
 
*/
/* find duplicate special primaries */
select state_id,  special, race_type, end_date, count(id)
from hub_election 
where special = 't'
and start_date = end_date
group by 1,2,3,4
having count(end_date) > 1
order by state_id, end_date DESC, race_type
;

select count(*)
from hub_election 
where race_type = 'primary'

select * from hub_election limit 10;
