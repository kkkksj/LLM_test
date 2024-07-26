import streamlit as st
from streamlit_cookies_controller import CookieController
import time

from llm import llm_food
import user_db as db


def naviagation_button():
    cookies = CookieController()
    st.session_state.logout = False
    cols = st.columns([3, 1, 1]) 
    with cols[0]:
        st.markdown(f'안녕하세요 **{cookies.get('user_name')}** 님')
    with cols[1]:
        if st.button("마이페이지"):
            st.session_state.page = 'mypage'
            st.rerun()
    with cols[2]:
        if st.button('로그아웃'):
            cookies.set('logged_in', 'False')
            cookies.set('user_id', '')
            cookies.set('user_pw', '')
            cookies.set('user_email', '')
            cookies.set('user_name', '')
            st.session_state.logout = True

    if st.session_state.logout:
        st.success('로그아웃 되었습니다.')
        st.session_state.page = 'login'
        time.sleep(1)
        st.rerun()
        

def display_main_page():
    
    naviagation_button()
    
    cookies = CookieController()
    
    user_id = cookies.get('user_name')
    

    request_form = st.form('request_form')
    request_form.subheader('**요구사항 입력**')

    # 체크박스 및 입력란
    option1 = request_form.checkbox("냉장고 재료 반영하기")
    option2 = request_form.checkbox("음식 취향 반영하기")
    option3 = request_form.checkbox("못먹는 음식 반영하기")
    user_input = request_form.text_input('''요구사항을 입력하세요. 예시) 다이어트에 좋은 음식 추천해줘''')

    submitted = request_form.form_submit_button('제출')

    
    # requirement_txt 생성
    requirement_txt = ""
    if submitted:
        if option1:
            option1_list = db.get_ingredient(user_id)
            option1_txt = ','.join(option1_list)
            requirement_txt += option1_txt + " 이 재료들을 반영해줘. 하지만 꼭 반영하지 않아도 괜찮아"
        if option2:
            option2_list = db.get_likes(user_id)
            option2_txt = ','.join(option2_list)
            requirement_txt += option2_txt + " 이건 내 취향이야. 내 취향을 반영해줘. "
        if option3:
            option3_list = db.get_dislikes(user_id)
            option3_txt = ','.join(option3_list)
            requirement_txt += option3_txt + " 이건 내가 싫어하는 음식이야. 이것들을 절대로 사용하지 않는 음식으로만 추천해줘. 그렇지 않는다면 나는 알러지로 죽을거야."
        if user_input:
            requirement_txt += user_input
        
        # llm에 requirement_txt 전달 및 결과 반환
        output_list = llm_food.GetInformation(requirement_txt)
        output_list = output_list.strip('[]').replace('"', '').split(', ')
        
        # 세션 상태에 결과 저장
        st.session_state.output_list = output_list 
        st.session_state.requirement_txt = requirement_txt

    if 'output_list' in st.session_state:
        st.markdown("## 추천 결과")
        st.divider()
        for idx, rec_food in enumerate(st.session_state.output_list, start=1):
            cols = st.columns([3, 1]) 
            with cols[0]:
                st.markdown(f"**{idx}. {rec_food}**")
            with cols[1]:
                if st.button("레시피 보러가기", key=idx):
                    st.session_state.page = 'recipe'
                    st.session_state.selected_index = idx
                    st.session_state.food_name = rec_food
                    st.rerun() 
            st.divider()
            