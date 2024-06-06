import streamlit as st
import pandas as pd


def csv_table(name: str):
    df = pd.read_csv(name)
    score_df = df.groupby("FIXTURE")["LLM_JUDGE_SCORE"].sum().reset_index()
    score_df.columns = ["FIXTURE", "Score"]
    score_df = score_df.sort_values(by="Score", ascending=False)
    models_by_score = score_df["FIXTURE"].values.tolist()

    score_df.set_index("FIXTURE", inplace=True)
    st.dataframe(score_df)

    filtered_df = df[["FIXTURE", "FILEPATH", "LLM_JUDGE_SCORE"]]
    # Pivot the DataFrame
    pivot_df = df.pivot(index="FILEPATH", columns="FIXTURE", values="LLM_JUDGE_SCORE")
    pivot_df.sort_values(by=models_by_score, ascending=False, inplace=True)
    pivot_df = pivot_df[models_by_score]

    # Display the pivoted DataFrame
    st.dataframe(pivot_df)
    # st.dataframe(filtered_df)

    # Add a selectbox to select a row
    selected_filepath = st.selectbox("Select a file", filtered_df["FILEPATH"].unique())

    # Display the edit diff in a code block with syntax highlighting
    rows = df[df["FILEPATH"] == selected_filepath]
    rows.sort_values(
        by="FIXTURE",
        key=lambda x: x.map(lambda fixture: models_by_score.index(fixture)),
        inplace=True,
    )

    for index, row in rows.iterrows():
        diagnostic_after = (
            "" if pd.isna(row["FIX_AFTER_DIAGNOSTIC"]) else row["FIX_AFTER_DIAGNOSTIC"]
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


fixTab, editTab, autocompleteTab, chatTab = st.tabs(
    ["Fix", "Edit", "Autocomplete", "Chat"]
)

with fixTab:
    st.header("Fix Command")
    csv_table("fix.csv")

with editTab:
    st.header("Edit Command")
    st.markdown("Coming soon!")

with autocompleteTab:
    st.header("Autocomplete")
    st.markdown("Coming soon!")

with chatTab:
    st.header("Chat")
    st.markdown("Coming soon!")
