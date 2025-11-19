# Baskin-Robbins 스타일 키오스크 앱 (Streamlit)
# 사용법: Streamlit Cloud 또는 로컬에서 `streamlit run baskin_kiosk_app.py` 로 실행
# 외부 라이브러리 없음(단, Streamlit은 실행 환경에 설치되어 있어야 합니다)

import streamlit as st

# --- 앱 제목과 설명 ---
st.set_page_config(page_title="베스킨라빈스 키오스크 🍨", page_icon="🍦", layout="centered")
st.title("베스킨라빈스 키오스크 🍨")
st.write("안녕하세요! 주문을 도와드릴게요 — 친절하고 센스있게 안내해 드립니다 😄")

# --- 매장/포장 선택 ---
place = st.radio("어떻게 드실 건가요?", ("매장에서 드실래요 🪑 (매장)", "포장해 갈게요 🛍️ (포장)"))

# --- 용기 옵션과 가격, 스쿱 수 정의 ---
containers = {
    "컵 (1스쿱) 🥄": {"price": 2000, "scoops": 1},
    "컵 (2스쿱) 🥄🥄": {"price": 3500, "scoops": 2},
    "콘 (2스쿱) 🍪": {"price": 3000, "scoops": 2},
    "파인트 (약 4스쿱) 🍯": {"price": 15000, "scoops": 4}
}

container_choice = st.selectbox("용기를 골라주세요", list(containers.keys()))
selected_container = containers[container_choice]

st.markdown(f"**선택:** {container_choice} — 가격: {selected_container['price']:,}원 | 스쿱 수: {selected_container['scoops']}\n")

# --- 용기별로 고를 수 있는 맛 목록 (간단 샘플) ---
base_flavors_common = [
    "바닐라", "초콜릿", "스트로베리", "민트초코", "쿠키앤크림", "솔티카라멜", "녹차", "밀크티", "아몬드봉봉"
]

# 파인트 전용/추천 맛을 추가
pint_extra = ["찹쌀도넛", "레인보우샤베트"]

available_flavors = list(base_flavors_common)
if selected_container['scoops'] >= 4:
    available_flavors += pint_extra

# --- 각 스쿱마다 선택할 수 있도록 selectbox 생성 ---
st.subheader("맛을 골라주세요 🍨")
num_scoops = selected_container['scoops']
choices = []
for i in range(1, num_scoops + 1):
    choice = st.selectbox(f"스쿱 {i} 선택", ["-- 선택 --"] + available_flavors, key=f"scoop_{i}")
    choices.append(choice)

# 유효성 검사: 빈칸이나 중복 허용 여부 처리 (중복은 허용하지만 사용자에게 알려줌)
if any(c == "-- 선택 --" for c in choices):
    st.warning("아직 모든 스쿱의 맛을 선택하지 않으셨어요. 모든 스쿱을 골라주세요!")

if len(set([c for c in choices if c != "-- 선택 --"])) < len([c for c in choices if c != "-- 선택 --"]):
    st.info("같은 맛을 여러 스쿱 선택하셨어요 — 괜찮다면 그대로 진행해주세요! ✨")

# --- 추가 토핑(선택) ---
st.subheader("토핑을 추가하시겠어요? (선택사항)")
available_toppings = ["초코칩", "견과류", "카라멜소스", "딸기소스", "젤리", "아이스크림 없음"]
selected_toppings = st.multiselect("토핑 선택 (복수 선택 가능)", available_toppings, default=["아이스크림 없음"])

# 토핑 가격 (간단하게 고정 또는 없음)
topping_price = 500 if any(t != "아이스크림 없음" for t in selected_toppings) else 0

# --- 가격 계산 ---
base_price = selected_container['price']
# 간단히 스쿱 단가나 추가 비용 없이 용기 가격만 사용. 필요하면 확장 가능.
subtotal = base_price + topping_price

# 할인/세금(간단 예시)
# 이 예제에서는 세금/할인 미적용. 원하면 주석 해제 후 조정 가능.
# tax = int(subtotal * 0.1)
# total = subtotal + tax

total = subtotal

# --- 주문 요약 ---
st.subheader("주문 요약 🧾")
if not any(c == "-- 선택 --" for c in choices):
    st.write(f"**매장형태:** {place}")
    st.write(f"**용기:** {container_choice}")
    st.write("**맛:**")
    for i, c in enumerate(choices, 1):
        st.write(f"- 스쿱 {i}: {c}")
    if topping_price > 0:
        st.write(f"**토핑:** {', '.join([t for t in selected_toppings if t != '아이스크림 없음'])} (+{topping_price:,}원)")
    else:
        st.write("**토핑:** 없음")
    st.write(f"\n**총 가격:** {total:,}원")
else:
    st.info("모든 스쿱의 맛을 선택하시면 주문 요약이 나타납니다 🙂")

# --- 결제 옵션 ---
st.subheader("결제 방법 선택 💳💵")
payment = st.radio("결제 수단을 골라주세요", ("카드 결제 💳", "현금 결제 💵"))

# 사용자의 선택을 저장하고 결제 버튼 생성
if st.button("결제 진행하기 ✅"):
    if any(c == "-- 선택 --" for c in choices):
        st.error("모든 스쿱의 맛을 선택하지 않으셨어요. 주문을 완료하려면 모든 맛을 선택해주세요.")
    else:
        # 간단한 결제 흐름 시뮬레이션
        st.success("주문이 접수되었습니다! 감사합니다 🎉")
        st.write("---")
        st.write(f"**매장형태:** {place}")
        st.write(f"**용기:** {container_choice}")
        st.write(f"**맛:** {', '.join(choices)}")
        if topping_price > 0:
            st.write(f"**토핑:** {', '.join([t for t in selected_toppings if t != '아이스크림 없음'])}")
        else:
            st.write("**토핑:** 없음")
        st.write(f"**결제방법:** {payment}")
        st.write(f"**결제금액:** {total:,}원")
        st.balloons()
        st.info("직원 호출 또는 안내에 따라 주문을 완료해주세요. 즐거운 시간 되세요! 🍨")

# --- 푸터 ---
st.write("\n---\n도움이 필요하시면 직원에게 문의해주세요 — 친절하게 도와드릴게요! 😊")
