import pandas as pd

dataframe = pd.read_excel('/home/diana/Downloads/ponctual_forecast(1).xlsx')
print(dataframe['Period'][0])
for i in dataframe:
    print(i)
    print(type(i))

