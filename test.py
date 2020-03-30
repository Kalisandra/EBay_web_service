from datetime import datetime, timedelta
import dateutil.parser as dp
import isodate

end_time = '2020-03-29T13:05:35.000Z'
time_left = 'P0DT0H37M45S'


end_time_1 = isodate.parse_datetime(end_time)
end_time_1 = end_time_1.strftime('%Y-%m-%d %H:%M:%S')
print(end_time_1)
print(type(end_time_1))

end_time_2 = str(isodate.parse_duration(time_left))
print(end_time_2)
print(type(end_time_2))
# end_time_2 = str(end_time_2)
# print(end_time_2)
# print(type(end_time_2))