import pandas as pd
import csv
import time

url = f"https://user.frdm.info/ckhung/saas/bus/taichung/timing4.php?timeformat=1&refresh=1&reverse=0&hidecar=1&dark=0"
df = pd.read_html(url)[2].values.tolist()
# print(pd.read_html(url)[2])

with open('bus.csv', 'w', newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['路線編號', '路線', '路線名稱', '站序', '中文站點名', '去回'])

    index = 1
    for path in df:
        time.sleep(1.0)
        url = f"https://user.frdm.info/ckhung/saas/bus/taichung/timing4.php?rid={path[0]}&timeformat=1&refresh=1&hidecar=1"
        path_data = pd.read_html(url)[3].values.tolist()
        i = 1
        for departure in path_data:
            if departure[0] != '↓':
                writer.writerow([path[0], path[1], path[2], str(i), departure[1], '去程'])
                i += 1
        i = 1
        return_path = path_data[::-1]
        for return_ in return_path:
            if return_[2] != '↑':
                writer.writerow([path[0], path[1], path[2], str(i), return_[1], '回程'])
                i += 1
        print(index)
        index += 1

