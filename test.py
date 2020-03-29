from datetime import datetime

end_time = '2020-03-29T13:05:35.000Z'
time_left = 'P0DT0H37M45S'

# end_time_1 = end_time.isoformat(" ", "seconds")
end_time_1 = datetime.(end_time)
# end_time_2 = datetime.fromisoformat(end_time)
print(end_time_1)
# print(end_time_2)