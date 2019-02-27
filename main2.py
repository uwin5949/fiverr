
import time
import json
import requests
from bs4 import BeautifulSoup


# url = 'https://study.com/academy/subj/history.html'

# time.sleep(5)
# driver = webdriver.Chrome()
# driver.get("https://study.com/academy/lesson/native-american-history-origin-of-tribes-and-cultures.html")
# driver.find_element_by_id("autoplayControls").find_element_by_class_name("onoffswitch").click()
# print("autoplay on")

def getTsFileName(binName):
    code = binName.replace("https://embed-ssl.wistia.com/deliveries/","").replace(".bin","")
    print(code)
    return "https://embedwistia-a.akamaihd.net/deliveries/" + code + ".ts"


data = {
    "history": {
        "url": "https://study.com/academy/subj/history.html",
        "courses": []
    },
    "humanities": {
        "url": "https://study.com/academy/subj/humanities.html",
        "courses": []
    },
    "socialScience": {
        "url": "https://study.com/academy/subj/social-science.html",
        "courses": []
    }
}

courseObj = {
    "url": "",
    "title": "",
    "chapters": []
}

chapterObj = {
    "title": "",
    "lessions": []
}

lessonObj = {
    "url": "",
    "title": "",
    "binUrl": "",
    "subtitleUrl": ""
}

try:

    with open('dataHumanities.json', 'r') as f:
        count = 0
        data = json.load(f)
        # for subject in data:
        courses = data["courses"]
        for course in courses:
            count = count + 1
            print("------------------------------------------------", count)
            for chapter in course["chapters"]:
                for lesson in chapter["lessions"]:
                    if lesson.get("binUrl") is None:
                        print(lesson["url"])
                        time.sleep(15)
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}
                        # driver.get(lesson["url"])
                        # page_html = driver.page_source
                        page_html = requests.get(lesson["url"], headers=headers)
                        soup = BeautifulSoup(page_html.text, 'html.parser')

                        title = soup.find("div", {"class": "headerTitle"}).find("h1").text
                        lesson["title"] = title

                        videoCont = soup.findAll("div", {"class": "videoContainer"})
                        if len(videoCont) > 0:
                            videoCont = videoCont[0]
                            print("Video Found")
                            wistia_id_cont = videoCont.findAll("div", {"test-id": "wistia_embed"})
                            if len(wistia_id_cont) > 0:
                                wistia_id = wistia_id_cont[0]['data-wistiaid']
                                lesson["subtitleUrl"] = "https://fast.wistia.com/embed/captions/" + wistia_id + ".json?language=eng&callback=wistiajson2"

                                mediasUrl = "https://fast.wistia.com/embed/medias/" + wistia_id + ".json?callback=wistiajson1"
                                jsonFile = requests.get(mediasUrl, headers={"Referer": lesson["url"]}).content
                                # print(jsonFile)
                                j = str(jsonFile).replace("b'/**/wistiajson1(", "").replace(")", "").replace("\\", "").replace("'", "")
                                # print(j[0:7982])
                                try:
                                    d = json.loads(j)
                                    assets = d["media"]["assets"]
                                    for asset in assets:
                                        if asset["type"] == "hls_video" and asset["display_name"] == "720p":
                                            lesson["binUrl"] = getTsFileName(asset["url"])
                                            break
                                except Exception as e456:
                                    lesson["binUrl"] = ""
                                    print(e456)
                                    print("e45")

                            else:
                                lesson["binUrl"] = ""
                                lesson["subtitleUrl"] = ""
                                print("else")
                        else:
                            lesson["binUrl"] = ""
                            lesson["subtitleUrl"] = ""
                            print("No Video")




except Exception as e45:
    print("e45")
    print(e45)


with open('dataHumanities1.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)








