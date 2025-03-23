# pages/11_quiz_practice_test.py
import streamlit as st
import yaml


def load_quiz_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)[0]


def convert_contents_to_dict(contents):
    """リスト形式のコンテンツを辞書形式に変換"""
    content_dict = {}
    for item in contents:
        content_dict.update(item)
    return content_dict


def checkbox_callback(option):
    if option in st.session_state.selected_options:
        st.session_state.selected_options.remove(option)
    else:
        st.session_state.selected_options.append(option)


def clear_checkbox_options():
    st.session_state.selected_options = []


def main():

    # YAMLファイルの読み込み
    quiz_data = load_quiz_data("assets/practice-test.yaml")
    # print(quiz_data)
    # print(quiz_data["011_title"])

    if "011_title" not in quiz_data:
        st.header("クイズアプリ")
        st.error("読み込みデータの形式が異なるようです")
        return
    else:
        st.subheader(quiz_data["011_title"])

    # セッション状態の初期化
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "show_answer" not in st.session_state:
        st.session_state.show_answer = False
    if "selected_options" not in st.session_state:
        # st.session_state.selected_options = []
        clear_checkbox_options()

    sections = quiz_data["013_sections"]
    current_section = sections[st.session_state.current_question]

    # 問題の表示
    st.subheader(current_section["021_title"])

    # コンテンツをリストから辞書に変換
    content = convert_contents_to_dict(current_section["023_contents"])

    # 問題文の表示
    st.markdown(content["031_question"])

    # 選択肢の表示
    options = content.get("032_selections", [])
    # if options:
    #     answer = st.radio(
    #         "答えを選んでください：",
    #         options,
    #         key=f"q_{st.session_state.current_question}",
    #     )
    # else:
    #     st.warning("選択肢が見つかりません。")

    st.write("答えを選んでください：")
    for option in options:
        is_selected = option in st.session_state.selected_options
        st.checkbox(
            option,
            value=is_selected,
            key=f"checkbox_{option}",
            on_change=checkbox_callback,
            args=(option,),
        )

    # # 選択されたオプションを表示
    # st.write("選択された答え:", st.session_state.selected_options)
    if st.session_state.selected_options:
        st.info("選択された答え:")
        for selected_option in st.session_state.selected_options:
            st.markdown(f"- {selected_option}")
    else:
        st.warning("選択された答えはありません")

    # 回答・解説の表示切り替え
    show_answer = st.toggle(
        "回答・解説を表示", key=f"toggle_{st.session_state.current_question}"
    )

    if show_answer:
        correct_answer = content["033_answer"].strip()
        st.markdown(f"### 正解：\n{correct_answer}")

        # 解説の表示
        st.markdown("### 解説")
        st.markdown(content["034_details"])

        # 補足情報の表示（存在する場合）
        if "035_supplements" in content:
            st.markdown(content["035_supplements"])

    # 前の問題と次の問題のボタンを横に並べる
    col1, col2 = st.columns([0.2, 0.8])

    # 前の問題へ進むボタン
    with col1:
        if st.session_state.current_question > 0:
            if st.button("前の問題へ"):
                clear_checkbox_options()
                st.session_state.current_question -= 1
                st.rerun()

    # 次の問題へ進むボタン
    with col2:
        if st.session_state.current_question < len(sections) - 1:
            if st.button("次の問題へ"):
                clear_checkbox_options()
                st.session_state.current_question += 1
                st.rerun()

    # 進捗状況の表示
    st.sidebar.markdown("### 進捗状況")
    st.sidebar.progress(
        (st.session_state.current_question + 1) / len(sections)
    )
    st.sidebar.markdown(
        f"問題 {st.session_state.current_question + 1} / {len(sections)}"
    )
    st.sidebar.markdown(f"現在のスコア: {st.session_state.score}")


if __name__ == "__main__":
    main()
