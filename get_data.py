import requests
import json

# API 호출에 필요한 기본 설정
API_KEY = '*********************'  # 발급받은 API 키 가려놨습니다. 입력해서 사용하세요.
SERVICE_NAME = 'COOKRCP01'  # 서비스 이름
FILE_TYPE = 'json'  # 요청할 파일 타입
PAGE_SIZE = 1000  # 한 번에 요청할 데이터 개수
TOTAL_COUNT = 1124  # 총 데이터 개수

# 데이터를 request해서 받아올수 있는 함수입니다.
def fetch_data(start_index, end_index):
    url = f"http://openapi.foodsafetykorea.go.kr/api/{API_KEY}/{SERVICE_NAME}/{FILE_TYPE}/{start_index}/{end_index}"
    response = requests.get(url)
    response.raise_for_status()  # 응답 상태 코드가 200이 아닌 경우 예외 발생
    return response.json()       # Json문자열을 Json파일로 만들어서 리턴합니다.

def main():
    # 모든 데이터를 받을 배열입니다.
    all_rows = []
    
    # 첫 번째 요청: 1부터 1000까지
    data = fetch_data(1, PAGE_SIZE) 
    
    # 받아서 row 이는 모든 데이터를 all_rows에 넣습니다.
    if SERVICE_NAME in data and 'row' in data[SERVICE_NAME]:
        rows = data[SERVICE_NAME]['row']
        all_rows.extend(rows)
    else:
        print("API 응답 구조가 예상과 다릅니다.")
    
    # 두 번째 요청: 1001부터 1124까지
    data = fetch_data(PAGE_SIZE + 1, TOTAL_COUNT)
    if SERVICE_NAME in data and 'row' in data[SERVICE_NAME]:
        rows = data[SERVICE_NAME]['row']
        all_rows.extend(rows)
    else:
        print("API 응답 구조가 예상과 다릅니다.")
    
    # JSON 파일로 저장
    # data_rows.json이라는 파일을 현재 디렉토리에 생성 후 쓰기모드로 합니다. 인코딩 방식도 지정했고
    # 열린 파일 객체를 f라는 변수에 할당한 뒤 all_rows를 json형식으로 바꿔서 f에 넣습니다.
    # ensure_ascii는 아스키가 아닌 다른 문자도 저장될수 있고, indent는 4입니다.
    with open('data_rows.json', 'w', encoding='utf-8') as f:
        json.dump(all_rows, f, ensure_ascii=False, indent=4)
    
    print("데이터를 data_rows.json 파일에 저장했습니다.")

if __name__ == '__main__':
    main()
