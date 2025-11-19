# Baskin-Robbins 스타일 키오스크 앱 (Streamlit) - 용기/맛 선택 + 해피포인트 결제

import streamlit as st

# --- 앱 제목과 설명 ---
st.set_page_config(page_title="베스킨라빈스 키오스크 🍨", page_icon="🍦", layout="centered")
st.title("베스킨라빈스 키오스크 🍨")
st.write("안녕하세요! 주문을 도와드릴게요 — 친절하고 센스있게 안내해 드립니다 😄")

# --- 매장/포장 선택 ---
place = st.radio("어떻게 드실 건가요?", ("매장에서 드실래요 🪑 (매장)", "포장해 갈게요 🛍️ (포장)"))

# --- 용기 옵션과 가격, 스쿱 수 정의 ---
containers = {
    "싱글레귤러 (1가지 맛, 115g) 🍨": {"price": 3900, "scoops": 1},
    "싱글킹 (1가지 맛, 145g) 🍨": {"price": 4700, "scoops": 1},
    "더블주니어 (2가지 맛, 150g) 🍨": {"price": 5100, "scoops": 2},
    "트리플주니어 (3가지 맛, 225g) 🍨": {"price": 7200, "scoops": 3},
    "더블레귤러 (2가지 맛, 230g) 🍨": {"price": 7300, "scoops": 2},
    "파인트 (3가지 맛, 336g) 🥄": {"price": 9800, "scoops": 3},
    "쿼터 (4가지 맛, 643g) 🥄": {"price": 18500, "scoops": 4},
    "패밀리 (5가지 맛, 989g) 🥄": {"price": 26000, "scoops": 5},
    "하프갤론 (6가지 맛, 1237g) 🥄": {"price": 31500, "scoops": 6}
}

container_choice = st.selectbox("용기를 골라주세요", list(containers.keys()))
selected_container = containers[container_choice]
st.markdown(f"**선택:** {container_choice} — 가격: {selected_container['price']:,}원 | 스쿱 수: {selected_container['scoops']}\n")

# --- 용기별로 고를 수 있는 맛 목록 ---
flavors = [
    "골든 프랄린 버터", "초코포키해♥", "말차다미아", "너는 참 달고나", "(Lessly Edition) 초코나무숲",
    "골든 애플 요거트", "(Lessly Edition) 아몬드 봉봉", "(Lessly Edition) 엄마는 외계인",
    "아이스 맥심 모카골드", "사랑에 빠진 딸기", "피치 요거트", "수박 Hero",
    "소금 우유 아이스크림", "마법사의 비밀 레시피", "엄마는 외계인", "민트 초콜릿 칩",
    "뉴욕 치즈케이크", "레인보우 샤베트", "체리쥬빌레", "슈팅스타",
    "오레오 쿠키 앤 크림", "베리베리 스트로베리", "31요거트", "바람과 함께 사라지다",
    "이상한 나라의 솜사탕", "피스타치오 아몬드", "초콜릿 무스", "그린티",
    "초콜릿", "자모카 아몬드 훠지", "아몬드 봉봉", "골든 바닐라"
]

st.write("### 맛을 골라주세요 🍨")
num_scoops = selected_container['scoops']
choices = []
for i in range(1, num_scoops + 1):
    choice = st.selectbox(f"맛 {i} 선택", ["-- 선택 --"] + flavors, key=f"scoop_{i}")
    choices.append(choice)

# 유효성 검사
if any(c == "-- 선택 --" for c in choices):
    st.warning("아직 모든 맛을 선택하지 않으셨어요. 모든 맛을 골라주세요!")

if len(set([c for c in choices if c != "-- 선택 --"])) < len([c for c in choices if c != "-- 선택 --"]):
    st.info("같은 맛을 여러 번 선택하셨어요 — 괜찮다면 그대로 진행해주세요! ✨")

# --- 가격 계산 ---
total = selected_container['price']

# --- 주문 요약 ---
st.write("### 주문 요약 🧾")
if not any(c == "-- 선택 --" for c in choices):
    st.write(f"**매장형태:** {place}")
    st.write(f"**용기:** {container_choice}")
    st.write("**맛:**")
    for i, c in enumerate(choices, 1):
        st.write(f"- {c}")
    st.write(f"\n**총 가격:** {total:,}원")
else:
    st.info("모든 맛을 선택하시면 주문 요약이 나타납니다 🙂")

# --- 결제 옵션 (카드, 현금, 해피포인트) ---
st.write("### 결제 방법 선택 💳💵🌟")
payment = st.radio("결제 수단을 골라주세요", ("카드 결제 💳", "현금 결제 💵", "해피포인트 결제 🌟"))

if st.button("결제 진행하기 ✅"):
    if any(c == "-- 선택 --" for c in choices):
        st.error("모든 맛을 선택하지 않으셨어요. 주문을 완료하려면 모든 맛을 선택해주세요.")
    else:
        st.success("주문이 접수되었습니다! 감사합니다 🎉")
        st.write("---")
        st.write(f"**매장형태:** {place}")
        st.write(f"**용기:** {container_choice}")
        st.write(f"**맛:** {', '.join(choices)}")
        st.write(f"**결제방법:** {payment}")
        st.write(f"**결제금액:** {total:,}원")
        st.snow()
        st.info("직원 안내에 따라 주문을 완료해주세요. 즐거운 시간 되세요! 🍨")

st.write("\n---\n도움이 필요하시면 직원에게 문의해주세요 — 친절하게 도와드릴게요! 😊")
