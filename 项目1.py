import pandas as pd
from sqlalchemy import create_engine
# 只读前 200 万行
df = pd.read_csv(r"F:\UserBehavior.csv", nrows=2000000, header=None,
                 names=['user_id','item_id','category_id','behavior','timestamp'])
# 保存为新文件
df.to_csv(r"F:\UserBehavior_2M.csv", index=False, header=False)
print("已生成 200 万行数据文件")

import pandas as pd
from sqlalchemy import create_engine

# 数据库连接
engine = create_engine('mysql+pymysql://root:123456@localhost/itcast')

# 文件路径（使用 200 万行文件或原始大文件）
file_path = r"F:\UserBehavior_2M.csv"

# 分块大小（每次处理 10 万行）
chunksize = 100000
col_names = ['user_id', 'item_id', 'category_id', 'behavior', 'timestamp']

first_chunk = True
total_rows = 0

for chunk in pd.read_csv(file_path, header=None, names=col_names, chunksize=chunksize):
    # --- 数据清洗 ---
    # 去重
    chunk = chunk.drop_duplicates()
    # 删除空值
    chunk = chunk.dropna(subset=['user_id', 'behavior'])
    # 转换时间戳
    chunk['behavior_time'] = pd.to_datetime(chunk['timestamp'], unit='s')
    chunk['behavior_date'] = chunk['behavior_time'].dt.date
    # 过滤有效行为
    chunk = chunk[chunk['behavior'].isin(['pv', 'cart', 'fav', 'buy'])]

    # --- 写入 MySQL（DWD 表）---
    if first_chunk:
        chunk.to_sql('user_behavior_dwd', con=engine, if_exists='replace', index=False)
        first_chunk = False
    else:
        chunk.to_sql('user_behavior_dwd', con=engine, if_exists='append', index=False)

    total_rows += len(chunk)
    print(f"已处理 {total_rows} 行")

print("DWD 表生成完成！")