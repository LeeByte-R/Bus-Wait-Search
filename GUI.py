import tkinter as tk
import bus
from tkinter import ttk
from operator import itemgetter


class UI:
    def __init__(self):
        self.root = tk.Tk()

        bus.read_bus_data()
        print("reading bus data")
        self.path_data = []
        self.begin = ""
        self.end = ""
        self.sort_by = ""
        self.trend = ""

        self.topf = tk.Frame(self.root)
        self.topf.pack()
        self.midf = tk.Frame(self.root)
        self.midf.pack()
        self.bottomf = tk.Frame(self.root)
        self.bottomf.pack()

        # initialize top frame
        self.input_begin = tk.StringVar()
        self.input_begin.set("")
        self.input0 = tk.Entry(self.topf, width=20, textvariable=self.input_begin)
        self.input0.pack(side="left")

        self.text0 = tk.StringVar()
        self.text0.set("  -->>  ")
        self.label0 = tk.Label(self.topf, textvariable=self.text0)
        self.label0.pack(side="left")

        self.input_end = tk.StringVar()
        self.input_end.set("")
        self.input1 = tk.Entry(self.topf, width=20, textvariable=self.input_end)
        self.input1.pack(side="left")

        # initialize middle frame
        self.text1 = tk.StringVar()
        self.text1.set("sort by  ")
        self.label1 = tk.Label(self.midf, textvariable=self.text1)
        self.label1.pack(side="left")

        self.combobox_sort = ttk.Combobox(self.midf, values=["等車時間", "到達時間", "搭車時間"], state="readonly")
        self.combobox_sort.current(0)
        self.combobox_sort.pack(side="left")

        self.text2 = tk.StringVar()
        self.text2.set("  trend  ")
        self.label2 = tk.Label(self.midf, textvariable=self.text2)
        self.label2.pack(side="left")

        self.combobox_trend = ttk.Combobox(self.midf, values=["小到大", "大到小"], state="readonly")
        self.combobox_trend.current(0)
        self.combobox_trend.pack(side="left")

        self.btn_update = tk.Button(self.midf, text='update', fg='blue', command=self.update_data)
        self.btn_update.pack(side="left")

        # initialize bottom frame
        self.bus_text = []
        for i in range(5):
            tmp = tk.StringVar()
            tmp.set("")
            tmp_label = tk.Label(self.bottomf, textvariable=tmp)
            tmp_label.pack()
            self.bus_text.append(tmp)

    def update_data(self):
        self.begin = self.input_begin.get()
        self.end = self.input_end.get()
        self.sort_by = self.combobox_sort.get()
        self.trend = self.combobox_trend.get()
        print(f"{self.begin} -->> {self.end}  sort by {self.sort_by}  trend {self.trend}")

        self.path_data = bus.get_path_data(self.begin, self.end)

        if self.sort_by == "等車時間":
            self.path_data = sorted(self.path_data, key=itemgetter(4))
        elif self.sort_by == "到達時間":
            self.path_data = sorted(self.path_data, key=itemgetter(5))
        else:
            self.path_data = sorted(self.path_data, key=itemgetter(6))

        if self.trend == "大到小":
            self.path_data = self.path_data[::-1]

        # print(self.path_data)
        for i in range(5):
            if i >= len(self.path_data):
                self.bus_text[i].set("")
            else:
                self.bus_text[i].set(self.bus_format(self.path_data[i]))

    @staticmethod
    def bus_format(data):
        return f"{data[1]}  {data[2]}  {data[3]}  等車:{data[7]}  到達:{data[8]}  搭車:{data[9]}"
