import os

import pandas as pd

df = pd.read_csv('queries.csv')

for index, row in df[df['Repo'] == 'cody'].iterrows():
    print(index, row['Question'])

    dir_ = f'input/chat_context/question_{index:03d}'
    os.makedirs(dir_, exist_ok=True)
    with open(os.path.join(dir_, 'question.yaml'), 'w+') as f:
        f.write('\n'.join([
            f'question: {row["Question"]}',
            f'class: {row["Class"]}',
        ]))
