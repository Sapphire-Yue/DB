    for index, row in df2.iterrows():
        condition = False
        for column in common_columns:
            condition = condition | (result[column] == row[column])
        result = result[condition]
        print(result)