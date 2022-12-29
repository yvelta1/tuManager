import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common.exceptions import *

# Selenium 모듈 로드
import time

options = webdriver.ChromeOptions()
options.add_argument('window-size=1920,1080')
options.add_argument('disable-gpu')
options.add_argument('disable-infobars')
options.add_argument('--disable-extensions')

drv = webdriver.Chrome('chromedriver', options=options)
drv.implicitly_wait(4)


def tuk_login(LOGIN_URL: str, user_id: str, user_pw: str, first_login: bool) -> int:
    login_success = False
    if first_login:
        drv.get(url=LOGIN_URL)

    id_input = drv.find_element(By.CSS_SELECTOR, "#internalId")
    pw_input = drv.find_element(By.CSS_SELECTOR, "#internalPw")
    login_btn = drv.find_element(By.CSS_SELECTOR, "#internalLogin")

    id_input.send_keys(user_id)
    pw_input.send_keys(user_pw)
    login_btn.click()
    try:
        alert = drv.switch_to.alert
        print("다음의 에러로 인하여 로그인할 수 없었습니다.")
        print(alert.text)
        alert.accept()
        return 1  # 로그인 실패
    except NoAlertPresentException:
        return 0  # 로그인 성공


def tuk_get_lesson():
    greet_message = drv.find_element(By.CSS_SELECTOR,
                                     "#Enview_Portlet_Content_15384 > div.p_11.profile > div.greeting > h3").text.split(
        " ")
    name = greet_message[0]
    major = drv.find_element(By.CSS_SELECTOR,
                             "#Enview_Portlet_Content_15384 > div.p_11.profile > div.profile_02 > p").text

    lessons = drv.find_elements(By.CSS_SELECTOR, "#todayLessonList > li")
    lesson_list = dict()
    if len(lessons) > 0:
        for lesson in lessons:
            lesson_title = lesson.find_element(By.CSS_SELECTOR, "a").text
            lesson_time = lesson.find_element(By.CSS_SELECTOR, "span.time").text
            lesson_list[lesson_title] = lesson_time

    print(f"{name} ({major})님 환영합니다.\n")
    if len(lessons) > 0:
        print("오늘의 수업")
        print("과목명   /   시간과 장소")
        for Ltitle, Ltime in lesson_list.items():
            print(f"{Ltitle} \t {Ltime}")
    else:
        print("오늘은 수업이 없는 것 같습니다.")


def tuk_access_to_dormitory():
    drv.execute_script("fn_openComMain('https://dream.tukorea.ac.kr/com/SsoCtr/initPageWork.do?loginGbn=sso');")
    drv.switch_to.window(drv.window_handles[-1])
    drv.implicitly_wait(2)
    category_btn = drv.find_element(By.CSS_SELECTOR,
                                    "#mainframe_VFrameSet_TopFrame_form_mb_topMenu_MPA0001TextBoxElement > div")
    category_btn.click()
    dropdown_btn = drv.find_element(By.CSS_SELECTOR,
                                    "#mainframe_VFrameSet_TopFrame_form_mb_topMenu_popupmenu_MPB0001TextBoxElement > div")

    dropdown_btn.click()


def tuk_get_dormitory_score(semester: int):
    score_cnt = 0
    score_list = []
    score_sum = 0
    sidebar_btn_to_score = drv.find_element(By.XPATH,
                                            '//*[@id="mainframe_VFrameSet_HFrameSet_leftFrame_form_grd_leftMenu_body_gridrow_12_cell_12_0_controltreeTextBoxElement"]/div')
    sidebar_btn_to_score.click()
    semester_dropdown = drv.find_element(By.CSS_SELECTOR,
                                         "#mainframe_VFrameSet_HFrameSet_VFrameSet1_WorkFrame_Child_MPB0024_form_div_Work_div_search_cbo_tmGbn > div")


    if semester == 1:  # 1학기
        semester_dropdown.click()
        find_semester = drv.find_element(By.XPATH, "//*[text()='1학기']")
    elif semester == 2:  # 2학기
        semester_dropdown.click()
        find_semester = drv.find_element(By.XPATH, "//*[text()='2학기']")
    elif semester == 3:  # 여름학기
        semester_dropdown.click()
        find_semester = drv.find_element(By.XPATH, "//*[text()='여름학기']")
    elif semester == 4:  # 겨울학기
        semester_dropdown.click()
        find_semester = drv.find_element(By.XPATH, "//*[text()='겨울학기']")

    drv.execute_script("arguments[0].scrollIntoView();", find_semester)
    find_semester.click()

    search_score_btn = drv.find_element(By.CSS_SELECTOR,
                                        "#mainframe_VFrameSet_HFrameSet_VFrameSet1_WorkFrame_Child_MPB0024_form_div_Work_div_search_btn_search > div")
    search_score_btn.click()
    try:  # alert(조회된 데이터 없음), 즉 상벌점 내역이 없는 경우
        alert = drv.switch_to.alert
        alert.accept()
        print(alert.text)
        return 1
    except NoAlertPresentException:
        scoreboard = list(
            '#mainframe_VFrameSet_HFrameSet_VFrameSet1_WorkFrame_Child_MPB0024_form_div_Work_grd_dorm100_body_gridrow_0')
        try:
            while True:
                scoreboard[-1] = str(score_cnt)
                score = drv.find_element(By.CSS_SELECTOR, ''.join(scoreboard))
                score_list.append(score.text.split('\n'))
                score_cnt += 1
        except:
            print("불러오기 완료.")
        finally:
            # 상벌점을 계산하는 부분
            for s in score_list:
                score_sum += int(s[3])

            # 상벌점을 출력하는 부분
            print("총 상/벌점 :", score_sum)
            for t in range(len(score_list)):
                print(f"{t + 1} : {score_list[t][1]}, {score_list[t][2]}, ({score_list[t][3]}점) / {score_list[t][4]}")
            print('\n\n')


def tuk_overnight():
    try:
        alert = drv.switch_to.alert
        if "입주중인" in alert.text:
            print("현재 생활관에 입주 중이지 않습니다.")
            return 1
    except NoAlertPresentException:
        pass