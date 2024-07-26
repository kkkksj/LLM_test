import streamlit as st
import streamlit.components.v1 as components
from streamlit_cookies_controller import CookieController
import re

import user_db as db

def navigation_button():
    cols = st.columns([3, 1]) 
    with cols[1]:
        if st.button("목록으로 돌아가기"):
            st.session_state.page = 'myrecipe_list'
            st.rerun()

def display_my_recipe_view():
    cookies = CookieController()
    user_id = cookies.get("user_id")
    navigation_button()

     # HTML 스타일을 사용한 추가 재료 박스
    def additional_ingredients(ingred, link):
        st.markdown(f"""
                <div style="padding: 5px; margin-top: 5px">
                    <ul style="list-style-type: disc; margin: 0; padding-left: 20px; align-items: center;">
                        <li>
                            <a href="{link}" 
                                    style="color: black; 
                                    text-decoration: none;
                                    font-size: 20px; 
                                    font-weight: bold;">
                                {ingred}
                            </a>
                        </li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

    recipe = """
                ### 김치찌개 레시피

                #### 재료
                - 묵은지 김치: 2컵
                - 돼지고기: 200g
                - 두부: 1/2모
                - 양파: 1/2개
                - 대파: 1대
                - 다진 마늘: 1큰술
                - 고춧가루: 1큰술
                - 국간장: 1큰술
                - 소금: 약간
                - 물: 4컵
                - 참기름: 1큰술

                #### 요리 순서
                1. 묵은지 김치를 먹기 좋은 크기로 잘라주세요.
                2. 돼지고기를 먹기 좋은 크기로 썰어주세요.
                3. 양파는 채 썰고, 두부는 깍둑썰기 해주세요. 대파는 어슷썰기 해주세요.
                4. 냄비에 참기름을 두르고 돼지고기를 볶아줍니다.
                5. 돼지고기가 반쯤 익으면 김치를 넣고 함께 볶아줍니다.
                6. 김치와 돼지고기가 잘 어우러지면 고춧가루와 다진 마늘을 넣고 볶아줍니다.
                7. 냄비에 물을 붓고 끓입니다.
                8. 물이 끓기 시작하면 양파와 국간장을 넣고 중불로 줄여서 끓입니다.
                9. 두부와 대파를 넣고 10분 정도 더 끓입니다.
                10. 마지막으로 소금으로 간을 맞추고 불을 끕니다.

                ### 재료 리스트
                ["묵은지 김치", "돼지고기", "두부", "양파", "대파", "다진 마늘", "고춧가루", "국간장", "소금", "물", "참기름"]
                """
    
    recipe_info = re.sub(r'\[.*\]', '', recipe)
    st.markdown(f"{recipe_info}")

    match = re.search(r'\[.*?\]', recipe)
    if match:
        ingredient_list = match.group()
        ingredient_list = ingredient_list.strip('[]').replace('"', '').split(', ')

    if ingredient_list:
        need_ingredient = set(ingredient_list)
    else:
        need_ingredient = set([])
    have_ingredient = set(db.get_ingredient(user_id))

    #내가 가진 재료 외 필요한 재료 구하기
    add_ingredient = need_ingredient - have_ingredient
    
    if add_ingredient:
        #마켓컬리 로고사진과 문구 출력
        img_url = "https://res.kurly.com/images/marketkurly/logo/logo_sns_marketkurly.jpg"
        st.markdown(f"""
            <div style="padding: 10px; margin-top: 10px; border-bottom: 1px solid #ddd;">
                <div style="display: flex; flex-direction: column;">
                    <img src="{img_url}" alt="preview" style="width: 100px; height: 100px; object-fit: cover; margin-bottom: 10px;">
                </div>
                <div style="text-align: left; font-size: 18px; padding: 1px;">
                    <span>{"상품명을 누르시면 마켓컬리 구매 링크로 연결됩니다."}</span>
                </div>
            </div>  
            """, unsafe_allow_html=True)
        
        for ingred in list(add_ingredient):
            #추가 재료 품목을 링크로 출력
            purchase_link = f"https://www.kurly.com/search?sword={ingred}"
            additional_ingredients(ingred, purchase_link)
