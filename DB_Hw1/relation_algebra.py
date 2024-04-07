import pandas as pd
import numpy as np
 
sheet_names = [
    '第一世代寶可夢',
    '第二世代寶可夢',
    '第三世代寶可夢',
    '第四世代寶可夢',
    '第五世代寶可夢',
    '第六世代寶可夢',
    '第七世代寶可夢',
    '第八世代寶可夢',
    '第九世代寶可夢',
    '全圖鑑',
] 
dfs = {}

#-----------------------------------------------------------------------------------------------------------寶可夢圖鑑
def load():

    global dfs, sheet_names

    for sheet_name in sheet_names:
        df = pd.read_excel('DB_Hw1/pokemen.xlsx', sheet_name=sheet_name)
        df.columns = ['編號', '中文', '日文', '英文', '屬性', '額外屬性', 'HP',	'攻擊',	'防禦',	'特攻',	'特防',	'速度']
        df = df.dropna(subset=['編號'])
        for index, row in df.iterrows():
            if not pd.isna(row['額外屬性']):
                df.at[index, '屬性'] = row['屬性'] + ' / ' + row['額外屬性']
        df = df.drop(columns=['額外屬性'])
        dfs[sheet_name] = df

#-----------------------------------------------------------------------------------------------------------測試讀檔
    """
    for sheet_name, df in dfs.items():
        print(f"{sheet_name}:")
        print(df)
        print("=====================")

    """

#-----------------------------------------------------------------------------------------------------------store
def store(df):

    global dfs

    while True:
        new_name = input("請輸入儲存的名稱: ")
        if new_name == "":
            print("名稱不能為空。")
        else:
            break
    
    dfs[new_name] = df
    print(f"表格 {new_name} 已成功儲存。")

    # 更改顯示
    table()

def agree_store(df):

    agree = input("是否儲存該結果(y/n): ")

    if agree == 'y' or agree ==  'Y':
        store(df)

#-----------------------------------------------------------------------------------------------------------select
def select():

    table()
    table_id = input("請輸入要操作的表格編號: ")
    if not table_id.isdigit() or int(table_id) < 1 or int(table_id) > len(dfs):
        print("無效的表格編號。")
        return
    
    table_name = list(dfs.keys())[int( table_id ) - 1]
    print(f"表格 {table_name} 的列名：")
    for i, column in enumerate(dfs[table_name].columns):
        print(f"{i+1}: {column}")

    search_input = input("請輸入要搜尋的列名編號、搜尋值與比較運算子，以空格分隔: ").split()
    search_columns = [dfs[table_name].columns[int(search_input[0]) - 1]]
    search_values = search_input[1::2]
    comparison_operators = search_input[2::3]

    if len(search_input) % 3 != 0:
        print("輸入格式錯誤。請按照 '列名編號 搜尋值 比較運算子' 格式輸入，並以空格分隔。")
        return
    
    # Search & Display
    print("搜尋結果：")
    found = False
    found_first_match = False
    matching_rows = []
    for index, row in dfs[table_name].iterrows():
        match = True
        for column, value, op in zip(search_columns, search_values, comparison_operators):
            if op == '=':
                if str(row[column]) != value:
                    match = False
                    break
            elif op == '>':
                if not (str(row[column]) > value):
                    match = False
                    break
            elif op == '>=':
                if not (str(row[column]) >= value):
                    match = False
                    break
            elif op == '<':
                if not (str(row[column]) < value):
                    match = False
                    break
            elif op == '<=':
                if not (str(row[column]) <= value):
                    match = False
                    break
            elif op == '!=':
                if str(row[column]) == value:
                    match = False
                    break
            else:
                print("無效的比較運算子。")
                return

        if match:
            found = True
            # print attributes
            if not found_first_match:
                print( *row.index ) 
                found_first_match = True
            # print value
            print(*row.values)
            matching_rows.append(row)

    if not found:
        print("未找到符合條件的行。")

    # store
    else:
        matching_df = pd.DataFrame(matching_rows, columns = dfs[table_name].columns)
        agree_store(matching_df)

