import telepot
import time
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox

key = 'iWHxRae9KbCbGsyVmmxDQL8uPvZMz%2Fv25C0qYAYXEJdi8xhlFNRXke9ZK4V4XZ1ELISh%2BhJnC3ib21UOO70qgw%3D%3D'  # 서비스 키를 입력해주세요
bot_token = '6136759904:AAFY_MIKXQzLsZn6CGArmPjooXnbTNSG7I8'  # 텔레그램 봇 토큰을 입력해주세요


class BusBot:
    def __init__(self):
        self.bot = telepot.Bot(bot_token)
        self.bot.message_loop(self.handle)

    def handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if content_type == 'text':
            bus_num = msg['text']
            route_id = self.getBusRouteId(bus_num)

            if route_id is not None:
                station_list = self.getStationList(route_id)
                response = f"버스 노선도 정보\n\n버스 번호: {bus_num}\n\n"
                for direction, stations in station_list.items():
                    response += f"운행 방향: {direction}\n"
                    for station in stations:
                        response += f"- {station}\n"
                    response += "\n"
                self.bot.sendMessage(chat_id, response)
            else:
                self.bot.sendMessage(chat_id, "해당하는 버스 번호를 찾을 수 없습니다.")

    def getBusRouteId(self, strSrch):
        try:
            html = requests.get('http://ws.bus.go.kr/api/rest/busRouteInfo/getBusRouteList',
                                params={'ServiceKey': key, 'strSrch': strSrch}).text
            root = BeautifulSoup(html, 'html.parser')
            loc = root.find('busrouteid')
            return loc.string
        except Exception as e:
            print(e)
            return None

    def getStationList(self, routeid):
        html = requests.get('http://ws.bus.go.kr/api/rest/busRouteInfo/getStaionByRoute',
                            params={'ServiceKey': key, 'busRouteId': routeid}).text
        root = BeautifulSoup(html, 'html.parser')
        items = root.find_all('itemlist')
        direction_list = []
        station_list = {}
        for item in items:
            direction = item.find('direction').string
            station_name = item.find('stationnm').string
            if direction not in direction_list:
                direction_list.append(direction)
                station_list[direction] = []
            station_list[direction].append(station_name)
        return station_list


if __name__ == "__main__":
    bus_bot = BusBot()
    print("BusBot is running...")

    while True:
        try:
            time.sleep(10)
        except KeyboardInterrupt:
            print("\nBusBot stopped.")
            break
        except Exception as e:
            print("An error occurred:", str(e))
            break
