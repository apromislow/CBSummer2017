SELECT COUNT(DISTINCT id), date_trunc('month', x.member_since) FROM

(SELECT daily_logins.id
	, daily_logins.login_date
	, mems_with_widgets.member_since
FROM
	mems_with_widgets
JOIN 
	daily_logins
ON mems_with_widgets.id = daily_logins.id) as x

group by date_trunc;