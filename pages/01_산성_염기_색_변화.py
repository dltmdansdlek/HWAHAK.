import streamlit as st

st.set_page_config(page_title="산·염기 탐정 실험실", page_icon="🧪", layout="centered")

materials = {
    "식초": {
        "type": "산성",
        "short": "시큼한 식초는 산성이에요.",
    },
    "레몬즙": {
        "type": "산성",
        "short": "상큼한 레몬즙도 산성이에요.",
    },
    "물": {
        "type": "중성",
        "short": "맑은 물은 중성이에요.",
    },
    "비눗물": {
        "type": "염기성",
        "short": "비눗물은 미끄럽고 염기성이에요.",
    },
    "베이킹소다 물": {
        "type": "염기성",
        "short": "베이킹소다 물은 염기성이에요.",
    },
    "탄산음료": {
        "type": "산성",
        "short": "탄산음료는 톡 쏘는 산성이에요.",
    },
}

indicator_options = {
    "보라색 양배추 지시약": {
        "acid": {"label": "빨간색", "css": "#e74c3c"},
        "neutral": {"label": "보라색", "css": "#8e44ad"},
        "base": {"label": "푸른색", "css": "#2980b9"},
    },
    "BTB 용액": {
        "acid": {"label": "노란색", "css": "#f1c40f"},
        "neutral": {"label": "초록색", "css": "#2ecc71"},
        "base": {"label": "파란색", "css": "#2471a3"},
    },
}

def reset_material_counts():
    for name in materials:
        st.session_state[f"count_{name}"] = 0
    st.session_state.dropped = False

if "started" not in st.session_state:
    st.session_state.started = False
    st.session_state.selected_indicator = "보라색 양배추 지시약"
    st.session_state.dropped = False
    for name in materials:
        st.session_state[f"count_{name}"] = 0


def get_combined_result(selected_counts):
    acid = 0
    base = 0
    neutral = 0
    for name, count in selected_counts.items():
        if count <= 0:
            continue
        t = materials[name]["type"]
        if t == "산성":
            acid += count
        elif t == "염기성":
            base += count
        else:
            neutral += count

    if acid > base and acid > neutral:
        return {
            "type": "산성",
            "label": "빨간색 또는 노란색",
            "css": "#e74c3c",
            "explanation": "산성 물질이 더 많아서 산성 쪽 색이 나와요.",
        }
    if base > acid and base > neutral:
        return {
            "type": "염기성",
            "label": "파란색 또는 초록색",
            "css": "#2980b9",
            "explanation": "염기성 물질이 더 많아서 염기성 쪽 색이 나와요.",
        }
    if acid == base and acid > 0:
        return {
            "type": "중성에 가까운 혼합물",
            "label": "보라색/초록색",
            "css": "#7d3c98",
            "explanation": "산성과 염기성이 비슷해서 중간색이 돼요.",
        }
    if neutral >= acid and neutral >= base:
        return {
            "type": "중성",
            "label": "보라색 또는 초록색",
            "css": "#8e44ad",
            "explanation": "중성 물질이 많거나 비슷해서 중성 쪽 색이 나와요.",
        }
    if acid > base:
        return {
            "type": "산성",
            "label": "빨간색 또는 노란색",
            "css": "#e74c3c",
            "explanation": "산성 물질이 더 많아서 산성 쪽 색이 나와요.",
        }
    return {
        "type": "염기성",
        "label": "파란색 또는 초록색",
        "css": "#2980b9",
        "explanation": "염기성 물질이 더 많아서 염기성 쪽 색이 나와요.",
    }

st.title("🧪 산·염기 탐정 실험실")
st.write("여러 물질에 지시약을 떨어뜨려 성질을 알아보자! 실험을 시작하려면 아래 버튼을 눌러요.")

if not st.session_state.started:
    if st.button("실험 시작하기"):
        st.session_state.started = True
        st.session_state.dropped = False

