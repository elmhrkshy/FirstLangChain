import os
from langchain_community.llms.openai import OpenAI
# from openai import OpenAI
from secret_key import openai_key
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

os.environ['OPENAI_API_KEY'] = openai_key

llm = OpenAI(temperature=0.7)

def generate_restaurant_name_and_items(cuisine):
    promt_template_name = PromptTemplate(
        input_variables=["cuisine"],
        template="I want to open a restaurant for {cuisine} food. Suggest a fancy name."
    )

    name_chain = LLMChain(llm=llm, prompt=promt_template_name, output_key="restaurant_name")

    promt_template_items = PromptTemplate(
        input_variables=["restaurant_name"],
        template="Suggest some menu items for {restaurant_name}. Return it as a comma separated list."
    )

    food_items_chain = LLMChain(llm=llm, prompt=promt_template_items, output_key="menu_items")

    chain = SequentialChain(
        chains=[name_chain, food_items_chain],
        input_variables=["cuisine"],
        output_variables=["restaurant_name", "menu_items"]
    )

    response = chain({"cuisine": cuisine})

    return response

if __name__ == "__main__":
    print(generate_restaurant_name_and_items("Italian"), end='')