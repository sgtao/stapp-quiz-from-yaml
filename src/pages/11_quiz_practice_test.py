# pages/11_quiz_practice_test.py
import streamlit as st
import yaml

from components.ConfigFiles import ConfigFiles

APP_TITLE = "Quiz Test App"


def load_quiz_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)[0]


def convert_contents_to_dict(contents):
    """リスト形式のコンテンツを辞書形式に変換"""
    content_dict = {}
    details_list = []
    for item in contents:
        if "034_details" in item:
            details_list.append(item["034_details"])
        else:
            content_dict.update(item)
    if details_list:
        content_dict["034_details"] = "\n\n-----\n\n".join(details_list)
    return content_dict


def checkbox_callback(option):
    if option in st.session_state.selected_options:
        st.session_state.selected_options.remove(option)
    else:
        st.session_state.selected_options.append(option)


def clear_checkbox_options():
    st.session_state.selected_options = []


def initialize_session_state():
    # セッション状態の初期化
    if "sections" not in st.session_state:
        st.session_state.sections = []
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "show_answer" not in st.session_state:
        st.session_state.show_answer = False
    if "selected_options" not in st.session_state:
        # st.session_state.selected_options = []
        clear_checkbox_options()


def itemSlider(sections, key="default"):
    # 前の問題と次の問題のボタンを横に並べる
    col1, col2, col3 = st.columns(3)

    # 前の問題へ進むボタン
    with col1:
        if st.session_state.current_question > 0:
            if st.button("前の問題へ", key=f"{key}_prev"):
                clear_checkbox_options()
                st.session_state.current_question -= 1
                st.rerun()
    with col2:
        pass
    # 次の問題へ進むボタン
    with col3:
        if st.session_state.current_question < len(sections) - 1:
            if st.button("次の問題へ", key=f"{key}_next"):
                clear_checkbox_options()
                st.session_state.current_question += 1
                st.rerun()


def sideMenuProgress(sections):
    # 進捗状況の表示
    st.sidebar.markdown("### 進捗状況")
    st.sidebar.progress(
        (st.session_state.current_question + 1) / len(sections)
    )
    st.sidebar.markdown(
        f"問題 {st.session_state.current_question + 1} / {len(sections)}"
    )
    # st.sidebar.markdown(f"現在のスコア: {st.session_state.score}")


def main():

    # st.session_stateの初期化
    initialize_session_state()
    # assets/privatesフォルダからyamlファイルを選択
    config_files = ConfigFiles("Select a Quiz file")

    st.page_link("main.py", label="Back to Home", icon="🏠")
    st.subheader(f"🚀 {APP_TITLE}")

    try:
        if st.session_state.sections == []:
            # YAMLファイルの読み込み
            selected_config_file = config_files.render_config_selector()
            st.info(f"Selected config file: {selected_config_file}")

            # if "quiz_data" not in locals():
            #     quiz_data = load_quiz_data("assets/practice-test.yaml")
            # sections = quiz_data["013_sections"]
            st.warning("Press 'Load Quiz' button to load quiz data.")
            if st.button("Load Quiz'"):
                quiz_data = load_quiz_data(selected_config_file)
                st.session_state.sections = quiz_data["013_sections"]
                st.rerun()

            return
        else:
            sections = st.session_state.sections

        current_section = sections[st.session_state.current_question]

        # 設問スライダー
        itemSlider(sections, key="top")

        # 問題の表示
        st.subheader(current_section["021_title"])

        # コンテンツをリストから辞書に変換
        content = convert_contents_to_dict(current_section["023_contents"])

        # 問題文の表示
        st.markdown(content["031_question"])

        # 選択肢の表示
        options = content.get("032_selections", [])

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
            st.subheader("選択された答え:")
            for selected_option in st.session_state.selected_options:
                st.markdown(f"- {selected_option}")
        else:
            st.warning("選択された答えはありません")

        # 回答・解説の表示切り替え
        if "033_answer" in content:
            with st.expander("回答・解説を表示"):
                correct_answer = content["033_answer"].strip()
                st.markdown(f"### 正解：\n{correct_answer}")

                # 解説の表示
                if "034_details" in content:
                    st.markdown("### 解説")
                    st.markdown(content["034_details"])

        # 補足情報の表示（存在する場合）
        if "035_supplements" in content:
            with st.expander("補足"):
                st.markdown(content["035_supplements"])

    except Exception as e:
        st.error(f"なんらかのエラーが起きました: {str(e)}")

    # 設問スライダー
    itemSlider(sections, key="bottom")

    # サイドメニュー
    sideMenuProgress(sections)


if __name__ == "__main__":
    main()
