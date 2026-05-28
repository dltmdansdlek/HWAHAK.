import streamlit as st

materials = {
    "식초": {
        "type": "산성",
        "cabbage": "빨간색",
        "btb": "노란색",
        "short": "시큼한 식초는 산성이에요.",
    },
    "레몬즙": {
        "type": "산성",
        "cabbage": "주황빛 빨간색",
        "btb": "노란색",
        "short": "상큼한 레몬즙도 산성이에요.",
    },
    "물": {
        "type": "중성",
        "cabbage": "보라색",
        "btb": "초록색",
        "short": "맑은 물은 중성이에요.",
    },
    "비눗물": {
        "type": "염기성",
        "cabbage": "푸른색",
        "btb": "파란색",
        "short": "비눗물은 미끄럽고 염기성이에요.",
    },
    "베이킹소다 물": {
        "type": "염기성",
        "cabbage": "초록빛 파란색",
        "btb": "파란색",
        "short": "베이킹소다 물은 염기성이에요.",
    },
    "탄산음료": {
        "type": "산성",
        "cabbage": "오렌지빛 빨간색",
        "btb": "노란색",
        "short": "탄산음료는 톡 쏘는 산성이에요.",
    },
}

indicator_options = {
    "보라색 양배추 지시약": {
        "acid": "빨간색",
        "neutral": "보라색",
        "base": "푸른색",
    },
    "BTB 용액": {
        "acid": "노란색",
        "neutral": "초록색",
        "base": "파란색",
    },
}

st.set_page_config(page_title="산·염기 탐정 실험실", page_icon="🧪", layout="centered")

if "started" not in st.session_state:
    st.session_state.started = False
    st.session_state.selected_material = None
    st.session_state.selected_indicator = "보라색 양배추 지시약"
    st.session_state.dropped = False

st.title("🧪 산·염기 탐정 실험실")
st.write("여러 물질에 지시약을 떨어뜨려 성질을 알아보는 재미있는 실험이에요.")
st.write("아래에서 직접 물질을 골라 실험을 해 보세요.")

if not st.session_state.started:
    if st.button("실험 시작하기"):
        st.session_state.started = True
        st.session_state.dropped = False

if st.session_state.started:
    st.markdown("---")
    st.subheader("1. 물질을 선택해요")
    st.write("어떤 물질을 실험할지 하나 골라 보세요.")

    cols = st.columns(3)
    material_names = list(materials.keys())
    for idx, material in enumerate(material_names):
        if cols[idx % 3].button(material):
            st.session_state.selected_material = material
            st.session_state.dropped = False

    if st.session_state.selected_material:
        st.success(f"현재 선택된 물질: {st.session_state.selected_material}")
    else:
        st.info("아래 카드에서 물질을 선택해 주세요.")

    st.markdown("---")
    st.subheader("2. 지시약을 선택해요")
    st.session_state.selected_indicator = st.radio(
        "어떤 지시약을 사용할까요?",
        list(indicator_options.keys()),
        index=list(indicator_options.keys()).index(st.session_state.selected_indicator),
    )

    st.markdown("---")
    st.subheader("3. 지시약 떨어뜨리기")
    st.write("선택한 물질과 지시약이 만나면 어떤 색으로 변할까요?")

    if st.button("지시약 떨어뜨리기"):
        if st.session_state.selected_material is None:
            st.warning("먼저 물질을 선택해 주세요.")
        else:
            st.session_state.dropped = True

    beaker = st.empty()
    if st.session_state.selected_material:
        material = st.session_state.selected_material
        indicator = st.session_state.selected_indicator
        material_type = materials[material]["type"]

        if st.session_state.dropped:
            if material_type == "산성":
                color_name = indicator_options[indicator]["acid"]
            elif material_type == "중성":
                color_name = indicator_options[indicator]["neutral"]
            else:
                color_name = indicator_options[indicator]["base"]
            result_text = f"{material}에 {indicator}를 떨어뜨리면 {color_name}으로 변해요. → {material_type}"
            explanation = materials[material]["short"]
            beaker.markdown(
                f"<div style='text-align:center'>"
                f"<div style='display:inline-block; margin:10px auto 8px; font-size:18px;'>비커 속 변화</div>"
                f"<div style='border:3px solid #444; border-radius:0 0 30px 30px; width:180px; height:220px; margin:0 auto; position:relative; background:#f4f4f4;'>"
                f"<div style='position:absolute; top:-20px; left:50%; transform:translateX(-50%); width:80px; height:30px; border:3px solid #444; border-bottom:none; border-radius:20px 20px 0 0; background:#f4f4f4;'></div>"
                f"<div style='position:absolute; bottom:10px; left:10px; right:10px; height:160px; background:{color_name}; border-radius:0 0 25px 25px; box-shadow: inset 0 0 20px rgba(0,0,0,0.25);'></div>"
                f"</div></div>",
                unsafe_allow_html=True,
            )
            st.write(f"**결과:** {result_text}")
            with st.expander("왜 이런 색이 되었을까?"):
                if material_type == "산성":
                    st.write("산성 물질은 지시약과 만나면 빨간색이나 노란색 계열로 변해요. 산성은 시큼한 맛과 연결돼요.")
                elif material_type == "염기성":
                    st.write("염기성 물질은 지시약을 만나면 파란색이나 초록색으로 변해요. 비눗물처럼 미끄러운 느낌이 나는 성질이에요.")
                else:
                    st.write("중성 물질은 지시약과 만나면 보라색 또는 초록색으로 변해요. 물처럼 아주 안전한 상태예요.")
                st.write("이 실험으로 우리는 산성과 염기성, 중성을 색으로 구분할 수 있어요.")
        else:
            current_color = "#eef"
            beaker.markdown(
                f"<div style='text-align:center'>"
                f"<div style='display:inline-block; margin:10px auto 8px; font-size:18px;'>비커에 들어있는 물질</div>"
                f"<div style='border:3px solid #444; border-radius:0 0 30px 30px; width:180px; height:220px; margin:0 auto; position:relative; background:#f4f4f4;'>"
                f"<div style='position:absolute; top:-20px; left:50%; transform:translateX(-50%); width:80px; height:30px; border:3px solid #444; border-bottom:none; border-radius:20px 20px 0 0; background:#f4f4f4;'></div>"
                f"<div style='position:absolute; bottom:10px; left:10px; right:10px; height:160px; background:{current_color}; border-radius:0 0 25px 25px; box-shadow: inset 0 0 15px rgba(0,0,0,0.15);'></div>"
                f"</div></div>",
                unsafe_allow_html=True,
            )
            st.info(f"{material}이(가) 비커에 담겨 있어요. 지시약을 떨어뜨려 색 변화를 확인해 보세요.")
    else:
        st.info("먼저 물질을 선택해서 비커에 담아 보세요.")

    st.markdown("---")
    st.subheader("실험 결과 예시")
    st.write("왼쪽은 양배추 지시약, 오른쪽은 BTB 용액을 썼을 때의 대표 결과예요.")
    st.write(
        "- 식초 + 양배추 지시약 → 붉은색 → 산성\n"
        "- 물 + 양배추 지시약 → 보라색 → 중성\n"
        "- 비눗물 + 양배추 지시약 → 푸른색 → 염기성"
    )
    st.write("이제 여러분이 여러 물질을 하나씩 실험해 보세요!")
