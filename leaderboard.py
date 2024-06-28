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

    df["LLM_JUDGE_SCORE"] = df["LLM_JUDGE_SCORE"].apply(
        lambda x: 0 if x == 0 else 1)
    df["VERBOSE"] = df["CONCISENESS_SCORE"].apply(lambda x: 1 if x == 0 else 0)

    score_df = df.groupby("FIXTURE")[
        ["LLM_JUDGE_SCORE", "HEDGES", "VERBOSE"]].sum().reset_index()
    score_df.columns = ["FIXTURE", "LLM Judge Score", "Hedges", "Verbose"]
    score_df = score_df.sort_values(by="LLM Judge Score", ascending=False)
    models_by_score = score_df["FIXTURE"].values.tolist()

    score_df = score_df.set_index("FIXTURE")
    st.dataframe(score_df)

    pivot_df = df.pivot(index=["CHAT_QUESTION", "QUESTION_CLASS"],
                        columns="FIXTURE", values="LLM_JUDGE_SCORE")
    pivot_df = pivot_df.sort_values(by="QUESTION_CLASS")
    pivot_df = pivot_df[models_by_score]

    st.dataframe(pivot_df.style.map(
        lambda score: 'background-color: #ffdddd' if score == 0 else '', subset=pivot_df.columns))

    selected_question = st.selectbox(
        "Select question", df["CHAT_QUESTION"].unique())
    filtered_models = st.multiselect("Filter models", df["FIXTURE"].unique())

    rows = df[(df["CHAT_QUESTION"] == selected_question) & (
        (len(filtered_models) == 0) | (df["FIXTURE"].isin(filtered_models)))]
    fixtures = rows.groupby("FIXTURE")

    for fixture, rows in fixtures:
        rows = rows.sort_values(by="LLM_JUDGE_SCORE", ascending=False)
        st.header(fixture)
        for index, row in rows.iterrows():
            score = 'Good' if row["LLM_JUDGE_SCORE"] > 0 else '<span style="color:red">Poor</span>'
            hedges = 'No' if row["HEDGES"] == 0 else '<span style="color:red">Yes</span>'
            verbose = 'No' if row["VERBOSE"] == 0 else '<span style="color:red">Yes</span>'

            st.markdown(f"""-----

🤖 **LLM Judge Score**: {score} | 🤔 **Hedges**: {hedges} | 🕑 **Verbose**: {verbose}

**Question**: {row["CHAT_QUESTION"]}

**Question Class**: {row["QUESTION_CLASS"]}

**Response**: {row["CHAT_REPLY"]}

""", unsafe_allow_html=True)


def emojify(b: bool):
    return "✅" if bool(b) else "❌"


def unit_test_csv_table(name: str):
    df = pd.read_csv(name)

    df['TEST_MATCHES_EXPECTED_TEST_FILE'] = df['TEST_EXPECTED_FILENAME'] == df['TEST_FILENAME']

    score_df = df.groupby("FIXTURE")[
        ["TEST_MATCHES_EXPECTED_TEST_FILE", "TEST_USED_EXPECTED_TEST_FRAMEWORK"]].sum().reset_index()
    score_df.columns = ["Fixture", "Expected path", "Expected framework"]
    score_df = score_df.sort_values(by="Expected path", ascending=False)

    score_df = score_df.set_index("Fixture")
    st.dataframe(score_df)

    selected_test = st.selectbox(
        "Select a test", df["TEST_NAME"].unique())

    filtered_models = st.multiselect(
        "Filter models", df["FIXTURE"].unique())

    rows = df[(df["TEST_NAME"] == selected_test) & (
        (len(filtered_models) == 0) | (df["FIXTURE"].isin(filtered_models)))]

    rows = rows.sort_values(by="FIXTURE")

    for _, row in rows.iterrows():
        st.header(row["FIXTURE"])
        expected_filename = row['TEST_EXPECTED_FILENAME']
        actual_filename = row['TEST_FILENAME']
        test_files_match = expected_filename == actual_filename
        expected_actual_text = f"(expected: {expected_filename}, actual: {actual_filename})"
        has_errors = row["TEST_LANGUAGE"] == "typescript" and bool(
            row["TEST_HAS_TYPESCRIPT_ERRORS"])

        st.markdown(f"""-----
**Correct file path?** {emojify(test_files_match)} {expected_filename if test_files_match else expected_actual_text}

**Correct framework?** {emojify(row["TEST_USED_EXPECTED_TEST_FRAMEWORK"])}

{"**No Typescript errors?** " + emojify(not has_errors) if row["TEST_LANGUAGE"] == "typescript" else ""}\n

{row["TEST_DIAGNOSTICS"] if has_errors and row["TEST_DIAGNOSTICS"] else ""}


**Generated test:**
```{row['TEST_LANGUAGE']}
{row["TEST_GENERATED"]}
```
""", unsafe_allow_html=True)


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
