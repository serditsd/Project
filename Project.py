from math import sin, cos, sqrt, atan2, radians
import pandas as pd
import math
from tqdm import tqdm

data = pd.read_csv("day4.csv")
data.dropna()
# list of all time
t = data.time.unique()

# answer variable
confl = []
confl_t = []


def horiz_dist(lat1, lat2, lon1, lon2):
    r = 6373.0
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    dist = r * c  # 1 nm. = 1.852 km

    return dist


def check(lat, lon, baro, callsign):
    count = 0
    for x in range(len(lat)):
        for y in range(len(lat) - (x + 1)):
            # 1 meters = 3.28084 ft.
            if (horiz_dist(lat[x], lat[x + y + 1], lon[x], lon[x + y + 1]) < (3 * 1.852) and abs(
                    baro[x] - baro[x + y + 1]) * 3.28084 < 1000):
                # print("The confliction info at time: " + str(t[z]))
                # print("The Callsign of the 1st plane is " + str(callsign[x]))
                # print("lat1 = " + str(lat[x]))
                # print("lon1 = " + str(lon[x]))
                # print("baro1 = " + str(baro[x]*3.28084))
                # print("The Callsign of the 2nd plane is " + str(callsign[x+y+1]))
                # print("lat2 = " + str(lat[x+y+1]))
                # print("lon2 = " + str(lon[x+y+1]))
                # print("baro2 = " + str(baro[x+y+1]*3.28084))
                confl.append([callsign[x], callsign[x + y + 1]])
                confl_t.append(t[z])


def unique(list1):
    # intilize a null list
    unique_list = []
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
            # print list
    return unique_list


# body
for z in tqdm(range(len(t)), desc="Loading all confliction by time"):
    focus_row = data.loc[data['time'] == t[z]]
    lat = focus_row["lat"].tolist()
    lon = focus_row["lon"].tolist()
    baro = focus_row["baroaltitude"].tolist()
    callsign = focus_row["callsign"].tolist()

    check(lat, lon, baro, callsign)

ans = unique(confl)

print("\nThis are all callsigns that conflict each other.\n")

for u in range(len(ans)):
    print(str(ans[u][0]) + "\tand\t" + str(ans[u][1]))
    for r in range(len(confl)):
        if (confl[r] == ans[u]):
            print('At time: ' + str(confl_t[r]))
            print('---------------------------------------------------- \n')
            break

print('\nAll conflict is ' + str(len(ans)) + ' times')
# print(confl)
# print(confl_t)

