/* Queries to pinpoint primaries from same day for purposes
of collapsing into a single record. Special elections 
are excluded because they should be itemized.

See PivotalTracker for details: 
   https://www.pivotaltracker.com/story/show/50554855
 
*/
select state_id,  end_date, count(id)
from hub_election 
where race_type = 'primary'
and special = 'f'
and start_date = end_date
group by 1,2
having count(end_date) > 1
order by state_id, end_date DESC
;

select count(*)
from hub_election 
where race_type = 'primary'

select * from hub_election limit 10;