import requests
import os

line_token = os.getenv('LINE_TOKEN')
token_family = os.getenv('TOKEN_FAMILY')

# 檢查 token_family 是否已設置
if token_family is None:
    raise ValueError("TOKEN_FAMILY environment variable is not set.")

url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWA-264D87C4-9C2E-4774-AF87-B987F15828FD'
data = requests.get(url)   # 取得 JSON 檔案的內容為文字
data_json = data.json()    # 轉換成 JSON 格式
location = data_json['records']['location']   # 取出 location 的內容

all_msg = '所有縣市天氣預報🤖(未來6小時): \n'
out_city = '離島縣市天氣預報🤖(未來6小時): \n'
key = " 重點縣市突出🤖(未來6小時): \n\n"

for i in location:
    city = i['locationName']    # 縣市名稱
    if city in ['臺北市','高雄市','屏東縣','嘉義縣']:
        wx8 = i['weatherElement'][0]['time'][0]['parameter']['parameterName']    # 天氣現象
        maxt8 = i['weatherElement'][4]['time'][0]['parameter']['parameterName'] # 最高溫
        mint8 = i['weatherElement'][2]['time'][0]['parameter']['parameterName'] # 最低溫
        pop8 = i['weatherElement'][1]['time'][0]['parameter']['parameterName'] # 降雨機率
        msg = f'{city}🌚天氣: {wx8}，最高溫 {maxt8} 度，最低溫 {mint8} 度，降雨機率 {pop8} %'
        all_msg += '🌞' + msg + '\n\n'


    """
    if city == '金門縣':
        out_city += '🌞' + f'{city} 🌚天氣: {wx8}，最高溫 {maxt8} 度，最低溫 {mint8} 度，降雨機率 {pop8} % \n\n'
    if city == '澎湖縣':
        out_city += '🌞' + f'{city} 🌚天氣: {wx8}，最高溫 {maxt8} 度，最低溫 {mint8} 度，降雨機率 {pop8} % \n\n'
    if city == '連江縣':
        out_city += '🌞' + f'{city} 🌚天氣: {wx8}，最高溫 {maxt8} 度，最低溫 {mint8} 度，降雨機率 {pop8} % \n\n'
    """

# 刪除最後一個換行符
all_messages = all_msg.strip()
# out_messages = out_city.strip()
key_messages = key.strip()


headers = {
    'Authorization': 'Bearer ' + line_token     # POST 使用的 headers
}

# 發送指定城市的天氣資訊
all_city = {'message':all_messages}
response_all = requests.post('https://notify-api.line.me/api/notify',headers=headers,data=all_city)

# 發送離島的天氣資訊
# out_city = {'message':out_messages}
# response_out = requests.post('https://notify-api.line.me/api/notify',headers=headers,data=out_city)


# 使用不同的 token 發送到另一個 LINE Notify
family_headers = {
    'Authorization': 'Bearer ' + token_family }
key_gro = {'message':key_messages} # 發送北高屏天氣
response_key2 = requests.post('https://notify-api.line.me/api/notify', headers=family_headers, data=key_gro)
