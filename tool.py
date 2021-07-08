def pm_to_am(time_string):
    if time_string[-2]=="A":
        time_string = time_string[:-2]
        hour_minute=time_string.split(":")
        hour_minute_int = [int(hour_minute[0]),int(hour_minute[1])]
        return hour_minute_int
    else:
        time_string = time_string[:-2]
        hour_minute=time_string.split(":")
        hour_minute_int = [int(hour_minute[0]) + 12,int(hour_minute[1])]
        return hour_minute_int

print(pm_to_am("6:00PM"))
