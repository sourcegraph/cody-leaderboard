import streamlit as st
import pandas as pd

def chat_csv_table(name: str):
    df = pd.read_csv(name)
    df["LLM_JUDGE_SCORE"] = df["LLM_JUDGE_SCORE"].apply(
        lambda x: 0 if x == 0 else 1)
    df["CONCISENESS_SCORE"] = df["CONCISENESS_SCORE"].apply(lambda x: 1 if x > 0 else 0)
    df["CONFIDENCE_SCORE"] = df["HEDGES"].apply(lambda x: 1 if x == 0 else 0)

    st.subheader("Summary")
    grouped_df = df.groupby("FIXTURE")
    num_questions = grouped_df.size().iloc[0]

    score_df = grouped_df[["LLM_JUDGE_SCORE", "CONFIDENCE_SCORE", "CONCISENESS_SCORE"]].sum().reset_index()
    score_df.columns = ["FIXTURE", "LLM Judge Score", "Confident", "Concise"]
    score_df[["LLM Judge Score", "Confident", "Concise"]] = (score_df[["LLM Judge Score", "Confident", "Concise"]] / num_questions).round(2)
    models_by_score = score_df["FIXTURE"].values.tolist()
    score_df = score_df.sort_values(by="LLM Judge Score", ascending=False)
    score_df = score_df.set_index("FIXTURE")

    st.dataframe(score_df)
    st.markdown(f'''
Average score across all **{num_questions} questions**. Scores of 1 are 'good', meaning averages closer to 1.0 are better.
* LLM judge score: whether an LLM judge deemed the response to be helpful and informative.
* Confident: whether the model responds affirmatively, without excessive hedging like apologizing.
* Concise: whether the model responds succinctly, instead of repeating itself or adding extra content.''')

    pivot_df = df.pivot(index=["CHAT_QUESTION", "QUESTION_CLASS"],
                        columns="FIXTURE", values="LLM_JUDGE_SCORE")
    pivot_df = pivot_df.replace(0, 'Poor').replace(1, 'Good')
    pivot_df = pivot_df.sort_values(by="QUESTION_CLASS")
    pivot_df = pivot_df[models_by_score]

    st.subheader("All scores")
    st.dataframe(pivot_df.style.map(
        lambda score: 'background-color: #ffdddd' if score == 'Poor' else '', subset=pivot_df.columns))

    st.markdown(f'''LLM judge score for each model and each question. **Note: these scores are noisy**, and are intended only as a starting point for analysis.''')

    st.subheader("Model responses")
    selected_question = st.selectbox(
        "Select question", df["CHAT_QUESTION"].unique())
    filtered_models = st.multiselect("Filter models", df["FIXTURE"].unique())

    rows = df[(df["CHAT_QUESTION"] == selected_question) & (
        (len(filtered_models) == 0) | (df["FIXTURE"].isin(filtered_models)))]
    fixtures = rows.groupby("FIXTURE")

    for fixture, rows in fixtures:
        rows = rows.sort_values(by="LLM_JUDGE_SCORE", ascending=False)
        for index, row in rows.iterrows():
            score = 'Good' if row["LLM_JUDGE_SCORE"] == 1 else '<span style="color:red">Poor</span>'
            confident = 'Yes' if row["CONFIDENCE_SCORE"] == 1 else '<span style="color:red">No</span>'
            concise = 'Yes' if row["CONCISENESS_SCORE"] == 1 else '<span style="color:red">No</span>'

            st.markdown(f"""#### {fixture}

🤖 **LLM Judge Score**: {score} | 🤔 **Confident**: {confident} | 🕑 **Concise**: {concise}

**Question**: {row["CHAT_QUESTION"]} | **Question Class**: {row["QUESTION_CLASS"]}

**Response**: {row["CHAT_REPLY"]}

""", unsafe_allow_html=True)


