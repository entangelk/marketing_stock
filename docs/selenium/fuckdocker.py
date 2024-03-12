# * 웹 크롤링 동작
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import re


webdriver_manager_directory = ChromeDriverManager().install()
browser = webdriver.Chrome(service=ChromeService(webdriver_manager_directory))

# from selenium.webdriver.chrome.options import Options

# options = Options()
# options.add_argument("--no-sandbox") #bypass OS security model
# options.add_argument("--headless")
# options.add_argument("--disable-dev-shm-usage") #overcome limited resource problems




# s=ChromeService('./chromedriver')
# driver = webdriver.Chrome(options=options, service=s)



'''
# 몽고db 저장
from pymongo import MongoClient
# mongodb에 접속
# mongoClient = MongoClient("mongodb://192.168.10.10:27017")
mongoClient = MongoClient("mongodb://localhost:27017")

# database 연결
database = mongoClient["project_coliving"]
# collection 작업
room_infor = database['woojoo']
'''

# Chrome WebDriver의 capabilities 속성 사용
capabilities = browser.capabilities
from selenium.webdriver.common.by import By

browser.get("https://www.woozoo.kr/houses")
time.sleep(2)

selector_element = '#search-result'
element_scrollableDiv = browser.find_element(by=By.CSS_SELECTOR, value=selector_element)

from selenium.webdriver.common.keys import Keys

element_body = browser.find_element(by=By.CSS_SELECTOR,value='body')

# 스크롤 부분
previous_scrollHeight = 0

while True:
    # python 방식 변수 매칭
    # javascript와 python 결합 방식 변수 매칭
    browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", element_scrollableDiv)

    current_scrollHeight = browser.execute_script("return arguments[0].scrollHeight",
                                                  element_scrollableDiv)
    
    
    if previous_scrollHeight >= current_scrollHeight:
        break
    else :
        previous_scrollHeight = current_scrollHeight
    time.sleep(1)
    pass

# 가져오기
element_get = browser.find_elements(by=By.CSS_SELECTOR,value='#search-result>div')

main_window_handle = browser.current_window_handle # 초기 창 핸들로 저장

