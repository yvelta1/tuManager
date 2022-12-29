from tuk import *
import getpass
import time

LOGIN_URL = "https://ksc.tukorea.ac.kr/sso/login_stand.jsp"
NX_URL = "https://dream.tukorea.ac.kr/nx/"


def show_title():   # 타이틀 부분을 출력합니다.
    print("*" * 40)
    print("FOR TUKOREA TIP DORMITORY")
    print("*" * 40)


def get_user_info() -> tuple[str, str]:   # 사용자의 정보를 받습니다.
    info_valid = 0   # 사용자에게 입력받은 값의 서식이 옳은지 저장합니다.
    while info_valid == 0:
        user_id = input("ID : ")
        user_pw = getpass.getpass("PW : ")

        if user_id.isspace() or user_pw.isspace() or user_id == "" or user_pw == "":
            print("아이디, 비밀번호는 비워둘 수 없습니다.")
        else:
            info_valid = 1

    return user_id, user_pw


def get_dormitory_score():
    print("a : 1학기 / b : 2학기 / c : 여름학기 / d : 겨울학기")
    choice = input(">")
    while True:
        if choice == "a":
            tuk_get_dormitory_score(1)
            return 0
        elif choice == "b":
            tuk_get_dormitory_score(2)
            return 0
        elif choice == "c":
            tuk_get_dormitory_score(3)
            return 0
        elif choice == "d":
            tuk_get_dormitory_score(4)
            return 0
        else:
            continue


def get_command_loop():
    while True:
        print("****************")
        print("a. 상벌점 체크")
        print("b. 외박 신청")
        command = input()

        if command == 'a':
            get_dormitory_score()
        elif command == 'b':
            pass
        elif command == 'q':
            print("Bye")
            break
        else:
            print("잘못된 명령입니다.")
            

def main():
    show_title()
    user_id, user_pw = get_user_info()
    login_attempt = tuk_login(LOGIN_URL, user_id, user_pw, True)   # 첫 로그인 시도

    while login_attempt == 1:   # 첫 로그인 시도에서 실패한 경우
        user_id, user_pw = get_user_info()
        login_attempt = tuk_login(LOGIN_URL, user_id, user_pw, False)

    tuk_get_lesson()
    tuk_access_to_dormitory()
    time.sleep(0.8)
    get_command_loop()


if __name__ == "__main__":
    main()