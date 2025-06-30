import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# --- 1. 페이지 기본 설정 ---
st.set_page_config(
    page_title="네이버 마케팅 AI 어시스턴트",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 네이버 스타일의 깔끔한 CSS (v6 - 누락된 스타일 추가)
css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;800&display=swap');
    
    /* 전체 배경 및 기본 폰트 */
    html, body, [class*="st-"] {
        font-family: 'Noto Sans KR', -apple-system, BlinkMacSystemFont, 'Malgun Gothic', '맑은 고딕', sans-serif;
        background-color: #F8F9FA;
        color: #333333;
    }

    /* Streamlit 기본 스타일 재설정 */
    .main .block-container {
        padding: 1.5rem 2rem 2rem 2rem;
        max-width: 1400px;
        margin: 0 auto;
    }

    /* 헤더 영역 */
    .header-container {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%);
        border-radius: 16px;
        padding: 25px 30px;
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #E9ECEF;
        display: flex;
        align-items: center;
        gap: 20px;
    }

    .naver-logo {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, #03C75A 0%, #02B351 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        font-weight: 800;
        color: white;
        box-shadow: 0 4px 16px rgba(3, 199, 90, 0.25);
    }

    .header-title {
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
        color: #333333;
    }

    .header-subtitle {
        margin: 5px 0 0 0;
        font-size: 0.95rem;
        color: #6C757D;
        font-weight: 400;
    }
    
    /* st.container(border=True)를 카드처럼 보이게 하는 스타일 */
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 25px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #E9ECEF;
        min-height: 600px; /* 양쪽 카드의 최소 높이를 맞춰줌 */
    }

    .card-title {
        color: #333333;
        font-size: 1.3rem;
        font-weight: 700;
        margin-top: 0 !important;
        margin-bottom: 20px !important;
        padding-bottom: 15px !important;
        border-bottom: 2px solid #F1F3F4;
        display: flex;
        align-items: center;
        gap: 10px;
        position: relative;
    }

    .card-title::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 50px;
        height: 2px;
        background: #03C75A;
        border-radius: 2px;
    }

    /* 텍스트 영역 */
    .stTextArea textarea {
        background: #F8F9FA !important;
        border: 1.5px solid #DEE2E6 !important;
        border-radius: 12px !important;
        padding: 16px !important;
        font-size: 0.9rem !important;
        color: #495057 !important;
        line-height: 1.6 !important;
        transition: border-color 0.2s ease !important;
    }

    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(135deg, #03C75A 0%, #02B351 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 20px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 16px rgba(3, 199, 90, 0.25) !important;
    }

    /* 사이드바 */
    [data-testid="stSidebar"] {
        background: #FFFFFF !important;
        border-right: 1px solid #E9ECEF !important;
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05) !important;
    }
    
    [data-testid="stSidebar"] h2 {
        color: white !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        margin-bottom: 1.5rem !important;
        padding: 12px 16px !important;
        background: linear-gradient(135deg, #03C75A, #02B351) !important;
        border-radius: 10px !important;
        text-align: center !important;
        box-shadow: 0 4px 16px rgba(3, 199, 90, 0.25) !important;
    }
    
    /* 결과 영역 강조 */
    .result-content {
        background: #F8F9FA;
        border-radius: 12px;
        padding: 20px;
        margin-top: 10px;
        border: 1px solid #E9ECEF;
        flex-grow: 1;
    }
    
    /* 피처 분석 섹션 스타일 */
    .feature-table {
        width: 100%;
        border-collapse: collapse;
        margin: 1.5rem 0;
        font-size: 0.9rem;
    }
    .feature-table th, .feature-table td {
        padding: 12px 15px;
        text-align: left;
        border-bottom: 1px solid #E9ECEF;
    }
    .feature-table th {
        background-color: #F8F9FA;
        font-weight: 600;
        color: #495057;
    }
    .feature-table td .tag {
        background: rgba(3, 199, 90, 0.1);
        color: #02B351;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    /* 페르소나 도출 설명 스타일 (추가됨) */
    .persona-derivation {
        font-size: 0.95rem;
        line-height: 1.7;
    }
    .persona-derivation .tag {
        display: inline-block;
        background: rgba(3, 199, 90, 0.1);
        color: #02B351;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
    }

    /* 페르소나 카드 스타일 (사이드바용, 추가됨) */
    .persona-card {
        background: #F8F9FA;
        border-radius: 8px;
        padding: 12px;
        margin: 8px 0;
        border-left: 3px solid #03C75A;
    }
    .persona-card strong {
        color: #333333;
    }

</style>
"""
st.markdown(css, unsafe_allow_html=True)

# --- 2. API 모델 로드 (캐싱) ---
@st.cache_resource
def load_gemini_model():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("🚨 오류: .env 파일에서 GEMINI_API_KEY를 찾을 수 없습니다.")
        return None
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model
    except Exception as e:
        st.error(f"🚨 API 모델 초기화 중 오류 발생: {e}")
        return None

model = load_gemini_model()

# --- 3. 헤더 영역 ---
st.markdown("""
<div class="header-container">
    <div class="naver-logo">N</div>
    <div>
        <h1 class="header-title">네이버 마케팅 AI 어시스턴트</h1>
        <p class="header-subtitle">AI 기반 개인화 마케팅 메시지 생성 플랫폼</p>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 4. 피처 분석 및 페르소나 정의 섹션 (Expander) ---
with st.expander("📊 타겟 고객 피처 분석 및 페르소나 정의 과정 보기"):
    st.markdown("<h3 class='card-title' style='font-size: 1.1rem; margin-bottom: 1rem;'>1. 주요 고객 행동 피처 (Feature)</h3>", unsafe_allow_html=True)
    feature_data = [
        {"feature": "최근 신용조회 이력", "description": "고객이 최근 자신의 신용점수를 조회했는지 여부 및 시점", "interpretation": "🟢 대출 니즈 발생의 가장 강력한 초기 신호"},
        {"feature": "대환대출 상품 비교 횟수", "description": "앱 내에서 여러 대출 상품을 비교해 본 횟수", "interpretation": "🟢 기존 부채에 대한 개선 의지가 매우 높음을 의미"},
        {"feature": "2금융권 대출 보유 여부", "description": "저축은행, 캐피탈 등 2금융권 대출 보유 현황", "interpretation": "🟡 금리 인하 및 부채 통합 니즈가 클 가능성 높음"},
        {"feature": "최근 온라인 쇼핑 금액", "description": "최근 1~3개월간의 온라인 쇼핑(네이버페이 등) 결제 총액", "interpretation": "🟡 단기적인 목적 자금 또는 비상금 대출 수요 예측"},
    ]
    table_html = "<table class='feature-table'><tr><th>주요 피처</th><th>설명</th><th>해석 (마케팅 관점)</th></tr>"
    for item in feature_data:
        table_html += f"<tr><td><strong>{item['feature']}</strong></td><td>{item['description']}</td><td><span class='tag'>{item['interpretation']}</span></td></tr>"
    table_html += "</table>"
    st.markdown(table_html, unsafe_allow_html=True)

    # --- 누락되었던 부분 복원 ---
    st.markdown("<hr style='margin: 1.5rem 0;'>", unsafe_allow_html=True)
    st.markdown("<h3 class='card-title' style='font-size: 1.1rem; margin-bottom: 1rem;'>2. 데이터 기반 페르소나 도출</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div class="persona-derivation">
    <p>위와 같은 개별 피처들을 조합하고, 특정 패턴을 보이는 고객 그룹을 묶어 구체적인 페르소나를 정의합니다. 예를 들어,</p>
    <ul>
        <li><strong>'최근 신용조회 이력' + '대환대출 상품 비교' + '2금융권 대출 보유'</strong> ➡️ <span class="tag">💰 현금흐름 개선 희망형</span> 페르소나로 정의</li>
        <li><strong>'최근 온라인 쇼핑 금액' + '앱 내 금융상품 조회'</strong> ➡️ <span class="tag">🛍️ 스마트 소비 금융형</span> 페르소나로 정의</li>
    </ul>
    <p>이렇게 정의된 페르소나는 좌측 사이드바에서 선택하여 맞춤형 마케팅 메시지를 생성하는 데 사용됩니다.</p>
    </div>
    """, unsafe_allow_html=True)


# 세션 상태 초기화
if 'show_results' not in st.session_state:
    st.session_state.show_results = False
if 'generated_text' not in st.session_state:
    st.session_state.generated_text = ""

# --- 5. 사이드바 및 메인 콘텐츠 ---
if model:
    with st.sidebar:
        st.markdown("<h2>🎯 타겟 설정</h2>", unsafe_allow_html=True)
        persona_options = {
            "💰 현금흐름 개선 희망형": {"description": "여러 건의 대출을 통합하여 월 납입 부담을 줄이고 싶어하는 고객", "features": {"최근 신용조회": "최근 3개월 내", "기존 대출 보유": "2금융권 다수", "앱 활동": "대환대출 비교 검색", "월소득": "300-500만원", "나이대": "30-40대"}},
            "🛍️ 스마트 소비 금융형": {"description": "계획적인 소비와 갑작스러운 지출에 대비하고 싶어하는 고객", "features": {"주요 관심사": "가전제품, 여행, 자기계발", "앱 활동": "비상금 대출 조회", "소비 성향": "온라인 쇼핑 활발", "신용등급": "2-3등급", "나이대": "20-30대"}},
            "🏠 주거안정 추구형": {"description": "내 집 마련이나 주거환경 개선을 위한 자금이 필요한 고객", "features": {"관심분야": "부동산, 인테리어", "대출목적": "주택구입, 전세자금", "직업": "안정적 직장인", "자산현황": "예금 보유", "나이대": "30-50대"}},
            "✏️ 커스텀 입력": {"description": "직접 고객의 특징을 입력하여 맞춤형 메시지를 생성합니다.", "features": {}}
        }
        selected_persona = st.selectbox("🎭 페르소나 선택", options=list(persona_options.keys()))

        st.markdown("<h4 style='margin-top:1.5rem; margin-bottom:0.8rem;'>📊 고객 데이터</h4>", unsafe_allow_html=True)
        if selected_persona == "✏️ 커스텀 입력":
            customer_data = st.text_area("고객의 특징을 자세히 입력하세요", "30대 초반 여성, IT 직종, 최근 자동차 구매 고민, 신용등급 2등급, 월소득 450만원, 온라인 활동 활발", height=150, label_visibility="collapsed")
        else:
            with st.expander("📋 페르소나 상세 정보", expanded=True):
                st.write(f"**설명:** {persona_options[selected_persona]['description']}")
                for key, value in persona_options[selected_persona]['features'].items():
                    st.markdown(f'<div class="persona-card"><strong>{key}:</strong> {value}</div>', unsafe_allow_html=True)
            customer_data = f"페르소나: {selected_persona}\n설명: {persona_options[selected_persona]['description']}\n\n상세 특징:\n" + "\n".join([f"- {k}: {v}" for k, v in persona_options[selected_persona]['features'].items()])
        
        st.markdown("<hr style='margin: 1.5rem 0;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin-bottom:0.8rem;'>⚙️ 생성 옵션</h4>", unsafe_allow_html=True)
        message_type = st.radio("📱 메시지 종류", ("📱 푸시 알림", "💬 SMS", "📧 이메일 제목", "🎯 카카오톡 광고"))
        num_variations = st.slider("🔢 생성할 문구 개수", 1, 8, 5)
        tone_and_manner = st.selectbox("🎨 톤앤매너", ("😊 친근하고 따뜻하게", "🤝 신뢰감을 주도록", "📈 정보 중심으로", "💎 혜택을 강조하며", "⚡ 긴급감을 조성하며"))
        
        st.markdown("<hr style='margin: 1.5rem 0;'>", unsafe_allow_html=True)
        if st.button("🚀 AI 메시지 생성하기", use_container_width=True):
            with st.spinner("🔮 AI가 창의적인 마케팅 메시지를 생성하고 있습니다..."):
                try:
                    prompt = f"""
                    당신은 네이버 금융 서비스의 전문 마케팅 카피라이터입니다. 
                    대출 상품에 관심이 있는 고객에게 개인화된 마케팅 메시지를 생성해주세요.
                    **[타겟 고객 정보]**
                    {customer_data}
                    **[생성 조건]**
                    • 메시지 유형: {message_type}
                    • 톤앤매너: {tone_and_manner}
                    • 생성 개수: {num_variations}개
                    • 브랜드: 네이버 금융
                    **[핵심 미션]**
                    1. 고객의 상황에 공감하고 실질적인 도움이 되는 메시지 작성
                    2. 네이버 금융의 신뢰성과 편의성 강조
                    3. 명확하고 매력적인 Call-to-Action 포함
                    4. 금융 광고 규제 준수 (과도한 표현 지양)
                    **[결과 형식]**
                    각 메시지를 번호와 함께 제시하고, 간단한 설명을 덧붙여주세요.
                    지금 {num_variations}개의 창의적인 마케팅 메시지를 생성해주세요!
                    """
                    safety_settings = {'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE', 'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE', 'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE', 'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE'}
                    response = model.generate_content(prompt, safety_settings=safety_settings)
                    st.session_state.generated_text = response.text
                    st.session_state.show_results = True
                except Exception as e:
                    st.session_state.generated_text = f"🚨 메시지 생성 중 오류가 발생했습니다: {e}"
                    st.session_state.show_results = True
            
    # --- 메인 콘텐츠 영역 (안정적인 2단 레이아웃) ---
    col1, col2 = st.columns(2, gap="large")

    with col1:
        with st.container(border=True):
            st.markdown("<h3 class='card-title'>⚙️ AI에게 전달될 프롬프트</h3>", unsafe_allow_html=True)
            prompt_display = f"""
            **[타겟 고객 정보]**
            {customer_data}
            ---
            **[생성 조건]**
            • 메시지 유형: {message_type}
            • 톤앤매너: {tone_and_manner}
            • 생성 개수: {num_variations}개
            """
            st.text_area("프롬프트 요약", prompt_display, height=480, label_visibility="collapsed")

    with col2:
        with st.container(border=True):
            st.markdown("<h3 class='card-title'>💡 AI 생성 결과</h3>", unsafe_allow_html=True)
            
            if st.session_state.show_results and st.session_state.generated_text:
                st.markdown('<div class="result-content">', unsafe_allow_html=True)
                st.markdown(st.session_state.generated_text)
                st.markdown('</div>', unsafe_allow_html=True)
                st.success("✨ 메시지 생성이 완료되었습니다!")
            else:
                st.info("좌측 사이드바에서 고객 및 생성 옵션을 설정한 후 'AI 메시지 생성하기' 버튼을 눌러주세요. 결과는 여기에 표시됩니다.")

else:
    st.error("🚨 AI 모델을 로드하지 못했습니다. .env 파일에 GEMINI_API_KEY가 올바르게 설정되어 있는지 확인해주세요.")
