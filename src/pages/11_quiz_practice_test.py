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


def main():
    st.title("クイズアプリ")

    # YAMLファイルの読み込み
    quiz_data = load_quiz_data("assets/practice-test.yaml")

    # セッション状態の初期化
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "submitted" not in st.session_state:
        st.session_state.submitted = False

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
    if options:
        answer = st.radio(
            "答えを選んでください：",
            options,
            key=f"q_{st.session_state.current_question}",
        )
    else:
        st.warning("選択肢が見つかりません。")

    # 送信ボタン
    if st.button("回答を送信"):
        st.session_state.submitted = True
        correct_answer = content["033_answer"].strip()
        st.markdown(f"### あなたの回答：\n{answer}")
        st.markdown(f"### 正解：\n{correct_answer}")

        # 解説の表示
        st.markdown("### 解説")
        st.markdown(content["034_details"])

        # 補足情報の表示（存在する場合）
        if "035_supplements" in content:
            st.markdown(content["035_supplements"])

        # 次の問題へ進むボタン
        if st.session_state.current_question < len(sections) - 1:
            if st.button("次の問題へ"):
                st.session_state.current_question += 1
                st.session_state.submitted = False
                st.experimental_rerun()

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