counter = 0
for element in element_get:
    counter +=1
    try :
        element_click = browser.find_element(by=By.CSS_SELECTOR,value=f'#search-result > div:nth-child({counter})')
        element_click.click()
        time.sleep(2)

        # 탭 옮겨가야됨
        all_window_handles = browser.window_handles # 모든 창 저장

        # 새 창 핸들을 찾기
        new_window_handle = None
        for handle in all_window_handles:
            if handle != main_window_handle:    #현재 창이 메인창이 아닐때
                new_window_handle = handle  # 현재 창이 새로운창으로 핸들
                break

        # 새 창 핸들로 전환
        browser.switch_to.window(new_window_handle) # 현재창으로 핸들

        # 새 창의 URL 가져오기
        url = browser.current_url

        browser.get(url)

        # new_page = browser.find_elements(by=By.CSS_SELECTOR, value=' body') 
        time.sleep(1)
        inside_element_gets = browser.find_elements(by=By.CSS_SELECTOR,value='body') #새창의 엘리맨츠 가져오기
        pass
        # 타이틀
        for inside_element_get in inside_element_gets:
            try:
                
                element_title = inside_element_get.find_element(by=By.CSS_SELECTOR,value='#house-show > div.detail_tab_wrapper > div.apply_wrapper-w > h2')
                titles = list(element_title.text.split('\n'))
                title = titles[0]
            except:
                title = ""
            # 옵션
            try:
                # 공용옵션
                selector_options = "#house-show > div.house_intro_wrapper.detail1.scroll > div.area_info > div.area_item.shared_area > ul"
                element_options = inside_element_get.find_element(by=By.CSS_SELECTOR,value=selector_options)
                options = element_options.text
                try:
                    # 개인옵션
                    selector_options = "#house-show > div.house_intro_wrapper.detail1.scroll > div.area_info > div.area_item.privat_area > ul"
                    element_options = inside_element_get.find_element(by=By.CSS_SELECTOR,value=selector_options)
                    options += '\n'
                    options += element_options.text
                except:
                    pass
            except:
                options = ""

            # 지역
            try:
                selector_region = "#house-show > div.house_intro_wrapper.detail1.scroll > div.house_intro"
                element_region = inside_element_get.find_element(by=By.CSS_SELECTOR,value=selector_region)
                region_test = re.split(r'\s+|\n', element_region.text)
                for l in region_test:
                    if l[-1] == '역':
                        region = l
                        break
            except:
                region = ""


            brandType = "일반사업자"    

            contents_wrap = '#image-slider > div.tab_content_wrapper>div'
            detail_element_get = inside_element_get.find_elements(by=By.CSS_SELECTOR,value=contents_wrap)
            menu_count = len(detail_element_get)
            
            incounter = -1
            for k in range(menu_count):
                # 페이지 구성이 0부터 시작... 밑으로 내리기 귀찮...
                incounter += 1

                time.sleep(1)
                if incounter != 0:
                    element_click_second = inside_element_get.find_element(by=By.CSS_SELECTOR,value=f'#image-slider > div.house_structure_tab_list > span:nth-child({incounter+1})')
                    pass

                    
                    element_click_second.click()
                    pass
                    time.sleep(1)

                room_name = inside_element_get.find_element(by=By.CSS_SELECTOR,value='#image-slider > div.house_structure_tab_list > span.house_structure_tab_item.on').text
                    


                new_tab = f'#image_tab_{incounter}'
                i = inside_element_get.find_elements(by=By.CSS_SELECTOR,value=new_tab)
                pass
                for fuck in i:
                    menu_element_get = fuck.find_element(by=By.CSS_SELECTOR,value=f'#image_tab_{incounter} > div.room_info > div.room_name')
                pass
                menu_name_list = re.split(r'\s+|\n', menu_element_get.text)

                isroomcheck = inside_element_get.find_elements(by=By.CSS_SELECTOR,value=f'#image_tab_{incounter} > div.room_info>div')

                if len(isroomcheck) > 2:
                    img_url = 'https://dgdr.co.kr/upload/jijum/238342658_Gf6XysaH_20210923034736.jpg'

                    # 기본 타입 초기화
                    roomType = '그 외'
                    gender = '공용'
                    py = ''

                    for j in menu_name_list:
                        # 성별
                        if '여성' in j:
                            gender = '여'
                        elif '남성' in j:
                            gender = '남'

                        # 평수
                        if 'm' in j:
                            py = j

                        #인실
                        if '1인실' in j:
                            roomType = j

                    # 보증금
                    try:
                        selector_value_deposti = f"#image_tab_{incounter} > div.room_info > div.cost_list > div.cost_item.deposit > span > span > em"
                        for fuck in i:
                            element_deposit= fuck.find_element(by=By.CSS_SELECTOR,value=selector_value_deposti)
                        deposit = element_deposit.text
                    except:
                        deposit = ""
                    # 월세
                    try:
                        selector_value_monthly_rent = f"#image_tab_{incounter} > div.room_info > div.cost_list > div.cost_item.monthly_rent > span > span > em"
                        for fuck in i:
                            try:
                                element_monthly_rent= fuck.find_element(by=By.CSS_SELECTOR,value=f'#image_tab_{incounter} > div.room_info > div.cost_list > div.cost_item.monthly_rent > span > span > em > div > div')
                            except:
                                element_monthly_rent= fuck.find_element(by=By.CSS_SELECTOR,value=selector_value_monthly_rent)
                        monthly_rent = element_monthly_rent.text
                    except:
                        monthly_rent = ""

                    data = {
                        'title' : title,
                        'roomName' : room_name,
                        'gender' : gender,
                        'roomType' : roomType,
                        'py' : py,
                        'deposit' : deposit,
                        'rentFee' : monthly_rent,
                        'region' : region,
                        'brandType' : brandType,
                        'roomOption' : options,
                        'url' : url,
                        'imgUrl' : img_url
                    }
                    pass
                    # room_infor.insert_one(data)
                pass
            else:
                pass
    except :
        pass   
    pass
    browser.close() # 새로 열린창 닫기
    browser.switch_to.window(main_window_handle)    # 다시 처음 창으로 전환


# 브라우저 종료
browser.quit()