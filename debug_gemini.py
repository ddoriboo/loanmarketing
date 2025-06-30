# debug_gemini.py (진단용 스크립트)

import google.generativeai as genai
import os
from dotenv import load_dotenv

print("--- 진단 스크립트를 시작합니다 ---")

# .env 파일에서 환경 변수 로드
load_dotenv()
print(".env 파일 로드를 시도했습니다.")

# API 키 가져오기
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("\n[진단 결과] 심각한 오류: .env 파일에서 'GEMINI_API_KEY'를 찾을 수 없습니다.")
    print("'.env' 파일이 정확한 위치에 있는지, 파일 내에 오타가 없는지 확인해주세요.")
else:
    # 키가 제대로 로드되었는지 일부만 출력하여 확인
    print(f"API 키를 성공적으로 로드했습니다. (키 일부: {api_key[:5]}...{api_key[-4:]})")
    
    try:
        print("\nGoogle AI 서버에 연결을 시도합니다...")
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Streamlit 앱에서 사용하는 것과 동일한 조건으로 테스트
        test_prompt = "당신은 핀테크 마케터입니다. '최근 신용조회 이력이 있고, 기존 대출이 있는 고객'을 위한 푸시 알림 메시지를 1개만 생성해주세요."
        safety_settings = {
            'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE',
            'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
            'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
            'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE',
        }
        
        print("모델에 프롬프트를 전송하고 응답을 기다립니다...")
        
        response = model.generate_content(test_prompt, safety_settings=safety_settings)
        
        print("\n" + "="*20)
        print("[진단 결과] 🎉 테스트 성공! 🎉")
        print("="*20)
        print("API 서버와 정상적으로 통신하여 아래와 같은 응답을 받았습니다:\n")
        print(response.text)

    except Exception as e:
        print("\n" + "="*20)
        print("[진단 결과] ❌ 테스트 실패! ❌")
        print("="*20)
        print("API 호출 중 아래와 같은 오류가 발생했습니다.\n")
        # 오류의 종류와 내용을 모두 출력하여 원인 파악
        print(f"오류 종류: {type(e).__name__}")
        print(f"오류 내용: {e}")
        print("\n--- 예상 원인 및 조치 사항 ---")
        if "API key not valid" in str(e) or "PERMISSION_DENIED" in str(e):
             print("▶ API 키가 잘못되었거나, Google Cloud 프로젝트에서 'Vertex AI API'가 활성화되지 않았을 수 있습니다. Google Cloud Console을 다시 확인해주세요.")
        elif "Billing" in str(e):
             print("▶ Google Cloud 프로젝트에 결제 계정이 연결되지 않았거나 비활성화되었습니다. Google Cloud Console의 '결제' 메뉴를 확인해주세요.")
        elif "DeadlineExceeded" in str(e) or "requests per minute" in str(e):
             print("▶ 요청 시간 초과 또는 분당 요청 한도(Quota)를 초과했습니다. 잠시 후 다시 시도해보세요.")
        else:
             print("▶ 네트워크 연결 문제(방화벽 등) 또는 예상치 못한 다른 오류일 수 있습니다. 위의 오류 내용을 확인해주세요.")