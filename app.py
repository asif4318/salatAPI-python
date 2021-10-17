import math
from time import time
import pytz
import datetime
from flask import Flask

app = Flask(__name__)


def get_julian_date() -> int:
    """
        Calculates today's Julian Date and returns an integer representation
    """
    currentDate = datetime.datetime.now()
    currentDate = currentDate.timetuple()
    julianDate = currentDate.tm_yday
    return(julianDate)

# Equation of Time Calculation
#def get_eot() -> float:
    eot = -23.45 * math.cos(360/365*(get_julian_date()+10))
    return eot

def get_eot() -> float:
    B = math.radians((get_julian_date()-1)*(360/365))
    E = 229.2*(0.000075 + 0.001868*math.cos(B) - 0.032077*math.sin(B) - 0.014615*math.cos(2*B) - 0.04089*math.sin(2*B))
    return E

print(get_eot())

# Using ISNA degree calculates for Fajr & Isha: 15 degrees


# def get_dhuhr(lng, timeZone):
#     dhuhr_time_raw = 12 + timeZone - lng/15 - (get_eot())/60
#     print(dhuhr_time_raw)
#     dhuhr_time = datetime.time(math.floor(dhuhr_time_raw//1), math.ceil(dhuhr_time_raw%1*60), 0)
#     return dhuhr_time
def is_dst(zone):
    now = pytz.utc.localize(datetime.datetime.utcnow())
    return now.astimezone(zone).dst() != datetime.timedelta(0)


def get_dhuhr(longitude:float, time_zone_offset:int, timezone: datetime.datetime.tzinfo) -> datetime.datetime:
    standard_meridian = time_zone_offset * 15 #degrees
    offset = 4*(standard_meridian-longitude) + get_eot() #minutes
    standard_time = 12 - offset/60 #hours
    #Convert hours to time
    now = datetime.datetime.now()
    hours = math.floor(standard_time//1)
    if is_dst(timezone) == True:
        hours += 1

    min = math.ceil(standard_time%1*60) + 1

    dhuhr_datetime = datetime.datetime.now().replace(hour=hours, minute=min, second=0, microsecond=0)
    return dhuhr_datetime

#Dhuhr time for greenwhich not accounting for DST
est = pytz.timezone('US/Eastern')
print(get_dhuhr(82.3, 5, pytz.utc).time())
#print(get_dhuhr(82.3,5))
