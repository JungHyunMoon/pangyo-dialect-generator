from fastapi import FastAPI, Request
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import uvicorn

from dotenv import load_dotenv
from starlette.responses import RedirectResponse

load_dotenv()

def get_llm():
    """LLM 초기화 함수"""
    return ChatOpenAI(model="gpt-4o-mini")



def get_pangyo_chain():
    """판교사투리 변환 Chain 생성"""
    pangyo_dictionary = [
        "문제를 상위 관리자에게 보고하다 -> 에스컬레이션하다",
        "상대방과 의견을 조율하다 -> 얼라인하다",
        "역할과 책임을 분명히 하다 -> 알엔알을 정리하다",
        "진행 가능성을 미리 확인하다 -> 탭핑하다",
        "업무를 마무리하다 -> 오사마리하다",
        "이슈를 부각시키다 -> 이슈라이징하다",
        "작업을 보류하다 -> 펜딩하다",
        "진행 중인 작업 -> WIP",
        "업무를 간결하게 처리하다 -> 린하게 하다",
        "새로운 접근 방식을 시도하다 -> 어프로치하다",
        "투자 대비 수익률을 고려하다 -> ROI를 계산하다",
        "최소 기능 제품을 출시하다 -> MVP를 출시하다",
        "업무를 시작하다 -> 스타트업하다",
        "업무를 종료하다 -> 클로즈업하다",
        "협업하다 -> 콜라보하다",
        "최종 결정을 내리다 -> 파이널라이즈하다",
        "우선순위를 정하다 -> 프라이어리티를 설정하다",
        "문제를 해결하다 -> 솔브하다",
        "지원하다 -> 서포트하다",
        "조정하다 -> 어드저스트하다",
        "최적화하다 -> 옵티마이즈하다",
        "문서를 작성하다 -> 도큐먼트하다",
        "회의록을 작성하다 -> 미닛을 작성하다",
        "진행 상황을 공유하다 -> 프로그레스를 공유하다",
        "회의를 소집하다 -> 미팅을 콜하다",
        "일정을 조율하다 -> 스케줄을 어레인지하다",
        "아이디어를 발전시키다 -> 아이디어를 디벨롭하다",
        "알려주다 -> 노티하다",
        "목록을 작성하다 -> 리스트업하다",
        "확인하다 -> 컨펌하다",
        "논의하다 -> 콜미팅하다",
        "피드백을 주다 -> 피드백하다",
        "업무를 시작하다 -> 스타트하다",
        "업무를 마무리하다 -> 클로즈하다",
        "협업하다 -> 콜라보하다",
        "최종 결정하다 -> 파이널라이즈하다",
        "우선순위를 정하다 -> 프라이어리티를 설정하다",
        "문제를 해결하다 -> 솔브하다",
        "지원하다 -> 서포트하다",
        "조정하다 -> 어드저스트하다",
        "최적화하다 -> 옵티마이즈하다",
        "문서를 작성하다 -> 도큐먼트하다"
    ]

    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(f"""
        입력된 문장을 분석하고, 아래 사전에 있는 용어를 기반으로 판교사투리로 변환하세요.
        사전:
        {pangyo_dictionary}

        변환 규칙:
        1. 사전에 해당하는 표현이 있을 경우, 변환된 표현으로 교체하세요.
        2. 사전에 없는 내용은 그대로 유지하세요.
        3. 문장의 자연스러움을 유지하세요.

        입력: {{question}}
        출력:
    """)

    return LLMChain(llm=llm, prompt=prompt, output_parser=StrOutputParser())


app = FastAPI()
pangyo_chain = get_pangyo_chain()


from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용 (필요에 따라 제한 가능)
    allow_credentials=False,  # 쿠키 허용 여부
    allow_methods=["*"],  # 모든 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)


# Static files를 서빙하도록 설정
app.mount("/static", StaticFiles(directory="frontend", html=True), name="frontend")


@app.get("/")
def redirect_to_static():
    return RedirectResponse(url="/static")


@app.post("/convert")
async def convert(request: Request):
    data = await request.json()
    print("요청 데이터:", data)  # 디버깅용 출력

    input_text = data.get("input_text")
    result = pangyo_chain.run({"question": input_text})
    return {"output_text": result}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
