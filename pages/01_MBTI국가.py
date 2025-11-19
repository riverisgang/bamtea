import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ---------------------
# 1. CSV 데이터 불러오기
# ---------------------
st.set_page_config(page_title="Country MBTI Distribution", layout="wide")
st.title("국가별 MBTI 비율 시각화")

# CSV 파일 직접 로드
csv_file = "countriesMBTI_16types.csv"
df = pd.read_csv(csv_file)

# MBTI 컬럼 확인
mbti_cols = [col for col in df.columns if col != "Country"]

# 데이터 정규화 (합계 1로 맞추기)
df[mbti_cols] = df[mbti_cols].div(df[mbti_cols].sum(axis=1), axis=0)

# ---------------------
# 2. 사이드바 국가 선택
# ---------------------
st.sidebar.title("국가 선택")
selected_country = st.sidebar.selectbox("국가 선택", df['Country'].tolist())

country_data = df[df['Country'] == selected_country].iloc[0, 1:]
top_mbti = country_data.idxmax()

# ---------------------
# 3. Plotly 막대 그래프
# ---------------------
colors = []
max_val = country_data.max()
for mbti, val in country_data.items():
    if mbti == top_mbti:
        colors.append("red")  # 1등 빨간색
    else:
        # 나머지 그라데이션 (블루 계열)
        alpha = 0.3 + 0.7 * (val / max_val)  # 0.3~1 범위
        colors.append(f"rgba(0,0,255,{alpha})")

# 내림차순 정렬
country_data_sorted = country_data.sort_values(ascending=False)
colors_sorted = [colors[list(country_data.index).index(mbti)] for mbti in country_data_sorted.index]

fig = go.Figure(
    data=[go.Bar(
        x=country_data_sorted.index,
        y=country_data_sorted.values,
        marker_color=colors_sorted,
        text=[f"{v:.2%}" for v in country_data_sorted.values],
        textposition='auto'
    )]
)

fig.update_layout(
    title=f"{selected_country}의 MBTI 비율",
    xaxis_title="MBTI 유형",
    yaxis_title="비율",
    yaxis=dict(tickformat=".0%"),
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------
# 4. 글로벌 평균 MBTI 표시
# ---------------------
st.subheader("전 세계 평균 MBTI 비율")
mean_mbti = df[mbti_cols].mean().sort_values(ascending=False)
st.dataframe(mean_mbti.to_frame("평균 비율").style.format("{:.2%}"))
