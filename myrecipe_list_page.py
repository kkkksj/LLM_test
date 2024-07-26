import streamlit as st
import user_db as db
from streamlit_cookies_controller import CookieController
from history_db import *

def navigation_button():
    cols = st.columns([1]) 
    with cols[0]:
        if st.button('이전으로 돌아가기'):
            st.session_state.page = 'mypage'
            st.rerun()

food_list = ['김치찌개', '된장찌개']
    
def display_my_recipe_list():
    st.markdown("## 내 레시피")
    navigation_button()
    st.divider()
    for idx, rec_food in enumerate(food_list, start=1):
        cols = st.columns([2, 1]) 
        food_name = food_list[idx-1]
        with cols[0]:
            st.markdown(f"**{idx}. {rec_food}**")
        with cols[1]:
            if st.button(f"{food_name} 레시피 보러가기", key=idx):
                st.session_state.page = 'myrecipe_view'
                st.rerun() 
        st.divider()
        