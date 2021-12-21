# Function to normalize the date and time, which is created by using the python module "time", according to the
# description in the Feature "SCHATSI002"
def time_analysis(timestamp):

    day = timestamp[8:10]
    month = timestamp[4:7]

    if month == "Jan":
        month = "01"
    elif month == "Feb":
        month = "02"
    elif month == "Mar":
        month = "03"
    elif month == "Apr":
        month = "04"
    elif month == "May":
        month = "05"
    elif month == "Jun":
        month = "06"
    elif month == "Jul":
        month = "07"
    elif month == "Aug":
        month = "08"
    elif month == "Sep":
        month = "09"
    elif month == "Oct":
        month = "10"
    elif month == "Nev":
        month = "11"
    elif month == "Dec":
        month = "12"

    year = timestamp[20:24]
    hour = timestamp[11:13]
    minute = timestamp[14:16]
    second = timestamp[17:19]
    # normalized String: DD.MM.YYYY HH:MM:SS
    time_string = day + "." + month + "." + year + " " + hour + ":" + minute + ":" + second
    return time_string


# Function for the calculation of the duration of the whole program. It takes two timestamps and calculates the
# duration in minutes (one timestamp at the beginning of the program and another at the end
def duration_calc(timestamp1_normalized, timestamp2_normalized):
    # normalized String: DD.MM.YYYY HH:MM:SS
    # duration is needed in minutes --> MM

    start_time = timestamp1_normalized[11:19]
    finish_time = timestamp2_normalized[11:19]

    start_hour = int(start_time[0:2])
    finish_hour = int(finish_time[0:2])
    start_minute = int(start_time[4:6])
    finish_minute = int(finish_time[4:6])
    start_second = int(start_time[7:9])
    finish_second = int(finish_time[7:9])

    # hour -> 60 minutes + minutes + 1 minute, if there are more than 30 seconds left
    duration = (finish_hour - start_hour)*60 + (finish_minute - start_minute)
    if (finish_second - start_second) >= 30:
        duration = duration + 1
    return duration

