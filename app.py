import streamlit as st

import llm_food
import llm_recipe
  

def display_main_page():

    request_form = st.form('request_form')
    request_form.subheader('**요구사항 입력**')

    # 체크박스 및 입력란
    option1 = request_form.checkbox("냉장고 재료 불러오기")
    option2 = request_form.checkbox("음식 취향 반영하기")
    option3 = request_form.checkbox("못먹는 음식 반영하기")
    user_input = request_form.text_input('''추가 요구사항을 입력하세요. 예시) 다이어트에 좋은 음식 추천해줘''')

    submitted = request_form.form_submit_button('제출')

    
    # requirement_txt 생성
    requirement_txt = ""
    if submitted:
        if option1:
            requirement_txt += "냉장고 재료 불러오기. "
        if option2:
            requirement_txt += "음식 취향 반영하기. "
        if option3:
            requirement_txt += "딸기, 견과류 알러지가 있어. "
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
            
            cols = st.columns([4, 1]) 
            with cols[0]:
                st.markdown(f"**{idx}. {rec_food}**")
            with cols[1]:
                if st.button("레시피 보러가기", key=idx):
                    st.session_state.page = 'recipe'
                    st.session_state.selected_index = idx
                    st.session_state.food_name = rec_food
                    st.rerun() 
            st.divider()
                            

def display_recipe(index):
    st.header("레시피")
    
    food_name = st.session_state.get("food_name", "정보가 없습니다.")
    
    # llm에 해당 음식 이름 전달 및 결과 반환
    recipe_info = llm_recipe.GetInformation(food_name)
    st.markdown(f"{recipe_info}")

    if st.button("이전 페이지로 돌아가기"):
        st.session_state.page = 'request'
        st.rerun()


def display_mypage():
    st.header("마이페이지")
    
    st.markdown("### 내 냉장고")
    
    # 추후에 DB에서 받아오는걸로 변경
    items = ['감자', '상추', '계란']
    
    
    st.markdown("### 회원정보")
    
    
    
    st.markdown("### 히스토리")


# Streamlit UI
st.title("레시피 추천 서비스")

if 'page' not in st.session_state:
    st.session_state.page = 'request'
if 'selected_index' not in st.session_state:
    st.session_state.selected_index = None


if st.session_state.page == 'request':
    cols = st.columns([5, 1]) 
    with cols[1]:
        if st.button("마이페이지"):
            st.session_state.page = 'mypage'
            st.rerun()
elif st.session_state.page == 'mypage':
    cols = st.columns([1, 1, 1, 1]) 
    with cols[3]:
        if st.button("홈으로 돌아가기"):
            st.session_state.page = 'request'
            st.rerun()
else:    
    cols = st.columns([1, 1, 1, 1]) 
    with cols[0]:
        if st.button("홈으로 돌아가기"):
            st.session_state.page = 'request'
            st.rerun()
    with cols[3]:
        if st.button("마이페이지"):
            st.session_state.page = 'mypage'
            st.rerun()
            

# Page navigation
if st.session_state.page == 'request':
    display_main_page()
elif st.session_state.page == 'recipe' and st.session_state.selected_index is not None:
    display_recipe(st.session_state.selected_index)
elif st.session_state.page == 'mypage':
    display_mypage()
    
