import datetime


def redis_user_stats_datetime(format: str = "%Y_%m_%d_%H_%M") -> str:
	"""Returns user_stats_cache datetime
	"""
	date_and_time = datetime.datetime.now().strftime(format=format)
	# XXX (ames0k0)
	#	-	Stats will be generated per 10 minutes
	#	-	`09` -> `00`
	return "".join((
		date_and_time[:-1],
		"0",
	))