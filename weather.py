import requests

url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWA-264D87C4-9C2E-4774-AF87-B987F15828FD'
data = requests.get(url)   # 取得 JSON 檔案的內容為文字
data_json = data.json()    # 轉換成 JSON 格式
location = data_json['records']['location']   # 取出 location 的內容

all_msg = ''

for i in location:
    city = i['locationName']    # 縣市名稱
    wx8 = i['weatherElement'][0]['time'][0]['parameter']['parameterName']    # 天氣現象
    maxt8 = i['weatherElement'][4]['time'][1]['parameter']['parameterName'] # 最高溫
    mint8 = i['weatherElement'][2]['time'][0]['parameter']['parameterName'] # 最低溫
    pop8 = i['weatherElement'][1]['time'][1]['parameter']['parameterName'] # 降雨機率
    msg = f'{city}明天天氣: {wx8}，最高溫 {maxt8} 度，最低溫 {mint8} 度，降雨機率 {pop8} %'
    all_msg += msg + '\n\n'

# 刪除最後一個換行符
all_messages = all_msg.strip()

token = 'yf6Q5uEV3LikZ8eL22yrC0ytdlUnZi1ZzjSf55aJ6Oc' # 自己申請的 LINE Notify 權杖
headers = {
    'Authorization': 'Bearer ' + token      # POST 使用的 headers
}
data = {
    'message':all_messages,            # 發送的訊息
}
data = requests.post('https://notify-api.line.me/api/notify', headers=headers, data=data)    # 發送 LINE NOtify
    