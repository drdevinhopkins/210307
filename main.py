import pandas as pd

df = pd.DataFrame([{
    'num': 2,
    'text': 'hey'
}, {'num': 5, 'text': 'hello'}])

df.to_csv('test.csv')
