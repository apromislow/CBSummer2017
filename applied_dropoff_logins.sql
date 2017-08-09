select count( distinct mems_with_widgets.id)
	, date_trunc('month', daily_logins.login_date) as login_mon
from mems_with_widgets
	, daily_logins
	, application_status
where mems_with_widgets.member_since = '2016-09-01'
and mems_with_widgets.id = daily_logins.id 
and mems_with_widgets.id = application_status.user_id

group by login_mon;