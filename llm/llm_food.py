from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv
import os


def GetInformation(input_text) :    
    load_dotenv()
    
    # 모델 셋팅 
    model = AzureChatOpenAI(
        azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT"), 
        temperature=1.0
    )

    # 프롬프트 템플릿 구성. 
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. 답변은 한국어로 해줘."),
        ("system", '''사용자의 요구사항에 적절한 요리 가능한 음식 딱 5개 추천해줘. 5개만 추천해준다면 500$를 지급할게. 그 이상이나 이하로 추천한다면 지급은 힘들 것 같아. 그리고 부가적인 말 없이 예시 형태로만 답변해줘.
        답변은 에시와 같이 출력해줘.
        예시: ["음식1", "음식2", "음식3", "음식4", "음식5"] 
        '''),
        ("human", "{input}")   
    ])

    # 아웃풋은 스트링으로 반환.
    output_parser = StrOutputParser()

    # 체인 구성.
    chain = prompt_template | model | output_parser
    
    output = chain.invoke({
        "input" : input_text,
    })

    return output