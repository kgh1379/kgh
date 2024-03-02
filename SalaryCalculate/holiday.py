import requests
from xml.etree import ElementTree

# OpenAPI 인증키 (URL 인코딩된 상태)
service_key = "rdRLE%2FHyy67UTtFIWVweDWoayloqCbA5a%2FFrXMSKhdFefs%2FSkgl8VbtJMQsnzZhjkFWBEN6K4f%2FqqStu6Rhhig%3D%3D"

# OpenAPI 요청 URL
url = "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getHoliDeInfo"

# 현재 날짜로부터 연도와 월 정보 추출
current_year = current_date.year
current_month_str = f"{current_date.month:02d}"  # 월 정보를 두 자리 문자열로 포맷팅 (예: 2월 -> '02')

# API 요청 파라미터 설정
params = {
    'serviceKey': service_key,
    'pageNo': '1',
    'numOfRows': '10',
    'solYear': str(current_year),
    'solMonth': current_month_str
}

# API 요청 및 응답 (가정)
response = requests.get(url, params=params)
# 응답으로부터 설날과 추석이 있는 달 확인 (가정)
# 예: response.content에 "<itemName>설날</itemName>", "<itemName>추석</itemName>" 등의 태그가 포함되어 있다고 가정

# 응답 XML 파싱 (가정)
root = ElementTree.fromstring(response.content)
holiday_months = []

for item in root.findall('.//item'):
    itemName = item.find('itemName').text
    if itemName in ['설날', '추석']:
        eventDate = item.find('locdate').text  # 'YYYYMMDD' 형식
        eventMonth = int(eventDate[4:6])  # 월 정보 추출
        if eventMonth not in holiday_months:
            holiday_months.append(eventMonth)

# holiday_months에 반영된 결과 확인 (가정)
print(holiday_months)
