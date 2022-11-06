import streamlit as st
import pandas as pd
import sqlite3

st.title("Fridge Management")
st.image("https://hips.hearstapps.com/ame-prod-goodhousekeeping-assets.s3.amazonaws.com/main/embedded/22355/fridge"
         "-infographic-main.jpg?resize=768:*")
ingres_data = pd.read_csv("Nutrition.csv")
ingres_data2 = pd.read_csv("Portion.csv")
ingre_choice = ingres_data['Main food description']

def calculatecalo(foodcode, i):
    unit_data = pd.read_csv("Portion.csv")
    ingres_data = pd.read_csv("Nutrition.csv")
    unit = unit_data.loc[unit_data['Food code'] == foodcode]
    unitchoice = st.selectbox('Choose the unit:', unit['Descr'],key = i+1)
    unitgr = unit_data.loc[(unit_data['Food code'] == foodcode) & (unit['Descr'] == unitchoice)]
    portion = st.number_input('Enter the number you want to have:',key = i+2)
    gram = int(unitgr['weight']) * portion
    nutri = ingres_data.loc[ingres_data['Food code'] == foodcode]
    return gram

def get_all_data(table_name):
    command = f'SELECT * FROM {table_name}'
    cur.execute(command)
    data = cur.fetchall()
    return data


con = sqlite3.connect("database.db")
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER, username VARCHAR PRIMARY KEY, password VARCHAR)''')

add_selectbox = st.sidebar.selectbox("Which one?",
                                     ("Home Page", "Sign In", "Sign Up"))

if add_selectbox == "Home Page":
    st.subheader("Home")

elif add_selectbox == "Sign Up":
    new_user_id = len(get_all_data('users')) + 1
    new_username = st.text_input("Enter your username: ")
    new_password = st.text_input("Enter your password: ")
    # try:
    #     cur.execute('''INSERT INTO users (id, username, password) VALUES (?, ?, ?)''',
    #                 (new_user_id, new_username, new_password))
    #     con.commit()
    #     st.success("Successfully")
    # except:
    #     st.warning("Username already exits.")
    if st.button("Sign Up"):
        cur.execute('SELECT * FROM users WHERE username =?', (new_username,))
        result = cur.fetchall()
        if result:
            st.warning("Username already exits.")
        else:
            cur.execute('''INSERT INTO users (id, username, password) VALUES (?, ?, ?)''',
                        (new_user_id, new_username, new_password))
            con.commit()
            st.success("Successfully")


elif add_selectbox == "Sign In":
    username = st.text_input("Username: ")
    password = st.text_input("Password: ")

    if st.checkbox("Sign In"):
        cur.execute('SELECT * FROM users WHERE username =? AND password = ?', (username, password))
        result = cur.fetchall()
        if not result:
            st.warning("Incorrect password/username")
        else:
            st.success(f"Logged in as {username}")
            cur.execute('''CREATE TABLE IF NOT EXISTS storage (id INTEGER, foodname VARCHAR,
                            foodcode INTEGER, weight_grams FLOAT, exp VARCHAR)''')

            cur.execute('SELECT * FROM users WHERE username =? AND password = ?', (username, password))
            current_user = cur.fetchall()
            current_user = list(current_user[0])
            current_user = current_user[0]
            cur.execute('SELECT * FROM storage WHERE id = ?', (current_user,))
            current_storage = cur.fetchall()
            current_table = pd.DataFrame(current_storage,
                                         columns=["ID", "Food Name", "Food Code", "Weight", "EXP"])
            st.dataframe(current_table)
            choice = st.selectbox("Choose One", ("Add New", "Take Out"))
            if choice == "Add New":
                with st.form("Add New"):
                    st.write("Add New Ingredient")
                    ingre_name = st.selectbox('Enter:', ingre_choice)
                    choice1 = ingres_data2.loc[ingres_data2['Main food description'] == ingre_name]
                    unit = choice1['Descr']
                    ingre_unit = st.selectbox('Enter Unit', unit)
                    ingre_weight = st.number_input("Quantity")
                    ingre_exp = st.text_input("Expiry Day")
                    ingre_code1 = ingres_data[ingres_data['Main food description'] == ingre_name]
                    ingre_code = ingre_code1['Food code']
                    ingre_code = ingre_code.values[0]
                    st.write(type(ingre_code))
                    submitted = st.form_submit_button("submit")
                    unitgr = ingres_data2.loc[(ingres_data2['Food code'] == ingre_code) & (choice1['Descr'] == ingre_unit)]
                    ingre_weight = int(unitgr['weight']) * ingre_weight
                    if submitted:
                        # try:
                        # st.write(ingre_code, type(ingre_code))
                        cur.execute(
                            'INSERT INTO storage (id, foodname, foodcode, weight_grams, exp) VALUES (?, ?, ?, ?, ?)',
                            (current_user, ingre_name, ingre_code, ingre_weight, ingre_exp))
                        con.commit()
                        # except:
                        #     st.write("error")