if st.session_state.started:
    st.markdown("---")
    st.subheader("1. 물질을 골라 추가해요")
    st.write("각 물질을 몇 번 넣을지 숫자로 정할 수 있어요. 0이면 선택하지 않은 거예요.")

    cols = st.columns(3)
    material_names = list(materials.keys())
    for idx, material in enumerate(material_names):
        with cols[idx % 3]:
            st.markdown(f"**{material}**")
            st.number_input(
                "개수",
                min_value=0,
                max_value=5,
                step=1,
                key=f"count_{material}",
                label_visibility="collapsed",
            )

    st.button("선택 초기화하기", on_click=reset_material_counts)

    selected_materials = [
        f"{name} x{st.session_state[f'count_{name}']}"
        for name in materials
        if st.session_state[f"count_{name}"] > 0
    ]
    selected_names = [
        name for name in materials if st.session_state[f"count_{name}"] > 0
    ]

    if selected_materials:
        st.success("현재 선택된 물질: " + ", ".join(selected_materials))
    else:
        st.info("아직 선택된 물질이 없어요. 숫자를 0보다 크게 바꿔 보세요.")

    st.markdown("---")
    st.subheader("2. 지시약을 선택해요")
    st.session_state.selected_indicator = st.radio(
        "어떤 지시약을 사용할까요?",
        list(indicator_options.keys()),
        index=list(indicator_options.keys()).index(st.session_state.selected_indicator),
    )

    st.markdown("---")
    st.subheader("3. 지시약을 떨어뜨리기")
    st.write("선택한 물질을 섞어서 지시약을 떨어뜨려 색 변화를 확인해요.")

    if st.button("지시약 떨어뜨리기"):
        if not selected_names:
            st.warning("먼저 하나 이상 물질을 선택해 주세요.")
        else:
            st.session_state.dropped = True

    beaker = st.empty()
    selected_counts = {
        name: st.session_state[f"count_{name}"]
        for name in materials
        if st.session_state[f"count_{name}"] > 0
    }

    if selected_names:
        indicator = st.session_state.selected_indicator
        combined = get_combined_result(selected_counts)

        if st.session_state.dropped:
            result_text = (
                f"{', '.join(selected_materials)}에 {indicator}를 떨어뜨리면 "
                f"{combined['label']}로 변할 수 있어요. → {combined['type']}"
            )
            beaker.markdown(
                f"<div style='text-align:center'>"
                f"<div style='display:inline-block; margin:10px auto 8px; font-size:18px;'>혼합 비커 속 변화</div>"
                f"<div style='border:3px solid #444; border-radius:0 0 30px 30px; width:260px; height:280px; margin:0 auto; position:relative; background:#f4f4f4;'>"
                f"<div style='position:absolute; top:-24px; left:50%; transform:translateX(-50%); width:100px; height:36px; border:3px solid #444; border-bottom:none; border-radius:24px 24px 0 0; background:#f4f4f4;'></div>"
                f"<div style='position:absolute; bottom:10px; left:14px; right:14px; height:200px; background:{combined['css']}; border-radius:0 0 28px 28px; box-shadow: inset 0 0 20px rgba(0,0,0,0.25);'></div>"
                f"</div>"
                f"<div style='margin-top:12px; font-weight:bold;'>{combined['label']} 색으로 변했어요!</div>"
                f"</div>",
                unsafe_allow_html=True,
            )
            st.write(f"**결과:** {result_text}")
            with st.expander("왜 이런 색이 되었을까?"):
                st.write(combined['explanation'])
                if len(selected_names) > 1:
                    st.write("여러 물질을 섞으면 색이 섞여서 더 다양한 결과가 나올 수 있어요.")
                st.write("이 실험으로 우리는 산성과 염기성, 중성을 색으로 구분할 수 있어요.")
        else:
            current_color = "#eef"
            beaker.markdown(
                f"<div style='text-align:center'>"
                f"<div style='display:inline-block; margin:10px auto 8px; font-size:18px;'>비커에 들어있는 혼합물</div>"
                f"<div style='border:3px solid #444; border-radius:0 0 30px 30px; width:260px; height:280px; margin:0 auto; position:relative; background:#f4f4f4;'>"
                f"<div style='position:absolute; top:-24px; left:50%; transform:translateX(-50%); width:100px; height:36px; border:3px solid #444; border-bottom:none; border-radius:24px 24px 0 0; background:#f4f4f4;'></div>"
                f"<div style='position:absolute; bottom:10px; left:14px; right:14px; height:200px; background:{current_color}; border-radius:0 0 28px 28px; box-shadow: inset 0 0 15px rgba(0,0,0,0.15);'></div>"
                f"</div>"
                f"<div style='margin-top:12px; font-weight:bold;'>아직 지시약을 떨어뜨리지 않았어요.</div>"
                f"</div>",
                unsafe_allow_html=True,
            )
            st.info("지금 선택한 물질을 섞은 뒤 지시약을 떨어뜨리면 결과를 볼 수 있어요.")
    else:
        st.info("먼저 하나 이상 물질을 선택해서 비커에 담아 보세요.")

    st.markdown("---")
    st.subheader("실험 결과 예시")
    st.write("양배추 지시약과 BTB 용액을 이용해 물질을 구분해 보세요.")
    st.write(
        "- 식초 + 양배추 지시약 → 붉은색 → 산성\n"
        "- 물 + 양배추 지시약 → 보라색 → 중성\n"
        "- 비눗물 + 양배추 지시약 → 푸른색 → 염기성"
    )
    st.write("여러 물질을 섞어서 어떤 색으로 변하는지 직접 확인해 보세요!")
