import streamlit as st
from helperFunctions import business, tech
import openai
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import json


# to change from GPT4 to GPT4-Turbo
# in model selection
# choose: gpt-4-1106-preview


with open("config.json") as f:
    config = json.load(f)
    key_vault_url = config["KEY_VAULT_URL"]
    deployment_gpt35 = config["gpt3.5"]
    deployment_gpt4 = config["gpt4"]


# credential = DefaultAzureCredential()
#
# secret_client = SecretClient(vault_url=key_vault_url, credential=credential)
# azure_openai_endpoint = secret_client.get_secret("oai-hera-uksouth-endpoint").value
# azure_openai_key = secret_client.get_secret("oai-hera-uksouth-key").value
#
# openai.api_type = "azure"
# openai.api_version = "2023-05-15"
# openai.api_base = azure_openai_endpoint
# openai.api_key = azure_openai_key

openai.api_key = "azure_openai_key"


def main():
    # data_folder = "HR/HRdata"

    metatag_system_prompt = """ 
    
        You are Meta Tag Pro, a data specialist and expert SQL Developer. You will deal with financial data in a bank. You are required to perform the following tasks:

        - From a given dataset, you need to examine, understand, analyze the data
        - Describe the key components and structure of the data file 
        - Outline the data types of the values, the relationships between the data, and check if any dependencies are present in the data
        - Additionally, identify any potential data inconsistencies or abnormalities that you notice
        - Generate a SQL table schema and return only a SQL query based on user input to return data that matches said input
    
    """

    st.markdown(
        """
    <style>
        [data-testid=stSidebar] [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.image("heraLogo.png", width=75)

    menu = ["Home", "Business View", "Technical View"]
    choice = st.sidebar.selectbox("Select your role", menu)
    st.sidebar.markdown("----")

    display_model = st.sidebar.radio("Pick a model version", ("gpt-3.5-turbo", "gpt-4"))
    # data_string = read_dataset(demo_folder)
    # dataStringNew = read_dataset(data_folder)
    # init_prompt = generate_response(
    #     metatag_system_prompt, dataStringNew, model)
    if display_model == "gpt-3.5-turbo":
        model = deployment_gpt35
    elif display_model == "gpt-4":
        model = deployment_gpt4

    if choice == "Home":
        home()
    elif choice == "Business View":
        business(model, metatag_system_prompt)
    elif choice == "Technical View":
        tech(model, metatag_system_prompt)
    # elif choice == "SQL Converter":
    #     customUser(model)


def home():
    st.title("Data Modeller")
    st.markdown(
        """Data Modeller is a powerful tool that drives data management efficiency, assists with data analysis, providing SQL code by leveraging cutting-edge LLMs. \n
• Easily understand existing datasets with structured, human-readable descriptions and automated metadata management. \n
• Advanced capabilities include generating data product descriptions, creating data dictionaries and suggesting potential use cases and improvements, accelerating technical documentation creation. \n
• Identify PII and sensitive information, providing an extra layer of governance to your data management processes. \n
• For the technical user, the Data Assistant can provide SQL code based on plain english user input in proper code format from the data provided. \n
• The Data Assistant can propose potential improvements in the structure/architecture of the data provided. \n
"""
    )

    st.header("Security and Compliance")
    st.markdown(
        "This Data Modeller works by leveraging Azure OpenAI services and its APIs. For use cases that are sensitive and highly regulated in nature, we have compiled the important security highlights of Azure OpenAI:"
    )
    st.markdown(
        "1. Data used to fine-tune models are stored in Azure Storage and are encrypted at rest. \n 2. User Prompts (including data uploaded from the UI) and its corresponding chat completions are stored in servers for 30 days, then deleted. \n 3. Access to this data are limited to Microsoft employees only in the case of Azure OpenAI service abuse by customer. \n 4. This 30 day data retention and Microsoft employee access can be removed by submitting a form to Microsoft defining the use-case. Once approved nothing will be retained in their servers. \n 5. Chat, completions, prompts are not used to train, test, retrain Azure OpenAI models \n 6. Currently, most of our prompts can produce good results from a well defined data dictionary, so redacting any further information from the data is being considered. \n"
    )
    st.markdown(
        "[Source](https://learn.microsoft.com/en-us/legal/cognitive-services/openai/data-privacy?context=%2Fazure%2Fcognitive-services%2Fopenai%2Fcontext%2Fcontext)"
    )


if __name__ == "__main__":
    main()
