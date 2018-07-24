import twitter
import requests

API_Key = input("kakao RestAPI 키를 입력해 주세요 : ")
ID = input("검사할 상대의 id를 입력해주세요(@빼고) : ")

api = twitter.Api(consumer_key="", consumer_secret="", access_token_key="", access_token_secret="")

images = []
max_id = None

not_good = 0

API_URL = 'https://kapi.kakao.com/v1/vision/adult/detect'
MYAPP_KEY = API_Key

Score=0


try:
    for i in range(10):
        statuses = api.GetUserTimeline(trim_user=ID, max_id=max_id,count=20)
        for data in statuses:
            max_id = data.id
            if data.media is not None:
                for media in data.media:
                    images.append(media.media_url)

except:
    pass

print(images)

def detect_adult(image_url):
    headers = {'Authorization': 'KakaoAK {}'.format(MYAPP_KEY)}
    global Score
    global not_good

    try:
        data = { 'image_url' : image_url}
        resp = requests.post(API_URL, headers=headers, data=data)
        resp.raise_for_status()
        result = resp.json()['result']

        Score = Score + (result['adult']*100 + result['soft']*80)
        print(result['adult']*100 + result['soft']*80)

        if(result['adult']*100 + result['soft']*80)>90:
            not_good=not_good+1

    except Exception as e:
        print(str(e))
        print(resp.json())

for image in images:
    detect_adult(image)

print("결과:"+str(Score/len(images))+"\n총 이미지:"+str(len(images))+"\n흠...:"+str(not_good))

exitdata = input("엔터를 눌러 프로그램 종료")