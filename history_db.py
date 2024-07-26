import sqlite3

# DB의 파일명 입니다.
DB_NAME = 'my_recipe.db'

# 사용하실 필요 없습니다.
def make_database(db_name = DB_NAME):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS recipes (
        ID TEXT NOT NULL, 
        food TEXT NOT NULL,
        recipe TEXT NOT NULL,
        PRIMARY KEY (ID, food)
    )
    ''')
    conn.commit()
    conn.close()

# DB에 id,food,recipe를 삽입하는 함수입니다. 사용법 예시) insert_recipe(id,food,recipe)
def insert_recipe(id, food, recipe, db_name = DB_NAME):
    # 어디서 호출 하더라도 오류를 막기 위해서. 
    make_database()
    
    # DB 열기.
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # DB 삽입.
    cursor.execute('INSERT INTO recipes (ID, food, recipe)VALUES (?, ?, ?)', (id, food, recipe))
    
    # 커밋하고 닫기
    conn.commit()
    conn.close()

# DB내의 모든 값 반환하는 함수입니다. 사용법 예시) all_history = get_all_history()
def get_all_history(db_name = DB_NAME):
    make_database()
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM recipes')
    recipes = cursor.fetchall()
    
    conn.close()
    
    return recipes

# DB내의 모든 값 프린트하는 함수입니다. 사용법 예시) print_all_history()
def print_all_history(db_name = DB_NAME):
    make_database()
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM recipes')
    recipes = cursor.fetchall()
    
    conn.close()
    
    for row in recipes :
        print(row)

# id랑 food를 파라미터로 받아서 recipe를 얻어내는 함수입니다. 사용법 예시) recipe_text = get_recipe(id,food)
def get_recipe(id, food,db_name = DB_NAME):
    make_database()
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # id, food랑 매치되는 곳의 recipe 가져옵니다.
    cursor.execute('SELECT recipe FROM recipes WHERE ID = ? AND food = ?', (id, food))
    recipe = cursor.fetchone()
    conn.close()
    
    # 레시피를 반환합니다.
    return recipe[0]

# 특정 유저의 모든 food를 반환하는 함수.   사용법 예시 ) users_all_food = get_users_all_food('parkgod98')
# 파이썬 배열 형식의 리턴값을 가집니다. ex ['김치찌개', '된장찌개', '사시미']
def get_users_all_food(id, db_name=DB_NAME):
    make_database()
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute('SELECT food FROM recipes WHERE ID = ?', (id,))
    foods = cursor.fetchall()
    
    conn.close()
    
    return [food[0] for food in foods]

# id,food만 파라미터로 삽입하면 그 행을 지울 함수입니다. 사용법 예시) remove_recipe(id,food)
def remove_recipe(id, food,db_name = DB_NAME):
    make_database()
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM recipes WHERE ID = ? AND food = ?', (id, food))
    
    conn.commit()
    conn.close()