#------------------------------------------------------------------------------------------------------------project
def project():

    table()
    table_id = input("請輸入要操作的表格編號: ")
    if not table_id.isdigit() or int(table_id) < 1 or int(table_id) > len(dfs):
        print("無效的表格編號。")
        return
    
    table_name = list(dfs.keys())[int( table_id ) - 1]
    out_options = list(range( 1, len(dfs[table_name].columns ) + 1))
    print(f"表格 {table_name} 的列名：")
    for i, column in enumerate(dfs[table_name].columns):
        print(f"{i+1}: {column}")
    out = input("請輸入要顯示的列名編號，以空格分隔多個選項: ").split()
    
    output_data = []
    for option in out:
        if option.isdigit() and int( option ) in out_options:
            output_data.append(dfs[table_name].columns[int(option) - 1])
        else:
            print( "無效的輸出選項" )
            return
        
    print("\t".join(output_data))
    matching_rows = []
    for index, row in dfs[table_name].iterrows():
        print( *row[output_data], sep="\t" )
        matching_rows.append(row[output_data])

    # store
    matching_df = pd.DataFrame(matching_rows, columns = output_data)
    agree_store(matching_df)

#------------------------------------------------------------------------------------------------------------rename
def rename():

    global dfs

    table()
    table_id = input("請輸入要再命名的表格編號: ")
    if not table_id.isdigit() or int(table_id) < 1 or int(table_id) > len(dfs):
        print("無效的表格編號。")
        return

    # 再命名的table
    table_name = list(dfs.keys())[int(table_id) - 1]
    rename_table = dfs[table_name]

    store(rename_table)


#------------------------------------------------------------------------------------------------------------binary_operaters
def binary_operaters_interface():

    table()

    # 輸入要相乘的表格
    table_id1 = input("請輸入第一個表格的編號: ")
    if not table_id1.isdigit() or int(table_id1) < 1 or int(table_id1) > len(dfs):
        print("無效的表格編號。")
        return
    table_name1 = list(dfs.keys())[int( table_id1 ) - 1]

    table_id2 = input("請輸入第二個表格的編號: ")
    if not table_id2.isdigit() or int(table_id2) < 1 or int(table_id2) > len(dfs):
        print("無效的表格編號。")
        return
    table_name2 = list(dfs.keys())[int( table_id2 ) - 1]

    if table_name1 not in dfs or table_name2 not in dfs:
        print("表格名稱不存在")
        return None

    df1 = dfs[table_name1]
    df2 = dfs[table_name2]
    return df1, df2

#------------------------------------------------------------------------------------------------------------cartesian_product
def cartesian_product(df1, df2):
    
    cartesian = []
    
    for index1, row1 in df1.iterrows():
        for index2, row2 in df2.iterrows():
            cartesian.append(list(row1) + list(row2))
    
    columns = list(df1.columns) + list(df2.columns)
    cartesian_df = pd.DataFrame(cartesian, columns=columns)
    
    return cartesian_df


#------------------------------------------------------------------------------------------------------------union
def union(df1, df2):

    df1 = df1.reset_index(drop=True)
    df2 = df2.reset_index(drop=True)

    union = pd.concat([df1, df2]).drop_duplicates().reset_index(drop=True)
    return union

#------------------------------------------------------------------------------------------------------------set_different
def set_diff(df1, df2):
    
    set_diff = df1.merge(df2, indicator=True, how='left').loc[lambda x: x['_merge'] == 'left_only'].drop(columns='_merge')
    return set_diff

#------------------------------------------------------------------------------------------------------------set_intersection
def set_inter(df1, df2):

    diff1 = set_diff(df1, df2)
    diff2 = set_diff(df2, df1)

    union_set = union(df1, df2)
    
    intersection = set_diff(union_set, diff1)
    intersection = set_diff(intersection, diff2)
    
    if intersection.empty:
        print("交集為空")
        return pd.DataFrame()
    return intersection

#------------------------------------------------------------------------------------------------------------division
def division(df1, df2):
    """
    intersection_set = set_inter(df1, df2)
    
    # 交集為空
    if intersection_set.empty:
        return pd.DataFrame()
    
    diff1 = set_diff(df1, df2)
    
    # 除法結果計算為差集與交集的聯集
    division_result = union(diff1, intersection_set)
    
    return division_result
    """
    # 找到關係 R 中存在但不在 S 中存在的屬性集合 Y
    common_columns = df1.columns.intersection(df2.columns)
    Y = df1.columns.difference(df2.columns)
    
    # 找到 R 中屬性 Y 的所有值組
    result = df1
    
    # 篩選出在 S 中每個值組 ts 都存在的值組
    for index, row in df2.iterrows():
        condition = True
        for column in common_columns:
            condition = condition & (result[column] == row[column])
        result = result[~condition]
    
    # 返回關係 T(Y)
    return result[Y] if not result.empty else pd.DataFrame()

