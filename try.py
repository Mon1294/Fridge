import pandas as pd
import streamlit as st

user_data = [{'id':11511200, 'name':'Chocolate milk, ready to drink, reduced fat', 'weight':10, 'exp_date':'20-10-2022'},
             {'id':21500000, 'name':'Ground beef, raw', 'weight':4, 'exp_date':'24-10-2022'}]
gram= 0
calo = 0
protein = 0
carb = 0
fat = 0
i = 0
foodid = 0
prd_data = []
#nhung san pham co trong tu lanh = prd_total
for food in user_data:
    prd_data.append(food['name'])
#cac ham
def calculatecalo(foodcode,i):
    unit_data = pd.read_csv("Portion.csv")
    ingres_data = pd.read_csv("Nutrition.csv")
    unit = unit_data.loc[unit_data['Food code'] == foodcode]
    unitchoice = st.selectbox('Choose the unit:', unit['Descr'],key = i+1)
    unitgr = unit_data.loc[(unit_data['Food code'] == foodcode) & (unit['Descr'] == unitchoice)]
    portion = st.number_input('Enter the number you want to have:',key = i+2)
    gram = int(unitgr['weight']) * portion
    nutri = ingres_data.loc[ingres_data['Food code'] == foodcode]
    return gram,nutri
def add(options,i,calo,protein,carb,fat):
    for food1 in user_data:
        if food1['name'] == options:
            foodid = food1['id']
            break
    st.write('Product:',options)
    gram,nutri = calculatecalo(foodid,i)
    calo += int(nutri['Energy']) * (gram / 100)
    protein += int(nutri['Protein (g)']) * (gram / 100)
    carb += int(nutri['Carbohydrate (g)']) * (gram / 100)
    fat += int(nutri['Total Fat (g)']) * (gram / 100)
    i+=2
    return calo,protein,carb,fat,i
def finish(calo,protein,carb,fat):
    st.write(f'Total calo: {calo} kcal')
    st.write(f'Total carb: {carb} g')
    st.write(f'Total protein: {protein} g')
    st.write(f'Total fat: {fat} g')
#cac button
multichoice = st.multiselect('Pick products',prd_data)
for options in multichoice:
    calo,protein,carb,fat,i = add(options,i,calo,protein,carb,fat)
finish(calo,protein,carb,fat)