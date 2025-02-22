import streamlit as st
import pandas as pd

# Streamlit app setup
st.set_page_config(page_title="Calories Advisor App")
st.header("Doctor Nutritionist")

# Configure API key


def get_gemini_response(input_prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content([input_prompt])
        return response.text
    except Exception as e:
        return f"Error in fetching data from the model: {str(e)}"


def create_detailed_prompt(food_items_dict):
    food_details = "\n".join([f"{item} - {quantity} grams" for item, quantity in food_items_dict.items()])
    prompt = f"""
    You are an expert nutritionist. Based on the following quantities of food items in grams,
    please analyze the items and calculate the total calories. For each food item, provide the calories 
    per item based on its quantity and list them in the format below:

    1. Item 1 - quantity in grams - number of calories
    2. Item 2 - quantity in grams - number of calories
    ...

    Additionally, give an overview of the food's healthiness and provide a percentage breakdown of 
    carbohydrates, fats, fibers, sugar, and other essential nutrients.

    Food items and quantities:
    {food_details}
    """
    return prompt



# Dynamic food items input section
st.header("Add Food Items and Quantities")

# List to store dynamically added food items and their quantities
if 'food_items_dict' not in st.session_state:
    st.session_state['food_items_dict'] = {}

# Initialize empty session state variables for user input
if 'new_food_item' not in st.session_state:
    st.session_state['new_food_item'] = ""
if 'new_quantity' not in st.session_state:
    st.session_state['new_quantity'] = 0

# Function to add food item and quantity
def add_food_item():
    item_name = st.session_state['new_food_item'].strip()
    quantity = st.session_state['new_quantity']
    if item_name and quantity > 0:
        st.session_state['food_items_dict'][item_name] = quantity
        st.session_state['new_food_item'] = ""  # Reset input
        st.session_state['new_quantity'] = 0    # Reset quantity

# Input for food item
st.text_input("Enter food item", key='new_food_item')

# Input for quantity
st.number_input("Enter quantity (in grams)", min_value=0, step=1, key='new_quantity')

# Button to add the food item and quantity
st.button("Add Food Item", on_click=add_food_item)

# Display the added food items and their quantities
st.subheader("Food Items and Quantities:")
for item, quantity in st.session_state['food_items_dict'].items():
    st.write(f"{item}: {quantity} grams")

# Submit button to calculate calories based on dynamic inputs
if st.button("Tell me about the total calories"):
    if not st.session_state['food_items_dict']:
        st.error("Please add at least one food item and its quantity.")
    else:
        # Create the prompt based on added food items and quantities
        final_prompt = create_detailed_prompt(st.session_state['food_items_dict'])
        response = get_gemini_response(final_prompt)
        if "Error" in response:
            st.error(response)
        else:
            st.header("The response is:")
            st.write(response)
