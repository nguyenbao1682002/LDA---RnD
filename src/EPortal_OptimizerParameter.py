import numpy as np
from datetime import datetime, timedelta

def LN_EPortal(PG_cursor, PG_conn, model_LN_EPortal, model_LN_EPortal_COconsumption):
    # try:
        query_crontime = '''
            SELECT 
                "CronTime" 
            FROM "DCS_Items" ORDER BY "CronTime" DESC LIMIT 1
            '''
        PG_cursor.execute(query_crontime)
        crontime = PG_cursor.fetchone()
        crontime = crontime[0]
        if isinstance(crontime, str):
            crontime = datetime.strptime(crontime, '%Y-%m-%d %H:%M:%S')
            # Query DATA_CTCN
        query_DATA_CTCN = '''
            SELECT 
                "LDA07060012000157", "LDA07060012000158",
                "LDA07060012000166", "LDA11070012000630" 
            FROM "DATA_CTCN" ORDER BY "CronTime" DESC LIMIT 1
            '''
        PG_cursor.execute(query_DATA_CTCN)
        DATA_CTCN = PG_cursor.fetchone()
        # print(DATA_CTCN)
        DATA_CTCN = [float(value) for value in DATA_CTCN]

            # Query DCS_Items
        query_DCS_Items = '''
            SELECT 
                "CM_A181FT0001_DACA_PV__Value", "CM_A181PT0013_DACA_PV__Value", 
                "CM_A181_V19_COM_V19_IN_5_PV3__Value", "CM_A181TE0023_DACA_PV__Value",
                "CM_A181FT0010_DACA_PV__Value", "CM_A181AT0004_DACA_PV__Value",
                "CM_A181PDT0002_DACA_PV__Value", "CM_A181PT0002_DACA_PV__Value",
                "CM_A181PT0003_DACA_PV__Value", "CM_A181PT0004_DACA_PV__Value",
                "CM_A181PT0005_DACA_PV__Value", "CM_A181PT0006_DACA_PV__Value",
                "CM_A181PT0007_DACA_PV__Value", "CM_A181PT0008_DACA_PV__Value",
                "CM_A181_TIEUHAOCO_OUT__Value"
            FROM "DCS_Items" ORDER BY "CronTime" DESC LIMIT 1
            '''
        PG_cursor.execute(query_DCS_Items)
        DCS_Items = PG_cursor.fetchone()
        DCS_Items = [float(value) for value in DCS_Items]
        # print(DCS_Items)

        # Giảm giá trị CM_A181_TIEUHAOCO_OUT__Value xuống 95%
        DCS_Items[-1] = DCS_Items[-1] * 0.99

        # Create input:
        input = DATA_CTCN + DCS_Items
        
        # Predict:
        input = np.array(input).reshape(1, -1)
        # print(input)
        pred_LN_EPortal = model_LN_EPortal.predict(input)
        
        # print("LN_Forecasting:", LN_Forecasting)

        # Truy vấn bảng "DATA_LN_Forecasting" để lấy tên cột
        PG_cursor.execute(
            '''
            SELECT * FROM "DATA_LN_EPortal" LIMIT 1
            ''')
        name_columns = [desc[0] for desc in PG_cursor.description]

        # Tạo chuỗi cột và placeholders cho câu lệnh INSERT
        placeholders = ', '.join(['%s'] * len(name_columns))
        columns = ', '.join([f'"{col}"' for col in name_columns])
        crontime = (crontime + timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:00')

        input_COconsumption = np.hstack((input[:, :-1], pred_LN_EPortal))
        COconsumption = model_LN_EPortal_COconsumption.predict(input_COconsumption)
        print("COconsumption:", COconsumption)

        values = [crontime] + [float(x) for x in input[0][:-1]] + [float(x) for x in pred_LN_EPortal[0]] + [float(COconsumption[0])]
        print(values)
        insert_query = f'''
            INSERT INTO "DATA_LN_EPortal" ({columns}) VALUES ({placeholders})
            '''
        PG_cursor.execute(insert_query, values)
        PG_conn.commit() 
    # except Exception as e:
    #     PG_conn.rollback()
    #     print(f"An error occurred: {e}")
    #     pass