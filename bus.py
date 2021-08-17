import pandas as pd
import csv
import time

bus_data = []
paths = []
path_data = []


def arrive_time(number, trip, begin, end):
    url = f"https://user.frdm.info/ckhung/saas/bus/taichung/timing4.php?rid={number}&timeformat=1&refresh=0&reverse=0&hidecar=0&dark=0&ivrno=&stopID=&stopName="
    df = pd.read_html(url)[3].values.tolist()
    # print(df)
    minutes = 0
    last_m = 0
    begin_m = 0
    end_m = 0
    begin_s = ""
    end_s = ""
    license_plate = ""
    b = True

    c = '↓'
    plate = 0
    time_ = 1
    if trip == "回程":
        df = df[::-1]
        plate = 4
        time_ = 3
        c = '↑'

    for station in df:
        current_m = convert_minute(station[time_])
        if not b:
            if station[plate] != c and license_plate != station[plate]:
                license_plate = station[plate]
                minutes += last_m
            if station[2] == end:
                minutes += current_m
                end_m = minutes
                if end_m == 0:
                    end_s = "即將到站"
                else:
                    end_s = f"{end_m}分鐘"
                break

        if b and station[2] == begin:
            begin_m = current_m
            license_plate = station[plate]
            if is_minute(station[time_]):
                begin_s = f"{begin_m}分鐘"
            else:
                begin_s = station[time_]
            b = False
        last_m = current_m

    in_bus_m = end_m - begin_m
    in_bus_s = f"{in_bus_m}分鐘"
    print(number, begin_m, end_m, in_bus_m, begin_s, end_s, in_bus_s)
    return begin_m, end_m, in_bus_m, begin_s, end_s, in_bus_s


def is_minute(s):
    if len(s) > 2 and s[:-2].isnumeric():
        return True
    return False


def convert_minute(s):
    m = 0
    if is_minute(s):
        m = int(s[:-2])

    return m


def read_bus_data():
    with open('bus.csv', newline='', encoding="utf-8") as csvfile:
        rows = csv.reader(csvfile)

        next(rows, None)
        next(rows, None)
        tmp = []
        number = '???'
        trip = '???'
        for row in rows:
            if number == row[0] and trip == row[5]:
                tmp.append(row[4])
            else:
                bus_data.append(tmp)
                tmp = []
                number = row[0]
                trip = row[5]
                tmp.append(row[0])
                tmp.append(row[1])
                tmp.append(row[2])
                tmp.append(row[5])
                tmp.append(row[4])

        del bus_data[0]


def in_path(path, begin, end):
    b = True
    in_path_ = False
    for station in path[4:]:
        if b and station == begin:
            b = False
        if not b and station == end:
            in_path_ = True
            break

    return in_path_


def find_path(begin, end):
    paths.clear()
    for path in bus_data:
        if in_path(path, begin, end):
            paths.append(path[:4])


def get_path_data(begin, end):
    path_data.clear()
    find_path(begin, end)
    for path in paths:
        time.sleep(0.5)
        time_data = arrive_time(path[0], path[3], begin, end)

        if time_data[3] == "末班駛離" or time_data[4] == "末班駛離" or time_data[3] == "離站" or time_data[4] == "離站":
            continue
        a = 1
        path_data.append(path + list(time_data))
    print(path_data)
    return path_data


if __name__ == "__main__":
    pass
    # read_bus_data()
    # print(in_path(bus_data[0], '忠明南路', '永春東七路'))
    # arrive_time('324', '回程', '牛頂頭', '台中精機')
    # find_path('臺中教育大學', '北區運動中心')
    # print(paths)
    # print(get_path_data('臺中教育大學', '干城站'))

