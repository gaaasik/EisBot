import sqlite3

conn = sqlite3.connect('tenders.db')
cursor = conn.cursor()


defineTable = 'tenders.db'


def insert_data_in_db(table, dict_data_tender, all_key):
    conn = sqlite3.connect(defineTable)
    cursor = conn.cursor()
    cursor.execute('''
               INSERT INTO tenders (number, url, name, price, employer, dateStartAuction, dateUpdate, datePost, platform, securityRequest, typeAuction, region, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
           ''', (dict_data_tender["number"],
                 dict_data_tender["url"],
                 dict_data_tender[all_key["key_name"]],
                 dict_data_tender[all_key["key_price"]],
                 dict_data_tender[all_key["key_employer"]],
                 dict_data_tender[all_key["key_dateStartAuction"]],
                 dict_data_tender[all_key["key_dateUpdate"]],
                 dict_data_tender[all_key["key_datePost"]],
                 dict_data_tender[all_key["key_platform"]],
                 dict_data_tender[all_key["key_securityRequest"]],
                 dict_data_tender[all_key["key_typeAuction"]],
                 dict_data_tender[all_key["key_region"]],
                 dict_data_tender[all_key["key_status"]]
                 ))
    conn.commit()




    # cursor.execute(f"""INSERT INTO {table}(number, url, name, price, employer, dateStartAuction, dateUpdate, datePost, platform, securityRequest, typeAuction, region, status, checking_notifications)
    #     VALUES ({all_data_tender["number"]},
    #             {all_data_tender["url"]},
    #             {all_data_tender[all_key["key_name"]]},
    #             {all_data_tender[all_key["key_price"]]},
    #             {all_data_tender[all_key["key_employer"]]},
    #             {all_data_tender[all_key["key_dateStartAuction"]]},
    #             {all_data_tender[all_key["key_dateUpdate"]]},
    #             {all_data_tender[all_key["key_datePost"]]},
    #             {all_data_tender[all_key["key_platform"]]},
    #             {all_data_tender[all_key["key_securityRequest"]]},
    #             {all_data_tender[all_key["key_typeAuction"]]},
    #             {all_data_tender[all_key["key_region"]]},
    #             {all_data_tender[all_key["key_status"]]});""")


def select_true_false_db(table, column, value):
    conn = sqlite3.connect(defineTable)
    cursor = conn.cursor()
    cursor.execute(f'''SELECT {column} FROM {table} WHERE {column} = "{value}" ''')
    return cursor.fetchone() is not None


def select_db(table, column):
    conn = sqlite3.connect(defineTable)
    cursor = conn.cursor()
    cursor.execute(f"""SELECT {column} FROM {table}  """)
    print(cursor.fetchall())
    print("0149200002324004449" in cursor.fetchall())
    return cursor



def creatTable_db():
    conn = sqlite3.connect(defineTable)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tenders (
            tender_id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT,
            url TEXT,
            name TEXT,
            price TEXT,
            employer TEXT,
            dateStartAuction TEXT,
            dateUpdate TEXT,
            datePost TEXT,
            platform TEXT,
            securityRequest TEXT,
            typeAuction TEXT,
            region TEXT,
            status TEXT,
            checking_notifications BOOLEAN DEFAULT 0
        );''')

    conn.commit()




# Тест для заполнения таблицы
# def values_db(table, list_value):
#     conn = sqlite3.connect(defineTable)
#     cursor = conn.cursor()
#     try:
#         cursor.execute(f"INSERT INTO {table} VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?);", list_value)
#         conn.commit()
#     except sqlite3.OperationalError:
#         print("id уже есть")
#     cursor.close(defineTable)
