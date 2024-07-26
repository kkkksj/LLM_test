import streamlit as st
from streamlit_cookies_controller import CookieController
from recipe import recipe_page
from user_db import *
import time

st.session_state.name = None
st.session_state.signup_name = None
def login_page():
    with st.form("login_form"):
        st.header('log-in')

        # 사용자 입력 필드
        id = st.text_input('id')
        password = st.text_input('password', type='password')

        # 로그인 버튼
        if st.form_submit_button('로그인'):
            if id_not_exists(id):
                st.success("회원정보가 없습니다. 회원가입을 진행해주세요")
            else:
                if log_in(id, password):
                    st.session_state.name = get_user_name(id)
                    st.success(f"환영합니다, {st.session_state.name}님!")
                    
                    st.session_state.page = 'main'
                    st.session_state.user_id = id
                    pw, email, name = get_user_information(st.session_state.user_id)
                    st.session_state.user_pw = pw
                    st.session_state.user_email = email
                    
                    cookies = CookieController()
                    cookies.set('logged_in', 'True')
                    cookies.set('user_id', id)
                    cookies.set('user_pw', pw)
                    cookies.set('user_email', email)
                    cookies.set('user_name', name)
                    
                    time.sleep(1)
                    st.rerun()
                    

                else:
                    st.error('잘못된 비밀번호입니다.')

        if st.form_submit_button('아직 회원이 아니신가요?'):
            st.session_state.page = 'signup'
            st.rerun()

def signup_page():
    # def append_info(id, pw):
    #     st.session_state.id_list.append(id)
    #     st.session_state.pw_list.append(pw)

    if 'id_check' not in st.session_state:
        st.session_state.id_check = False

    def id_check():
        st.session_state.id_check = True

    # 페이지 제목
    st.title('회원가입 화면')

    # 회원가입 양식
    st.header('회원가입')

    # 사용자 입력 필드
    id = st.text_input('id')

    if st.button('아이디 중복 확인'):
        if id_not_exists(id):
            id_check()
            st.success("사용 가능한 아이디 입니다.")
        else:
            st.error("사용 불가능한 아이디 입니다. 다시 입력해주세요")

    password = st.text_input('pw', type='password')
    email = st.text_input('e-mail')
    fullname = st.text_input('name')

    # 제출 버튼
    if st.button('회원가입'):
        if id and password and email and fullname and st.session_state.id_check:
            # 여기서 실제 회원가입 로직을 추가할 수 있습니다.
            # 예를 들어, 데이터베이스에 사용자 정보를 저장하는 코드 등.
            add_user(id, password, email, fullname)
            # append_info(id, password)
            st.session_state.page = 'complete'
            st.session_state.signup_name = fullname
            st.rerun()
        else:
            st.error('모든 필드를 입력과 아이디 중복확인을 마쳐주세요.')

    if st.button('로그인으로 돌아가기'):
        st.session_state.page = 'login'
        st.rerun()

def complete_signup_page(name):
    with st.form("complete_form"):
        st.subheader(f'🎉{st.session_state.signup_name}님, 회원가입을 환영합니다🎉')
        st.subheader('서비스를 이용하시려면 로그인을 진행해 주세요.')
        
        if st.form_submit_button('로그인 하러 가기'):
            st.session_state.page = 'login'
            st.rerun()