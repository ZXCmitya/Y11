from datetime import timedelta, datetime, timezone
# import tzlocal
# import pytz

import time

tz = -time.timezone
print(tz / 60)
print(f'Часы: {tz // 3600}, Минуты: {int(tz / 3600 % 1 * 60)}')
tz_hours = tz // 3600
tz_minutes = int(tz / 3600 % 1 * 60)

# local_datetime = datetime.now()
# local_iso_str = datetime.strftime(local_datetime, '%d.%m.%y %H:%M:%S')
utc_datetime = datetime.now(timezone.utc)

# print(utc_datetime + timedelta(hours=tz_hours, minutes=tz_minutes))

datetime_str = datetime.strftime(utc_datetime, '%d.%m.%y %H:%M:%S')
print(datetime_str)  # в бд по utc

datetime_object = (datetime.strptime(datetime_str, '%d.%m.%y %H:%M:%S')
                   + timedelta(hours=tz_hours, minutes=tz_minutes))  # формат datetime для добавления offset'а

print(datetime_object)

datetime_str = datetime.strftime(datetime_object, '%d.%m.%y %H:%M:%S')  # выводим в карточку

print(datetime_str)
# datetime_str = local_iso_str
#
# datetime_object = datetime.strptime(datetime_str, '%d.%m.%y %H:%M:%S')
#
# print(timezone.utc)


# tz_London = pytz.timezone('Europe/London')
# datetime_London = datetime.now(tz_London)
# print(datetime_London)
# print(tz_London)
# print(tz_London)
#
# print(local_datetime)
# print(utc_datetime)
# print(local_iso_str)
# print(datetime_object + timedelta(hours=2))
# print(datetime_str)
#
#
# utc_iso_str = datetime.strftime(utc_datetime, "%Y-%m-%dT%H:%M:%S")[:-3]
#
#
# print(utc_iso_str)
#
# print(f"local dt: {local_iso_str}, tzname: {local_datetime.tzname()}")
# print(f"  utc dt: {utc_iso_str}, tzname: {utc_datetime.tzname()}")
#
# print("\n")
#
# print(f"local dt: {local_datetime.isoformat()}")
# print(f"  utc dt: {utc_datetime.isoformat()}")