#------------------------------------------------------------------------------------------------------------natural_join
def natural_join(df1, df2):
    """
    # 取得兩個表格的列名
    columns1 = df1.columns.tolist()
    columns2 = df2.columns.tolist()
    
    # 共同列名
    common_columns = list(set(columns1) & set(columns2))
    
    # 無共同列名
    if not common_columns:
        return "沒有共同列名"
    
    # 找到共同列名的索引
    idx1 = [columns1.index(col) for col in common_columns]
    idx2 = [columns2.index(col) for col in common_columns]
    
    # 初始化結果 DataFrame
    join_result = pd.DataFrame(columns=columns1+df2.loc[:, ~df2.columns.isin(common_columns)].columns.tolist())
    print( join_result.columns)
    
    # 根據共同列名進行交集
    for index1, row1 in df1.iterrows():
        for index2, row2 in df2.iterrows():
            # 檢查共同列的值是否相等
            match = True
            for i in range(len(common_columns)):
                if row1.iloc[idx1[i]] != row2.iloc[idx2[i]]:
                    match = False
                    break
            if match:
                # 合併兩行並添加到結果中
                combined_row = pd.concat([row1, row2], ignore_index=True)
                join_result = pd.concat([join_result, combined_row], ignore_index=True)
    
    if join_result.empty:
        print("自然集合為空")
        
    return join_result
    """

    # 取得兩個表格的列名
    columns1 = df1.columns.tolist()
    columns2 = df2.columns.tolist()

    # 共同列名
    common_columns = list(set(columns1) & set(columns2))

    # 無共同列名
    if not common_columns:
        return "沒有共同列名"

    # 初始化結果 DataFrame
    join_result = pd.DataFrame(columns=columns1 + [col for col in columns2 if col not in common_columns])

    # 根據共同列名進行交集
    for index1, row1 in df1.iterrows():
        for index2, row2 in df2.iterrows():
            match = True
            # 檢查共同列的值是否相等
            for col in common_columns:
                if row1[col] != row2[col]:
                    match = False
                    break
            if match:
                # 合併兩行並添加到結果中
                combined_row = {**row1, **{col: row2[col] for col in columns2 if col not in common_columns}}
                join_result = join_result._append(combined_row, ignore_index=True)

    if join_result.empty:
        print("自然集合為空")

    return join_result

#------------------------------------------------------------------------------------------------------------list
def table():

    print("所有表格：")
    print("=====================")
    for index, ( table_name, _ ) in enumerate( dfs.items(), start=1 ):
        print(f"{index} : {table_name}")
    print("=====================")

def tables_schema():

    print("所有表格：")
    print("=====================")
    for id, (table_name, df) in enumerate(dfs.items(), start=1):
        print(f"{id} : {table_name}")
        print("---" , end="")
        print(", ".join(df.columns.tolist()))
    print("=====================")


#------------------------------------------------------------------------------------------------------------reload
def reload():

    global dfs
    dfs.clear()
    load()
    print("數據已回歸原始狀態 (•͈⌔•͈⑅)~")

#------------------------------------------------------------------------------------------------------------print
def print_main():

    options = ["Quit", "Select", "Project", "Rename", "Cartesian Product", "Set Union", "Set Difference", "Set Intersection", "Division", "Natural Join", "Print Schema", "Reload Data"]
    print("☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆")
    for id, option in enumerate(options):
        print(f"{id} : {option}")
    print("☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆")

def print_result(result):

    if not result.empty:
        print(result)

        # store
        agree_store(result)

#------------------------------------------------------------------------------------------------------------main
load()

while True:
    print_main()
    command = input("What do you want to do?: ")
    if command == '0':
        break
    elif command == '1':
        select()
    elif command == '2':
        project()
    elif command == '3':
        rename()
    elif command == '4':
        table1, table2 = binary_operaters_interface()
        print_result(cartesian_product(table1, table2))
    elif command == '5':
        table1, table2 = binary_operaters_interface()
        print_result(union(table1, table2))
    elif command == '6':
        table1, table2 = binary_operaters_interface()
        print_result(set_diff(table1, table2))
    elif command == '7':
        table1, table2 = binary_operaters_interface()
        print_result(set_inter(table1, table2))
    elif command == '8':
        table1, table2 = binary_operaters_interface()
        print_result(division(table1, table2))
    elif command == '9':
        table1, table2 = binary_operaters_interface()
        print_result(natural_join(table1, table2))
    elif command == '10':
        tables_schema()
    elif command == '11':
        reload()
    else:
        print("Invalid command. Please enter again.")

