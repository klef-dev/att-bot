from datetime import date, timedelta, time, datetime

today = date.today()
# GETS THE TUESDAY FOR THE WEEK
tuesday = today + timedelta(days=1-today.weekday(), weeks=0)
# GETS THE WEDNESDAY FOR THE WEEK
wednesday = today + timedelta(days=2-today.weekday(), weeks=0)
# GETS THE THURSDAY FOR THE WEEK
thursday = today + timedelta(days=3-today.weekday(), weeks=0)
# GETS THE SUNDAY FOR THE WEEK
sunday = today + timedelta(days=6-today.weekday(), weeks=0)
picking_time = time(18, 00, 30)
date_1 = "{} Service 1"
date_1 = date_1.format(sunday)
date_2 = "{} Service 2"
date_2 = date_2.format(sunday)
service_date = sunday.strftime("%A, %B %d, %Y")
friends = [
    {
        "username": "SURNAME.FIRSTNAME",
        "pw": "PASSWORD",
        "regnum": "REG_NO",
        "date": date_1
    },
    {
        "username": "SURNAME.FIRSTNAME",
        "pw": "PASSWORD",
        "regnum": "REG_NO",
        "date": date_2
    },
    {
        "username": "SURNAME.FIRSTNAME",
        "pw": "PASSWORD",
        "regnum": "REG_NO",
        "date": date_1
    },
    {
        "username": "SURNAME.FIRSTNAME",
        "pw": "PASSWORD",
        "regnum": "REG_NO",
        "date": date_1
    },
]


def check(self):
    if tuesday == today and picking_time == datetime.now().strftime("%H:%M:%S") or wednesday == today or thursday == today:
        return True
    else:
        return False
