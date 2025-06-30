import google.generativeai as genai
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# API 키 가져오기
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("오류: .env 파일에서 GEMINI_API_KEY를 찾을 수 없습니다.")
else:
    try:
        print("API 키를 성공적으로 로드했습니다. API 서버에 연결을 시도합니다...")
        genai.configure(api_key=api_key)

        # 가장 간단한 질문으로 API 호출 테스트
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("하늘이 파란 이유를 3줄로 설명해줘.")

        print("\n--- API 테스트 성공! ---")
        print(response.text)
        print("------------------------")

    except Exception as e:
        print(f"\n--- API 테스트 실패 ---")
        print(f"오류가 발생했습니다: {e}")
        print("------------------------")
        print("\n[조치 사항]")
        print("1. .env 파일의 API 키가 올바른지 다시 한번 확인해주세요.")
        print("2. Google Cloud Console에서 API 키가 활성화되어 있는지 확인해주세요.")
        print("3. Google Cloud 프로젝트에 결제 계정이 연결되어 있는지 확인해주세요.")