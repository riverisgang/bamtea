import streamlit as st
from PIL import Image
import random
import numpy as np

# ---------------------------------------------------------
# 기본 설정
# ---------------------------------------------------------
st.set_page_config(page_title="BAME (Bamti Escape)", layout="wide")

# ---------------------------------------------------------
# 유틸 함수들
# ---------------------------------------------------------
def simple_sentiment_hint(text):
    neg_kw = ["싫", "안돼", "짜증", "별로", "화", "싫어"]
    pos_kw = ["좋", "멋", "대박", "축하", "예쁘", "사랑", "감사"]
    score = 0
    for w in pos_kw:
        if w in text: score += 1
    for w in neg_kw:
        if w in text: score -= 1
    return score

def generate_reply_suggestions(incoming_msg):
    base = simple_sentiment_hint(incoming_msg)
    if base > 0:
        base_sugs = ["오 대박인데!", "좋아 보인다 :)", "더 알려줘!"]
    elif base < 0:
        base_sugs = ["괜찮아?", "혹시 무슨 일 있어?", "나한테 말해줘도 돼"]
    else:
        base_sugs = ["그렇구나!", "오 흥미롭다", "조금 더 얘기해줘!"]

    return [s + " (부드러운 톤)" for s in base_sugs]

def generate_social_post_recommendations(message):
    filters = ["따뜻한 필름톤", "쿨톤 미니멀", "하이콘트라스트"]
    fonts = ["산세리프", "모던 세리프", "손글씨 느낌"]
    stickers = ["미니멀 스티커", "감성 텍스트 스티커", "아이콘형 스티커"]

    captions = [
        f"'{message[:40]}' 느낌 살린 감성 문구",
        f"#{''.join(message.split()[:3])} #BAME 추천",
        "짧고 강렬한 한 문장 강조"
    ]

    return {
        "filter": random.choice(filters),
        "font": random.choice(fonts),
        "stickers": random.choice(stickers),
        "captions": captions
    }

def explain_meme(name):
    memes = {
        "짤방": "짤(짤방)은 인터넷에서 자주 쓰이는 반응 이미지로 감정을 표현할 때 사용돼요.",
        "밈템플릿": "캡션만 바꿔 끊임없이 재창조되는 인터넷 밈 포맷이에요.",
        "캐릭터패러디": "유명 캐릭터를 상황에 맞게 재해석하는 밈이에요."
    }
    return memes.get(name.lower(), "해당 밈이 데이터베이스에 없어요!")

def compute_score(has_chat, has_style, has_sns):
    score = 50
    if has_chat: score += 15
    if has_style: score += 20
    if has_sns: score += 15
    return min(100, score)

# ---------------------------------------------------------
# CSS (3개 패널 스타일)
# ---------------------------------------------------------
st.markdown("""
<style>
    .main { background-color: #000; color: white; }
    .panel {
        background: rgba(255,255,255,0.05);
        border-radius: 22px;
        padding: 24px;
        min-height: 600px;
        border: 1px solid rgba(255,255,255,0.15);
    }
    h1, h2, h3, h4 { font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 레이아웃
# ---------------------------------------------------------
left, mid, right = st.columns(3)

# ---------------------------------------------------------
# LEFT PANEL — 앱 소개
# ---------------------------------------------------------
with left:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown("## 🌓 BAME — 밤티 탈출 앱")
    st.write("- 📱 대화 추천")
    st.write("- 👔 AI 코디 추천")
    st.write("- ✨ SNS 브랜딩 추천")
    st.write("- 😂 유행 밈 설명")
    st.write("- 📊 오늘의 밤티 점수 분석")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# MID PANEL — 기능 실행 구역
# ---------------------------------------------------------
with mid:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown("## 기능 선택")

    selected = st.selectbox(
        "원하는 기능을 선택하세요",
        ["선택하세요", "대화 추천", "코디 추천 (간단버전)", "SNS 컨텐츠 추천", "밈 설명"]
    )
    st.markdown("---")

    # 대화 추천
    if selected == "대화 추천":
        msg = st.text_area("상대 메시지 입력")
        if st.button("답장 추천 보기"):
            if msg:
                sugs = generate_reply_suggestions(msg)
                st.success("추천 답장:")
                for s in sugs:
                    st.write("- " + s)

    # 코디 추천 (이미지 없는 간단 버전)
    elif selected == "코디 추천 (간단버전)":
        colortone = st.selectbox("퍼스널 컬러", ["선택", "웜톤", "쿨톤", "중성톤"])
        if st.button("코디 추천"):
            if colortone == "웜톤":
                st.write("- 베이지/브라운 계열 코디 추천")
                st.write("- 골드 악세서리")
            elif colortone == "쿨톤":
                st.write("- 네이비/화이트 조합")
                st.write("- 실버 악세서리")
            else:
                st.write("- 무채색 + 포인트 색상 조합")

    # SNS 추천
    elif selected == "SNS 컨텐츠 추천":
        msg = st.text_input("올릴 게시물의 분위기/메시지")
        if st.button("추천 받기"):
            rec = generate_social_post_recommendations(msg)
            st.write("🎨 필터 추천:", rec["filter"])
            st.write("🔤 폰트 추천:", rec["font"])
            st.write("🔖 스티커:", rec["stickers"])
            st.write("📝 문구:")
            for c in rec["captions"]:
                st.write("- " + c)

    # 밈 설명
    elif selected == "밈 설명":
        meme = st.text_input("밈 이름")
        if st.button("설명 보기"):
            st.write(explain_meme(meme))

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# RIGHT PANEL — 오늘의 점수
# ---------------------------------------------------------
with right:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown("## 오늘의 밤티 점수")

    has_chat = st.checkbox("오늘 대화·답장 잘 했음")
    has_style = st.checkbox("오늘 스타일 관리함")
    has_sns = st.checkbox("SNS 꾸준히 올림")

    if st.button("점수 분석하기"):
        score = compute_score(has_chat, has_style, has_sns)
        st.markdown(f"<h1 style='font-size:80px; text-align:center;'>{score}</h1>", unsafe_allow_html=True)
        if score == 100:
            st.write("🔥 완벽한 밤티! 오늘 너무 멋져요!")
        elif score > 70:
            st.write("좋아요! 오늘도 성장 중 ✨")
        else:
            st.write("내일 더 멋진 밤티로 만들어보자 :)")

    st.markdown("</div>", unsafe_allow_html=True)
