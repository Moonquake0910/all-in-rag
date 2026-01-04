import os
import json
import sqlite3
import numpy as np
from pprint import pprint
from typing import List, Dict, Any
from text2sql.text2sql_agent import SimpleText2SQLAgent

def demo():
    """简单演示"""
    
    # 数据库查询演示
    db_path = "demo.db"
    
    if os.path.exists(db_path):
        os.remove(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, city TEXT)")
    
    users_data = [(1, '张三', 25, '北京'), (2, '李四', 32, '上海'), (3, '王五', 35, '深圳')]
    cursor.executemany("INSERT INTO users VALUES (?, ?, ?, ?)", users_data)
    
    conn.commit()
    
    # 执行查询
    test_sqls = [
        ("查询所有用户", "SELECT * FROM users"),
        ("年龄大于30的用户", "SELECT * FROM users WHERE age > 30"),
        ("统计用户总数", "SELECT COUNT(*) FROM users")
    ]

    # 初始化Text2SQL代理
    agent = SimpleText2SQLAgent()
    # 连接数据库
    agent.connect_database(db_path)
    # 加载知识库
    agent.load_knowledge_base()
    
    for i, (question, sql) in enumerate(test_sqls, 1):
        print(f"\n问题 {i}: {question}")
        print("-" * 40)
        # print(f"SQL: {sql}")
        
        # cursor.execute(sql)
        # rows = cursor.fetchall()
        
        # if rows:
        #     print(f"返回 {len(rows)} 行数据")
        #     for j, row in enumerate(rows[:2], 1):
        #         print(f"  {j}. {row}")
            
        #     if len(rows) > 2:
        #         print(f"  ... 还有 {len(rows) - 2} 行")
        # else:
        #     print("无数据返回")

        # 调用Text2SQL代理讲查询转为SQL并执行
        result = agent.query(question)
        print("查询结果：")
        pprint(result, width=120, sort_dicts=False)
    
    agent.cleanup()

    conn.close()
    os.remove(db_path)


if __name__ == "__main__":
    demo()