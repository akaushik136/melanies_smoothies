# Import python packages
import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Smoothie Streamlit App :cup_with_straw:")
st.write(
    """Choose fruits in smoothie
    """
)

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be: ", name_on_order)

fruit_chosen = st.selectbox(
    "What is your favorite fruit?",
    ("Peaches", "Banana", "Strawberry"),
)

st.write("Your favourite fruit is:", fruit_chosen)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options")
# st.dataframe(data=my_dataframe, use_container_width=True)

# Convert the Snowpark DataFrame to a Pandas DataFrame
df = my_dataframe.to_pandas()

# Extract options from the FRUIT_NAME column
fruit_options = df['FRUIT_NAME'].tolist()


ingredients_list = st.multiselect(
    "Choose 5 ingredients",
    fruit_options,
    max_selections = 5
)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += ' ' + str(fruit_chosen)
    
    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    # st.write(my_insert_stmt)
    # st.stop()
    # st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# st.text(fruityvice_response.json())
fv_df = st.dataframe(data=fruityvice_response.json(, use_container_width = True)
