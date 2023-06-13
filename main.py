import pandas as pd
import numpy as np
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import xml
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import io
from googlemaps import Client
from tkintermapview import TkinterMapView
import subprocess


key = 'iWHxRae9KbCbGsyVmmxDQL8uPvZMz%2Fv25C0qYAYXEJdi8xhlFNRXke9ZK4V4XZ1ELISh%2BhJnC3ib21UOO70qgw%3D%3D'

class App(tk.Tk):
    WIDTH = 1600
    HEIGHT = 900

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        main_frame = tk.Frame(self)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=0)  # 우측 열은 고정 크기
        main_frame.grid_rowconfigure(0, weight=1)

        left_frame = tk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky="nsew")

        right_frame = tk.Frame(main_frame)
        right_frame.grid(row=0, column=1, sticky="nsew")

        self.search_text = tk.StringVar()

        self.search_bar = tk.Entry(left_frame, textvariable=self.search_text, width=30)
        self.search_bar.grid(row=0, column=0, pady=10, padx=10, sticky="nw")

        self.search_button = tk.Button(left_frame, text="Search", command=self.search_bus)
        self.search_button.grid(row=0, column=1, pady=(10, 0), padx=10, sticky="nw")

        self.station_list = tk.Listbox(left_frame, width=40, height=20)
        self.station_list.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        self.station_list.configure(selectbackground="blue", selectforeground="white")
        self.station_list.bind("<<ListboxSelect>>", self.station_list_select)

        self.map_widget = TkinterMapView(right_frame, width=self.WIDTH, height=self.HEIGHT, corner_radius=0)
        self.map_widget.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")

        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_rowconfigure(1, weight=1)

        left_frame.grid_propagate(0)

        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(0, weight=1)

        # 이미지 추가
        image = Image.open("T_Icon.png")  # 이미지 파일 경로에 맞게 수정
        image = image.resize((50, 50))  # 이미지 크기 조정

        self.image_tk = ImageTk.PhotoImage(image)

        image_label = tk.Label(right_frame, image=self.image_tk)
        image_label.grid(row=1, column=0, pady=10, padx=10, sticky="se")  # 이미지 위치 조정

        image_label.bind("<Button-1>", self.run_python_file)  # 이미지 클릭 이벤트에 함수 연결

    def search_bus(self):
        bus_num = self.search_text.get()
        routeid = self.getBusRouteId(bus_num)
        if routeid:
            self.getStationList(routeid)
            self.map_widget.set_address("서울 강남역")

    def getBusRouteId(self, strSrch):
        html = requests.get(
            'http://ws.bus.go.kr/api/rest/busRouteInfo/getBusRouteList?ServiceKey=' + key + '&strSrch=' + strSrch).text
        root = BeautifulSoup(html, 'html.parser')
        try:  # 존재하지 않는 노선번호를 입력한 경우에 대한 예외처리
            loc = root.find('busrouteid')
            return loc.string
        except Exception as e:
            print(e)
            return None


    def getStationList(self, routeid):
        html = requests.get(
            'http://ws.bus.go.kr/api/rest/busRouteInfo/getStaionByRoute?ServiceKey=' + key + '&busRouteId=' + routeid).text
        root = BeautifulSoup(html, 'html.parser')
        items = root.find_all('itemlist')
        direction = root.find_all('direction')
        self.station_list.delete(0, tk.END)
        for i in set(direction):
            direction_text = i.string
            self.station_list.insert(tk.END, f'======= 운행방향: {direction_text} =======')
            for j in items:
                if j.direction.string == direction_text:
                    station_name = j.stationnm.string
                    self.station_list.insert(tk.END, f'- {station_name}')
            self.station_list.insert(tk.END, '')


    def station_list_select(self, event):
        selected_index = self.station_list.curselection()
        if selected_index:
            station_name = self.station_list.get(selected_index)
            print(f"Clicked station: {station_name}")
            self.map_widget.set_address(station_name)

    def run_python_file(self, event):
        subprocess.run(["python", "Teleg.py"])  # 다른 파이썬 파일 실행

if __name__ == "__main__":
    app = App()
    app.mainloop()
