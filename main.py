import streamlit as st
from streamlit_cookies_controller import CookieController


from login_signup import login_page
from login_signup import signup_page
from login_signup import complete_signup_page
from recipe import recipe_page
from main_page import display_main_page
from mypage import display_mypage
from myrecipe_view_page import display_my_recipe_view
from myrecipe_list_page import display_my_recipe_list

from user_db import get_user_name

st.title("Today's Recipe")

# cookie 및 seesion_state 초기화
cookies = CookieController()
if cookies.get('logged_in') == 'True':
    logged_in=st.session_state.logged_in = True
else:
    logged_in=st.session_state.logged_in = False
    
st.session_state.user_name = get_user_name(cookies.get('user_id'))
st.session_state.user_id = cookies.get('user_id')
st.session_state.user_email = cookies.get('user_email')
st.session_state.user_pw = cookies.get('user_pw')

if cookies.get("logged_in") == 'True' and \
    st.session_state.page != 'mypage' and \
        st.session_state.page != 'recipe' and \
            st.session_state.page != 'myrecipe_list' and \
                st.session_state.page != 'myrecipe_view':
    st.session_state.page = 'main'
elif 'page' not in st.session_state:
    st.session_state.page = 'login'

if 'selected_index' not in st.session_state:
    st.session_state.selected_index = None
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_pw' not in st.session_state:
    st.session_state.user_pw = None
if 'user_email' not in st.session_state:
    st.session_state.user_email = None

if st.session_state.page == 'login':
    st.session_state.user_name = None

# 현재 페이지 상태에 따라 화면 표시
if st.session_state.page == 'login':
    login_page()
elif st.session_state.page == 'signup':
    signup_page()
elif st.session_state.page == 'recipe' and st.session_state.selected_index is not None:
    recipe_page(st.session_state.selected_index)
elif st.session_state.page == 'complete':
    complete_signup_page(st.session_state.user_name)
elif st.session_state.page == 'main':
    display_main_page()
elif st.session_state.page == 'mypage' and st.session_state.page != 'myrecipe_view_list':
    display_mypage()
elif st.session_state.page == 'myrecipe_list':
    display_my_recipe_list()
elif st.session_state.page == 'myrecipe_view':
    display_my_recipe_view()