def fix_csv_table(name: str):
    df = pd.read_csv(name)

    st.subheader("Summary")
    grouped_df = df.groupby("FIXTURE")
    num_questions = grouped_df.size().iloc[0]

    score_df = grouped_df["LLM_JUDGE_SCORE"].sum().reset_index()
    score_df.columns = ["FIXTURE", "Score"]
    score_df = score_df.sort_values(by="Score", ascending=False)
    models_by_score = score_df["FIXTURE"].values.tolist()

    score_df = score_df.set_index("FIXTURE")
    st.dataframe(score_df)
    st.markdown(f'''
Average score across all **{num_questions} questions**. Scores of 1 are 'good', meaning averages closer to 1.0 are better.
* Score: whether an LLM judge deemed the response to be high quality.''')

    filtered_df = df[["FIXTURE", "FILEPATH", "LLM_JUDGE_SCORE"]]
    # Pivot the DataFrame
    pivot_df = df.pivot(index="FILEPATH", columns="FIXTURE",
                        values="LLM_JUDGE_SCORE")
    pivot_df = pivot_df.sort_values(by=models_by_score, ascending=False)
    pivot_df = pivot_df.sort_values(by='FILEPATH')

    st.subheader("All scores")
    st.dataframe(pivot_df.style.map(
        lambda score: 'background-color: #ffdddd' if score == 0 else '', subset=pivot_df.columns))
    st.markdown(f'''LLM judge score for each model and each file. **Note: these scores are noisy**, and are intended only as a starting point for analysis.''')

    st.subheader("Model responses")
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
        st.markdown(f"""
#### {row["FIXTURE"]}

 **LLM-as-Judge score**: {row["LLM_JUDGE_SCORE"]}

 **Diff:**
 ```{row["LANGUAGEID"]}
 {row["EDIT_DIFF"]}
 ```

 **Diagnostic before**: {row["FIX_BEFORE_DIAGNOSTIC"]}

 **Diagnostic after**: {diagnostic_after}

 **LLM-as-Judge reasoning**: {row["LLM_JUDGE_REASONING"]}

 """)


def unit_test_csv_table(name: str):
    df = pd.read_csv(name)
    df['TEST_MATCHES_EXPECTED_TEST_FILE'] = df['TEST_EXPECTED_FILENAME'] == df['TEST_FILENAME']

    st.subheader("Summary")
    grouped_df = df.groupby("FIXTURE")
    num_questions = grouped_df.size().iloc[0]

    score_df = grouped_df[["TEST_MATCHES_EXPECTED_TEST_FILE", "TEST_USED_EXPECTED_TEST_FRAMEWORK"]].sum().reset_index()
    score_df.columns = ["Fixture", "Correct path", "Correct framework"]
    score_df[["Correct path", "Correct framework"]] = (score_df[["Correct path", "Correct framework"]] / num_questions).round(2)
    score_df = score_df.sort_values(by="Correct path", ascending=False)
    score_df = score_df.set_index("Fixture")

    st.dataframe(score_df)
    st.markdown(f'''
Average score across all **{num_questions} questions**. Scores of 1 are 'good', meaning averages closer to 1.0 are better.
* Correct path: whether the test path matched the expected one
* Correct framework: whether the test used the expected test framework''')

    st.subheader("Model responses")
    selected_test = st.selectbox(
        "Select a test", df["TEST_NAME"].unique())

    filtered_models = st.multiselect(
        "Filter models", df["FIXTURE"].unique())

    rows = df[(df["TEST_NAME"] == selected_test) & (
        (len(filtered_models) == 0) | (df["FIXTURE"].isin(filtered_models)))]

    rows = rows.sort_values(by="FIXTURE")

    for _, row in rows.iterrows():
        expected_filename = row['TEST_EXPECTED_FILENAME']
        actual_filename = row['TEST_FILENAME']
        test_files_match = expected_filename == actual_filename
        expected_actual_text = f"(expected: {expected_filename}, actual: {actual_filename})"
        diagnostics = row["TEST_DIAGNOSTICS"]

        st.markdown(f"""
#### {row["FIXTURE"]}
**Correct file path?** {emojify(test_files_match)} {expected_filename if test_files_match else expected_actual_text}

**Correct framework?** {emojify(row["TEST_USED_EXPECTED_TEST_FRAMEWORK"])}

{"**No Typescript errors?** " + emojify(not diagnostics) if row["TEST_LANGUAGE"] == "typescript" else ""}

{"Diagnostics: `" + str(diagnostics) + "`" if row["TEST_LANGUAGE"] == "typescript" and diagnostics  else ""}

**Generated test:**
```{row['TEST_LANGUAGE']}
{row["TEST_GENERATED"]}
```
""", unsafe_allow_html=True)


def emojify(b: bool):
    return "✅" if bool(b) else "❌"


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
