import numpy as np
from datetime import datetime, timedelta

def LH1_Forecasting(PG_cursor, PG_conn, model_LH_Forecasting):
    try:
        query_crontime = '''SELECT "CronTime" FROM "DCS_Items" ORDER BY "CronTime" DESC LIMIT 1'''
        PG_cursor.execute(query_crontime)
        crontime = PG_cursor.fetchone()
        crontime = crontime[0]
        if isinstance(crontime, str):
            crontime = datetime.strptime(crontime, '%Y-%m-%d %H:%M:%S')
        # Stage 1: 
            # Query DATA_CTCN
        query_DATA_CTCN = '''SELECT "LDA12080012000243", "LDA12080012000228", "LDA12080012000227", "LDA12080012000230",
        "LDA12080012000238", "LDA12080012000237", "LDA12080012000232", "LDA12080012000236",
        "LDA12080012000235", "LDA12080012000234", "LDA12080012000233" FROM "DATA_CTCN" ORDER BY "CronTime" DESC LIMIT 1'''
        PG_cursor.execute(query_DATA_CTCN)
        DATA_CTCN = PG_cursor.fetchone()
        # print(DATA_CTCN)
        DATA_CTCN = [float(value) for value in DATA_CTCN]
            # Query DCS_Items
        query_DCS_Items = '''SELECT "B1_FT1151_DACA_PV__Value", "B1_TE1251_DACA_PV__Value","B2_FT1151_DACA_PV__Value",
        "B1_Z_BEDT_DACA_PV__Value", "B1_PT1281_DACA_PV__Value", "B1_AT1011_DACA_PV__Value", 
        "B1_AT1012_DACA_PV__Value", "B1_TE1212_DACA_PV__Value", "B1_PT1061_DACA_PV__Value","B1_PT1071_DACA_PV__Value", 
        "B1_PT1111_DACA_PV__Value","B1_PT1112_DACA_PV__Value", "B1_PT1211_DACA_PV__Value","B1_PT1212_DACA_PV__Value", 
        "B1_TZ1131ZT_DACA_PV__Value","B1_S051AIT_DACA_PV__Value", "B1_AZ1011ZT_DACA_PV__Value","B1_S052AIT_DACA_PV__Value", 
        "B1_S052AVFD_CRT_DACA_PV__Value","B1_S052AVFD_FB_DACA_PV__Value", "B1_PT1081_DACA_PV__Value","B1_PT1082_DACA_PV__Value", 
        "B1_PT1091_DACA_PV__Value","B1_PT1092_DACA_PV__Value", "B1_TE1111_DACA_PV__Value","B1_TE1112_DACA_PV__Value", 
        "B1_FT1151_DIVA_OUT__Value" FROM "DCS_Items" ORDER BY "CronTime" DESC LIMIT 1'''
        PG_cursor.execute(query_DCS_Items)
        DCS_Items = PG_cursor.fetchone()
        DCS_Items = [float(value) for value in DCS_Items]
        # print(DCS_Items)

        # Create input:
        input = DATA_CTCN + DCS_Items
        
        # Predict:
        input = np.array(input).reshape(1, -1)
        # print(input)
        LH1_Forecasting = model_LH_Forecasting.predict(input)
        
        # print("LH1_Forecasting:", LH1_Forecasting)

        # Truy vấn bảng "DATA_LH1_Forecasting" để lấy tên cột
        PG_cursor.execute('SELECT * FROM "DATA_LH1_Forecasting" LIMIT 1')
        name_columns = [desc[0] for desc in PG_cursor.description]

        # Tạo chuỗi cột và placeholders cho câu lệnh INSERT
        placeholders = ', '.join(['%s'] * len(name_columns))
        columns = ', '.join([f'"{col}"' for col in name_columns])

        crontime = (crontime + timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:00')
        values = [crontime] + [float(x) for x in LH1_Forecasting[0]]
        # print(values)
        insert_query = f'''
        INSERT INTO "DATA_LH1_Forecasting" ({columns}) VALUES ({placeholders})
        '''
        PG_cursor.execute(insert_query, values)
        PG_conn.commit() 
    except Exception as e:
        PG_conn.rollback()
        print(f"An error occurred: {e}")
        pass

def LH2_Forecasting(PG_cursor, PG_conn, model_LH_Forecasting):
    try:
        query_crontime = '''SELECT "CronTime" FROM "DCS_Items" ORDER BY "CronTime" DESC LIMIT 1'''
        PG_cursor.execute(query_crontime)
        crontime = PG_cursor.fetchone()
        crontime = crontime[0]
        if isinstance(crontime, str):
            crontime = datetime.strptime(crontime, '%Y-%m-%d %H:%M:%S')
        # Stage 1: 
            # Query DATA_CTCN
        query_DATA_CTCN = '''SELECT "LDA12080012000243", "LDA12080012000228", "LDA12080012000227", "LDA12080012000230",
        "LDA12080012000238", "LDA12080012000237", "LDA12080012000232", "LDA12080012000236",
        "LDA12080012000235", "LDA12080012000234", "LDA12080012000233" FROM "DATA_CTCN" ORDER BY "CronTime" DESC LIMIT 1'''
        PG_cursor.execute(query_DATA_CTCN)
        DATA_CTCN = PG_cursor.fetchone()
        # print(DATA_CTCN)
        DATA_CTCN = [float(value) for value in DATA_CTCN]
            # Query DCS_Items
        query_DCS_Items = '''SELECT "B2_FT1151_DACA_PV__Value", "B2_TE1251_DACA_PV__Value","B1_FT1151_DACA_PV__Value",
        "B2_Z_BEDT_DACA_PV__Value", "B2_PT1281_DACA_PV__Value", "B2_AT1011_DACA_PV__Value", 
        "B2_AT1012_DACA_PV__Value", "B2_TE1212_DACA_PV__Value", "B2_PT1061_DACA_PV__Value","B2_PT1071_DACA_PV__Value", 
        "B2_PT1111_DACA_PV__Value","B2_PT1112_DACA_PV__Value", "B2_PT1211_DACA_PV__Value","B2_PT1212_DACA_PV__Value", 
        "B2_TZ1131ZT_DACA_PV__Value","B2_S051AIT_DACA_PV__Value", "B2_AZ1011ZT_DACA_PV__Value","B2_S052AIT_DACA_PV__Value", 
        "B2_S052AVFD_CRT_DACA_PV__Value","B2_S052AVFD_FB_DACA_PV__Value", "B2_PT1081_DACA_PV__Value","B2_PT1082_DACA_PV__Value", 
        "B2_PT1091_DACA_PV__Value","B2_PT1092_DACA_PV__Value", "B2_TE1111_DACA_PV__Value","B2_TE1112_DACA_PV__Value", 
        "B2_FT1151_DIVA_OUT__Value" FROM "DCS_Items" ORDER BY "CronTime" DESC LIMIT 1'''
        PG_cursor.execute(query_DCS_Items)
        DCS_Items = PG_cursor.fetchone()
        DCS_Items = [float(value) for value in DCS_Items]
        # print(DCS_Items)

        # Create input:
        input = DATA_CTCN + DCS_Items
        
        # Predict:
        input = np.array(input).reshape(1, -1)
        # print(input)
        LH2_Forecasting = model_LH_Forecasting.predict(input)
        
        # print("LH2_Forecasting:", LH2_Forecasting)

        # Truy vấn bảng "DATA_LH2_Forecasting" để lấy tên cột
        PG_cursor.execute('SELECT * FROM "DATA_LH2_Forecasting" LIMIT 1')
        name_columns = [desc[0] for desc in PG_cursor.description]

        # Tạo chuỗi cột và placeholders cho câu lệnh INSERT
        placeholders = ', '.join(['%s'] * len(name_columns))
        columns = ', '.join([f'"{col}"' for col in name_columns])

        crontime = (crontime + timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:00')
        values = [crontime] + [float(x) for x in LH2_Forecasting[0]]
        # print(values)
        insert_query = f'''
        INSERT INTO "DATA_LH2_Forecasting" ({columns}) VALUES ({placeholders})
        '''
        PG_cursor.execute(insert_query, values)
        PG_conn.commit() 
    except Exception as e:
        PG_conn.rollback()
        print(f"An error occurred: {e}")
        pass

def LN_Forecasting(PG_cursor, PG_conn, model_LN_Forecasting):
    try:
        query_crontime = '''SELECT "CronTime" FROM "DCS_Items" ORDER BY "CronTime" DESC LIMIT 1'''
        PG_cursor.execute(query_crontime)
        crontime = PG_cursor.fetchone()
        crontime = crontime[0]
        if isinstance(crontime, str):
            crontime = datetime.strptime(crontime, '%Y-%m-%d %H:%M:%S')
            # Query DATA_CTCN
        query_DATA_CTCN = '''SELECT "LDA11070012000630", "LDA07060012000122",
            "LDA07060012000155", "LDA07060012000156", "LDA07060012000157",
            "LDA07060012000158", "LDA07060012000159", "LDA07060012000160",
            "LDA07060012000161", "LDA07060012000162", "LDA07060012000163",
            "LDA07060012000164", "LDA07060012000165", "LDA07060012000166" FROM "DATA_CTCN" ORDER BY "CronTime" DESC LIMIT 1'''
        PG_cursor.execute(query_DATA_CTCN)
        DATA_CTCN = PG_cursor.fetchone()
        # print(DATA_CTCN)
        DATA_CTCN = [float(value) for value in DATA_CTCN]
            # Query DCS_Items
        query_DCS_Items = '''SELECT "CM_A181_V19_COM_V19_IN_5_PV3__Value", "CM_A181FT0010_DACA_PV__Value",
            "CM_A181FT0001_DACA_PV__Value", "CM_A181PT0013_DACA_PV__Value",
            "CM_A181AT0001_DACA_PV__Value", "CM_A181PT0002_DACA_PV__Value",
            "CM_A181PT0003_DACA_PV__Value", "CM_A181PT0004_DACA_PV__Value",
            "CM_A181PDT0002_DACA_PV__Value", "CM_A181PT0005_DACA_PV__Value",
            "CM_A181PT0006_DACA_PV__Value", "CM_A181PT0007_DACA_PV__Value",
            "CM_A181PT0008_DACA_PV__Value", "CM_A181TE0007_DACA_PV__Value",
            "CM_A181S015BPGPV_DACA_PV__Value", "CM_A181_TIEUHAOCO_OUT__Value" FROM "DCS_Items" ORDER BY "CronTime" DESC LIMIT 1'''
        PG_cursor.execute(query_DCS_Items)
        DCS_Items = PG_cursor.fetchone()
        DCS_Items = [float(value) for value in DCS_Items]
        # print(DCS_Items)

        # Create input:
        input = DATA_CTCN + DCS_Items
        
        # Predict:
        input = np.array(input).reshape(1, -1)
        # print(input)
        LN_Forecasting = model_LN_Forecasting.predict(input)
        
        # print("LN_Forecasting:", LN_Forecasting)

        # Truy vấn bảng "DATA_LN_Forecasting" để lấy tên cột
        PG_cursor.execute('SELECT * FROM "DATA_LN_Forecasting" LIMIT 1')
        name_columns = [desc[0] for desc in PG_cursor.description]

        # Tạo chuỗi cột và placeholders cho câu lệnh INSERT
        placeholders = ', '.join(['%s'] * len(name_columns))
        columns = ', '.join([f'"{col}"' for col in name_columns])

        crontime = (crontime + timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:00')
        values = [crontime] + [float(x) for x in LN_Forecasting[0]]
        # print(values)
        insert_query = f'''
            INSERT INTO "DATA_LN_Forecasting" ({columns}) VALUES ({placeholders})
            '''
        PG_cursor.execute(insert_query, values)
        PG_conn.commit() 
    except Exception as e:
        PG_conn.rollback()
        print(f"An error occurred: {e}")
        pass