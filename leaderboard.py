import streamlit as st
import pandas as pd


def fix_csv_table(name: str):
    df = pd.read_csv(name)
    score_df = df.groupby("FIXTURE")["LLM_JUDGE_SCORE"].sum().reset_index()
    score_df.columns = ["FIXTURE", "Score"]
    score_df = score_df.sort_values(by="Score", ascending=False)
    models_by_score = score_df["FIXTURE"].values.tolist()

    score_df = score_df.set_index("FIXTURE")
    st.dataframe(score_df)

    filtered_df = df[["FIXTURE", "FILEPATH", "LLM_JUDGE_SCORE"]]
    # Pivot the DataFrame
    pivot_df = df.pivot(index="FILEPATH", columns="FIXTURE",
                        values="LLM_JUDGE_SCORE")
    pivot_df = pivot_df.sort_values(by=models_by_score, ascending=False)
    pivot_df = pivot_df[models_by_score]

    # Display the pivoted DataFrame
    st.dataframe(pivot_df)

    # Add a selectbox to select a row
    selected_filepath = st.selectbox(
        "Select a file", filtered_df["FILEPATH"].unique())

    # Display the edit diff in a code block with syntax highlighting
    rows = df[df["FILEPATH"] == selected_filepath]
    rows = rows.sort_values(
        by="FIXTURE",
        key=lambda x: x.map(lambda fixture: models_by_score.index(fixture)),
    )

    for index, row in rows.iterrows():
        diagnostic_after = (
            "" if pd.isna(row["FIX_AFTER_DIAGNOSTIC"]
                          ) else row["FIX_AFTER_DIAGNOSTIC"]
        )
        st.markdown(f"""-----
 **Fixture**: {row["FIXTURE"]}

 **LLM-as-Judge score**: {row["LLM_JUDGE_SCORE"]}

 **Diff:**
 ```{row["LANGUAGEID"]}
 {row["EDIT_DIFF"]}
 ```

 **Diagnostic before**: {row["FIX_BEFORE_DIAGNOSTIC"]}

 **Diagnostic after**: {diagnostic_after}

 **LLM-as-Judge reasoning**: {row["LLM_JUDGE_REASONING"]}

 """)


def chat_csv_table(name: str):
    df = pd.read_csv(name)
    st.subheader("Leaderboard")
    score_df = df.groupby("FIXTURE")["LLM_JUDGE_SCORE"].sum().reset_index()
    score_df.columns = ["FIXTURE", "Score"]
    score_df = score_df.sort_values(by="Score", ascending=False)
    models_by_score = score_df["FIXTURE"].values.tolist()

    score_df = score_df.set_index("FIXTURE")
    st.dataframe(score_df)

    filtered_df = df[["FIXTURE", "FILEPATH",
                      "LLM_JUDGE_SCORE", "CHAT_QUESTION"]]

    pivot_df = df.pivot(index="CHAT_QUESTION",
                        columns="FIXTURE", values="LLM_JUDGE_SCORE")
    pivot_df = pivot_df.sort_values(by=models_by_score, ascending=False)
    pivot_df = pivot_df[models_by_score]

    st.dataframe(pivot_df.style.map(
        lambda score: 'background-color: #ffdddd' if score == 0 else '', subset=pivot_df.columns))

    selected_question = st.selectbox(
        "Select a question", filtered_df["CHAT_QUESTION"].unique())
    filtered_models = st.multiselect(
        "Filter models", filtered_df["FIXTURE"].unique())

    rows = df[(df["CHAT_QUESTION"] == selected_question) & (
        (len(filtered_models) == 0) | (df["FIXTURE"].isin(filtered_models)))]
    rows = rows.sort_values(by="FIXTURE")

    for _, row in rows.iterrows():
        st.header(row["FIXTURE"])
        st.markdown(f"""-----
**Chat Reply**: {row["CHAT_REPLY"]}

""")


def emojify(b: bool):
    return "✅" if bool(b) else "❌"


def unit_test_csv_table(name: str):
    df = pd.read_csv(name)
    st.dataframe(df[['TEST_NAME', 'TEST_LANGUAGE']])

    # filtered_df = df[["FIXTURE", "FILEPATH", "TEST_NAME",
    #                   "LLM_JUDGE_SCORE", "TEST_INPUT_FILE", "TEST_FILE",
    #                   "TEST_GENERATED", "TEST_MATCHES_EXPECTED_TEST_FILE",
    #                   "TEST_USED_CORRECT_FRAMEWORK", "TEST_HAS_ERRORS",
    #                   "TEST_HAS_TYPESCRIPT_ERRORS", "TEST_LANGUAGE"]]

    selected_test = st.selectbox(
        "Select a test", df["TEST_NAME"].unique())

    filtered_models = st.multiselect(
        "Filter models", df["FIXTURE"].unique())

    rows = df[(df["TEST_NAME"] == selected_test) & (
        (len(filtered_models) == 0) | (df["FIXTURE"].isin(filtered_models)))]

    rows = rows.sort_values(by="FIXTURE")

    for _, row in rows.iterrows():
        st.header(row["FIXTURE"])
        test_files_match = bool(row["TEST_MATCHES_EXPECTED_TEST_FILE"])
        expected_text = f"({row['TEST_EXPECTED_FILE'].strip('/')})"
        expected_actual_text = f"(expected: {row['TEST_EXPECTED_FILE']}, produced: {row['TEST_FILE']})"
        st.text(
            f'Produced expected test file: {emojify(test_files_match)} {expected_text if test_files_match else expected_actual_text}')

        st.text("Imported correct framework: " +
                emojify(row["TEST_USED_EXPECTED_TEST_FRAMEWORK"]))
        if row["TEST_LANGUAGE"] == "typescript":
            st.text("Is error free? " +
                    emojify(not row["TEST_HAS_TYPESCRIPT_ERRORS"]))
        st.code(row["TEST_GENERATED"], language=row['TEST_LANGUAGE'])
    # pivot_df = df.pivot(index="FILEPATH",
    #                     columns="FIXTURE", values="LLM_JUDGE_SCORE")
    # pivot_df = pivot_df.sort_values(by=models_by_score, ascending=False)
    # pivot_df = pivot_df[models_by_score]


chatTab, fixTab, unitTestTab, editTab, autocompleteTab = st.tabs(
    ["Chat", "Fix", "Unit Test", "Edit", "Autocomplete"]
)

with chatTab:
    st.header("Chat")
    chat_csv_table("chat.csv")

with fixTab:
    st.header("Fix Command")
    fix_csv_table("fix.csv")

with unitTestTab:
    st.header("Unit Test Command")
    unit_test_csv_table("unit-test.csv")

with editTab:
    st.header("Edit Command")
    st.markdown("Coming soon!")

with autocompleteTab:
    st.header("Autocomplete")
    st.markdown("Coming soon!")
