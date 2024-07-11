import streamlit as st
import requests
from langchain.prompts import PromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain import LLMChain

# Function to validate and get missing details using LangChain
def get_missing_details(details):
    prompt_template = """
    You are an intelligent assistant. The user has provided the following order details:
    Customer: {customer}
    Address: {address}
    PO Number: {po_number}
    Order Date: {order_date}
    Attr1: {attr1}
    Attr2: {attr2}
    Attr3: {attr3}

    If there are any missing details then prompt the user to provide missing details. 
    Only check for above 7 mentioned details to indentify missing details
    If all above details are provided then respond as "no missing details".
    Dont provide extra explaination.
    """
    # Initialize LangChain with OpenAI LLM
    llm = Ollama(model="llama3")
    prompt = PromptTemplate(template=prompt_template, input_variables=["customer", "address", "po_number", "order_date", "attr1", "attr2", "attr3"])
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run(details)
    return response

# Streamlit UI
st.title("Order Creation Bot")

# Initialize session state for storing user inputs
if "details" not in st.session_state:
    st.session_state.details = {
        "customer": "",
        "address": "",
        "po_number": "",
        "order_date": "",
        "attr1": "",
        "attr2": "",
        "attr3": ""
    }

# Capture user inputs
st.session_state.details["customer"] = st.text_input("Customer")
st.session_state.details["address"] = st.text_input("Address")
st.session_state.details["po_number"] = st.text_input("PO Number")
st.session_state.details["order_date"] = st.text_input("Order Date (YYYY-MM-DD)")
st.session_state.details["attr1"] = st.text_input("Attr1")
st.session_state.details["attr2"] = st.text_input("Attr2")
st.session_state.details["attr3"] = st.text_input("Attr3")

# Validate and get missing details
if st.button("Submit"):
    missing_details_response = get_missing_details(st.session_state.details)
    st.write(missing_details_response)

    if "no missing details" in missing_details_response.lower():
        # Call API to create order
        order_data = {
            "cust_name": st.session_state.details["customer"],
            "bill_too_addr": st.session_state.details["address"],
            "order_date": st.session_state.details["order_date"] + "T00:00:00Z",
            "cust_po_number": st.session_state.details["po_number"],
            "comments": "Order created via bot",
            "order_status": "New",
            "header_id": "1",
            "order_number": "1",
            "attr1": st.session_state.details["attr1"],
            "attr2": st.session_state.details["attr2"],
            "attr3": st.session_state.details["attr3"],
            "creation_date": st.session_state.details["order_date"] + "T00:00:00Z",
            "created_by": "Test_User"
        }

        response = requests.post(
            "https://g91bdb7bff11d92-atpdev1.adb.ap-mumbai-1.oraclecloudapps.com/ords/demo_rest/order_header/",
            json=order_data
        )

        st.write("Order created successfully!")
        st.json(response.json())
    else:
        st.write("Please provide the missing details.")
