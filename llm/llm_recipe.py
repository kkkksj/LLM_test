from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv
import os

from rag_chain import *

def GetInformation(input_text) :    
    load_dotenv()
    
    # # 모델 셋팅 
    # model = AzureChatOpenAI(
    #     azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT"), 
    #     temperature=1.0
    # )

    # 프롬프트 템플릿 구성. 
    # prompt_template = ChatPromptTemplate.from_messages([
    #     ("system", "You are a helpful assistant. 답변은 한국어로 해줘."),
    #     ("system", '''사용자가 입력한 음식에 대한 레시피를 알려줘. 형식은 마크타운으로. 그리고 필요한 재료는 마크다운 형식 이후에 에시와 같이 출력해줘. 재료는 단어 형태로만 작성부탁할게.
    #     예시: ["재료1", "재료2", "재료3", "재료4", "재료5"] 
    #     '''),
    #     ("human", "{input}")   
    # ])

    # output_parser = StrOutputParser()

    # 체인 구성.
    # chain = prompt_template | model | output_parser
    
    retriever = init_retriver()
    rag_chain  = init_chain(retriever)
    
    # output = chain.invoke({
    #     "input" : input_text,
    # })
    
    output = ask_something(rag_chain, input_text)

    return output
