import streamlit as st
import pandas as pd


def csv_table(name: str):
    df = pd.read_csv(name)
    # Create a new DataFrame with the sum of LLM_JUDGE_SCORE for each FIXTURE
    score_df = df.groupby('FIXTURE')['LLM_JUDGE_SCORE'].sum().reset_index()
    score_df.columns = ['FIXTURE', 'Score']
    # Sort the DataFrame by Score in descending order
    score_df = score_df.set_index("FIXTURE").sort_values(by="Score", ascending=False)


    
    # Display the new DataFrame
    st.dataframe(score_df)

    # language_id_filter = st.selectbox("Select Language ID", df["LANGUAGEID"].unique())
    # filtered_df = df[df["LANGUAGEID"] == language_id_filter]
    filtered_df = df[['FIXTURE', 'FILEPATH', 'LLM_JUDGE_SCORE']]
     # Pivot the DataFrame
    pivot_df = df.pivot(index='FILEPATH', columns='FIXTURE', values='LLM_JUDGE_SCORE')
    
    # Display the pivoted DataFrame
    st.dataframe(pivot_df)
    # st.dataframe(filtered_df)

    # Add a selectbox to select a row
    selected_filepath = st.selectbox("Select a file", filtered_df["FILEPATH"].unique())

    # Display the edit diff in a code block with syntax highlighting
    for index, row in df[
        df["FILEPATH"] == selected_filepath
    ].iterrows():
        diagnostic_after = "" if pd.isna(row["FIX_AFTER_DIAGNOSTIC"]) else row["FIX_AFTER_DIAGNOSTIC"]
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




def fix():
    st.header("Fix Command")
    csv_table("fix.csv")


fix()
