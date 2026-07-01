import numpy as np
from datetime import datetime
import pandas as pd
def LH1_HistoryParameter(PG_cursor, PG_conn, model_LH1_HistoryParameter):
    """
    1. Workflow:
        Tìm kiếm bộ thông số Local dựa trên dữ liệu chất lượng than mới nhất hiện tại.
        - Giai đoạn 1: Lấy thời gian gần nhất từ bảng DCS_Items
        - Giai đoạn 2: Lấy dữ liệu vận hành gần nhất từ bảng DATA_CTCN
        - Giai đoạn 3: Tạo dữ liệu đầu vào
        - Giai đoạn 4: Tìm kiếm bộ thông số phù hợp với mức tải
        - Giai đoạn 5: Tra cứu nếu tiêu hao đó là thấp nhất trong ca thì lấy bộ thông số đó
        - Giai đoạn 6: Lưu thông số vào database
        
    2. Parameters:
        PG_cursor: Cursor để thực thi truy vấn SQL.
        PG_conn: Kết nối đến database PostgreSQL.
        model_LH1_HistoryParameter: Mô hình ML dự đoán tham số lịch sử.
        model_LH1_CoalConsumption: Mô hình ML dự đoán tiêu hao than.
    """
    try:
        print("Start LH1_HistoryParameter")

        query_crontime = '''
            SELECT "CronTime" 
            FROM "DCS_Items" 
            ORDER BY "CronTime" DESC 
            LIMIT 1
            '''
        PG_cursor.execute(query_crontime)
        crontime = PG_cursor.fetchone()

        # Giai đoạn 1: Lấy thời gian gần nhất từ bảng DCS_Items
        query_DATA_CTCN = '''
            SELECT "LDA12080012000243", "LDA12080012000228", "LDA12080012000227", "LDA12080012000230",
            "LDA12080012000238", "LDA12080012000237", "LDA12080012000232", "LDA12080012000236",
            "LDA12080012000235", "LDA12080012000234", "LDA12080012000233" 
            FROM "DATA_CTCN" 
            ORDER BY "CronTime" DESC 
            LIMIT 1
            '''
        PG_cursor.execute(query_DATA_CTCN)
        DATA_CTCN = PG_cursor.fetchone()
        DATA_CTCN = [float(value) for value in DATA_CTCN]
        # print(DATA_CTCN)

        # Giai đoạn 2: Lấy dữ liệu vận hành gần nhất từ bảng DATA_CTCN
        query_DCS_Items = '''
            SELECT "B1_FT1151_DACA_PV__Value", "B1_TE1251_DACA_PV__Value","B2_FT1151_DACA_PV__Value" 
            FROM "DCS_Items" 
            ORDER BY "CronTime" DESC 
            LIMIT 1
            '''
        PG_cursor.execute(query_DCS_Items)
        DCS_Items = PG_cursor.fetchone()
        DCS_Items = [float(value) for value in DCS_Items]

        # Phuong an duoi la phuong an moi thang 9/2025
        # power = DCS_Items[0]
        # df_baseparameter = pd.read_csv('../baseparameters/baseparameter_LH1.csv')
        # print(df_baseparameter)
        # bins = df_baseparameter['power_bin'].unique()
        # # Tìm bin gần nhất với công suất hiện tại
        # nearest_bin = min(bins, key=lambda x: abs(x - power))
        # # Lấy bộ thông số tương ứng
        # row = df_baseparameter[df_baseparameter['power_bin'] == nearest_bin].iloc[0]

        # Giai đoạn 3: Tạo dữ liệu đầu vào
        input = DATA_CTCN + DCS_Items
        input = np.array(input).reshape(1, -1)

        # Giai đoạn 4: Tìm kiếm bộ thông số phù hợp với mức tải và tính toán tiêu hao
        HistoryParameter = model_LH1_HistoryParameter.predict(input)
        print(f"HistoryParameter : {HistoryParameter}")
        hp_slice = np.array(HistoryParameter[0][:-1]).reshape(1, -1)
        input_coalconsumption = np.hstack((input, hp_slice))
        # input_coalconsumption = np.hstack((input, HistoryParameter))
        # OptimizerParameter_CoalConsumption = model_LH1_CoalConsumption.predict(input_coalconsumption)
        # OptimizerParameter_CoalConsumption = float(OptimizerParameter_CoalConsumption[0])
        if DCS_Items[0] == 0:
            OptimizerParameter_CoalConsumption = 0
        else:
            OptimizerParameter_CoalConsumption = HistoryParameter[0][-1]/DCS_Items[0]
        print("OptimizerParameter_CoalConsumption:", HistoryParameter[0][-1], DCS_Items[0])

        # Giai đoạn 5: Tra cứu nếu tiêu hao đó là thấp nhất trong ca thì lấy bộ thông số đó
        query_CoalConsumption = '''
            SELECT * 
            FROM "DATA_LH1_HistoryParameter" 
            ORDER BY "CronTime" DESC 
            LIMIT 1
            '''
        PG_cursor.execute(query_CoalConsumption)
        HistoryParameter_CoalConsumption = PG_cursor.fetchone()
        HistoryParameter_CoalConsumption = [float(value) for value in HistoryParameter_CoalConsumption[1:]]
        # print("HistoryParameter:", HistoryParameter_CoalConsumption[-1])
        # print("OptimizerParameter_CoalConsumption:", OptimizerParameter_CoalConsumption)
        target_times = ["06:00:00", "14:00:00", "22:00:00", "06:01:00", "14:01:00", "22:01:00"]
        cron_datetime = crontime[0]
        if DCS_Items[0] == 0:
            query_DCS = '''
                SELECT 
                    "B1_Z_BEDT_DACA_PV__Value", "B1_PT1281_DACA_PV__Value",
                    "B1_AT1011_DACA_PV__Value", "B1_AT1012_DACA_PV__Value",
                    "B1_TE1212_DACA_PV__Value", "B1_PT1061_DACA_PV__Value",
                    "B1_PT1071_DACA_PV__Value", "B1_PT1111_DACA_PV__Value",
                    "B1_PT1112_DACA_PV__Value", "B1_PT1211_DACA_PV__Value",
                    "B1_PT1212_DACA_PV__Value", "B1_TZ1131ZT_DACA_PV__Value",
                    "B1_S051AIT_DACA_PV__Value", "B1_AZ1011ZT_DACA_PV__Value",
                    "B1_S052AIT_DACA_PV__Value", "B1_S052AVFD_CRT_DACA_PV__Value",
                    "B1_S052AVFD_FB_DACA_PV__Value", "B1_PT1081_DACA_PV__Value",
                    "B1_PT1082_DACA_PV__Value", "B1_PT1091_DACA_PV__Value",
                    "B1_PT1092_DACA_PV__Value", "B1_TE1111_DACA_PV__Value",
                    "B1_TE1112_DACA_PV__Value" 
                FROM "DCS_Items" 
                ORDER BY "CronTime" DESC 
                LIMIT 1
                '''
            PG_cursor.execute(query_DCS)
            DCS = PG_cursor.fetchone()
            DCS = [float(value) for value in DCS]
            values = [crontime] + [float(x) for x in input[0]] + [float(x) for x in DCS] + [0]
        else:
            if cron_datetime.strftime("%H:%M:%S") in target_times or abs(DCS_Items[0] - HistoryParameter_CoalConsumption[11]) >= 3:
                values = [crontime] + [float(x) for x in input_coalconsumption[0]] + [OptimizerParameter_CoalConsumption]
            else:
                if OptimizerParameter_CoalConsumption > HistoryParameter_CoalConsumption[-1]:
                    input_coalconsumption = HistoryParameter_CoalConsumption[:-1]
                    OptimizerParameter_CoalConsumption = HistoryParameter_CoalConsumption[-1]
                    # print("input_coalconsumption:", input_coalconsumption)
                    # print("OptimizerParameter_CoalConsumption:", OptimizerParameter_CoalConsumption)
                    if isinstance(input_coalconsumption, float):
                        input_coalconsumption = [input_coalconsumption]
                    values = [crontime] + list(input_coalconsumption) + [OptimizerParameter_CoalConsumption]
                else:
                    values = [crontime] + [float(x) for x in input_coalconsumption[0]] + [OptimizerParameter_CoalConsumption]
        # print("DATA_CTCN:", DATA_CTCN)
        # print("DCS_Items:", DCS_Items)
        # print("HistoryParameter:", HistoryParameter)
        # print("OptimizerParameter_CoalConsumption:", OptimizerParameter_CoalConsumption)

        # Giai đoạn 6: Lưu thông số vào database
        # values = [
        #     crontime[0],
        #     row['LDA12080012000243'],
        #     row['LDA12080012000228'],
        #     row['LDA12080012000227'],
        #     row['LDA12080012000230'],
        #     row['LDA12080012000238'],
        #     row['LDA12080012000237'],
        #     row['LDA12080012000232'],
        #     row['LDA12080012000236'],
        #     row['LDA12080012000235'],
        #     row['LDA12080012000234'],
        #     row['LDA12080012000233'],
        #     row['B1_FT1151_DACA_PV__Value'],
        #     row['B1_TE1251_DACA_PV__Value'],
        #     row['B2_FT1151_DACA_PV__Value'],
        #     row['B1_Z_BEDT_DACA_PV__Value'],
        #     row['B1_PT1281_DACA_PV__Value'],
        #     row['B1_AT1011_DACA_PV__Value'],
        #     row['B1_AT1012_DACA_PV__Value'],
        #     row['B1_TE1212_DACA_PV__Value'],
        #     row['B1_PT1061_DACA_PV__Value'],
        #     row['B1_PT1071_DACA_PV__Value'],
        #     row['B1_PT1111_DACA_PV__Value'],
        #     row['B1_PT1112_DACA_PV__Value'],
        #     row['B1_PT1211_DACA_PV__Value'],
        #     row['B1_PT1212_DACA_PV__Value'],
        #     row['B1_TZ1131ZT_DACA_PV__Value'],
        #     row['B1_S051AIT_DACA_PV__Value'],
        #     row['B1_AZ1011ZT_DACA_PV__Value'],
        #     row['B1_S052AIT_DACA_PV__Value'],
        #     row['B1_S052AVFD_CRT_DACA_PV__Value'],
        #     row['B1_S052AVFD_FB_DACA_PV__Value'],
        #     row['B1_PT1081_DACA_PV__Value'],
        #     row['B1_PT1082_DACA_PV__Value'],
        #     row['B1_PT1091_DACA_PV__Value'],
        #     row['B1_PT1092_DACA_PV__Value'],
        #     row['B1_TE1111_DACA_PV__Value'],
        #     row['B1_TE1112_DACA_PV__Value'],
        #     row['B1_FT1151_DIVA_OUT__Value']
        # ]
        PG_cursor.execute('''SELECT * FROM "DATA_LH1_HistoryParameter" LIMIT 1''')
        name_columns = [desc[0] for desc in PG_cursor.description]
            # Tạo chuỗi cột và placeholders cho câu lệnh INSERT
        placeholders = ', '.join(['%s'] * len(name_columns))
        columns = ', '.join([f'"{col}"' for col in name_columns])
        insert_query = f'''
            INSERT INTO "DATA_LH1_HistoryParameter" ({columns}) VALUES ({placeholders})
            '''
        PG_cursor.execute(insert_query, values)
        PG_conn.commit() 
    except Exception as e:
        PG_conn.rollback()
        print(f"An error occurred: {e}")
        pass

def LH2_HistoryParameter(PG_cursor, PG_conn, model_LH2_HistoryParameter):
    """
    1. Workflow:
        Tìm kiếm bộ thông số Local dựa trên dữ liệu chất lượng than mới nhất hiện tại.
        - Giai đoạn 1: Lấy thời gian gần nhất từ bảng DCS_Items
        - Giai đoạn 2: Lấy dữ liệu vận hành gần nhất từ bảng DATA_CTCN
        - Giai đoạn 3: Tạo dữ liệu đầu vào
        - Giai đoạn 4: Tìm kiếm bộ thông số phù hợp với mức tải
        - Giai đoạn 5: Tra cứu nếu tiêu hao đó là thấp nhất trong ca thì lấy bộ thông số đó
        - Giai đoạn 6: Lưu thông số vào database
        
    2. Parameters:
        PG_cursor: Cursor để thực thi truy vấn SQL.
        PG_conn: Kết nối đến database PostgreSQL.
        model_LH2_HistoryParameter: Mô hình ML dự đoán tham số lịch sử.
        model_LH2_CoalConsumption: Mô hình ML dự đoán tiêu hao than.
    """
    try:
        print("Start LH2_HistoryParameter")
        query_crontime = '''
            SELECT "CronTime" FROM "DCS_Items" ORDER BY "CronTime" DESC LIMIT 1
            '''
        PG_cursor.execute(query_crontime)
        crontime = PG_cursor.fetchone()

        # Giai đoạn 1: Lấy thời gian gần nhất từ bảng DATA_CTCN
        query_DATA_CTCN = '''
            SELECT "LDA12080012000243", "LDA12080012000228", "LDA12080012000227", "LDA12080012000230",
            "LDA12080012000238", "LDA12080012000237", "LDA12080012000232", "LDA12080012000236",
            "LDA12080012000235", "LDA12080012000234", "LDA12080012000233" 
            FROM "DATA_CTCN" 
            ORDER BY "CronTime" DESC 
            LIMIT 1
            '''
        PG_cursor.execute(query_DATA_CTCN)
        DATA_CTCN = PG_cursor.fetchone()
        DATA_CTCN = [float(value) for value in DATA_CTCN]
        # print(DATA_CTCN)

        # Giai đoạn 2: Lấy dữ liệu vận hành gần nhất từ bảng DCS_Items
        query_DCS_Items = '''
            SELECT "B2_FT1151_DACA_PV__Value", "B2_TE1251_DACA_PV__Value", "B1_FT1151_DACA_PV__Value" 
            FROM "DCS_Items" 
            ORDER BY "CronTime" DESC 
            LIMIT 1
            '''
        PG_cursor.execute(query_DCS_Items)
        DCS_Items = PG_cursor.fetchone()
        DCS_Items = [float(value) for value in DCS_Items]

        # power = DCS_Items[0]
        # df_baseparameter = pd.read_csv('../baseparameters/baseparameter_LH2.csv')
        # print(df_baseparameter)
        # bins = df_baseparameter['power_bin'].unique()
        # # Tìm bin gần nhất với công suất hiện tại
        # nearest_bin = min(bins, key=lambda x: abs(x - power))
        # # Lấy bộ thông số tương ứng
        # row = df_baseparameter[df_baseparameter['power_bin'] == nearest_bin].iloc[0]
        # print("row:", row['LDA12080012000243'])

        # Giai đoạn 3: Tạo dữ liệu đầu vào
        input = DATA_CTCN + DCS_Items
        input = np.array(input).reshape(1, -1)
        HistoryParameter = model_LH2_HistoryParameter.predict(input)
        print(f"HistoryParameter : {HistoryParameter}")

        # Giai đoạn 4: Tìm kiếm bộ thông số phù hợp với mức tải
        hp_slice = np.array(HistoryParameter[0][:-1]).reshape(1, -1)
        input_coalconsumption = np.hstack((input, hp_slice))
        # input_coalconsumption = np.hstack((input, HistoryParameter))
        # OptimizerParameter_CoalConsumption = model_LH2_CoalConsumption.predict(input_coalconsumption)
        # OptimizerParameter_CoalConsumption = float(OptimizerParameter_CoalConsumption[0])
        if DCS_Items[0] == 0:
            OptimizerParameter_CoalConsumption = 0
        else:
            OptimizerParameter_CoalConsumption = HistoryParameter[0][-1]/DCS_Items[0]

        # Giai đoạn 5: Tra cứu nếu tiêu hao đó là thấp nhất trong ca thì lấy bộ thông số đó
        query_CoalConsumption = '''
            SELECT * 
            FROM "DATA_LH2_HistoryParameter" 
            ORDER BY "CronTime" DESC 
            LIMIT 1
            '''
        PG_cursor.execute(query_CoalConsumption)
        HistoryParameter_CoalConsumption = PG_cursor.fetchone()
        HistoryParameter_CoalConsumption = [float(value) for value in HistoryParameter_CoalConsumption[1:]]
        # print("HistoryParameter:", HistoryParameter[-1])
        # print("OptimizerParameter_CoalConsumption:", OptimizerParameter_CoalConsumption)
        target_times = ["06:00:00", "14:00:00", "22:00:00","06:01:00", "14:01:00", "22:01:00"]
        cron_datetime = crontime[0]
        if DCS_Items[0] == 0:
            query_DCS = '''
                SELECT 
                    "B2_Z_BEDT_DACA_PV__Value", "B2_PT1281_DACA_PV__Value",
                    "B2_AT1011_DACA_PV__Value", "B2_AT1012_DACA_PV__Value",
                    "B2_TE1212_DACA_PV__Value", "B2_PT1061_DACA_PV__Value",
                    "B2_PT1071_DACA_PV__Value", "B2_PT1111_DACA_PV__Value",
                    "B2_PT1112_DACA_PV__Value", "B2_PT1211_DACA_PV__Value",
                    "B2_PT1212_DACA_PV__Value", "B2_TZ1131ZT_DACA_PV__Value",
                    "B2_S051AIT_DACA_PV__Value", "B2_AZ1011ZT_DACA_PV__Value",
                    "B2_S052AIT_DACA_PV__Value", "B2_S052AVFD_CRT_DACA_PV__Value",
                    "B2_S052AVFD_FB_DACA_PV__Value", "B2_PT1081_DACA_PV__Value",
                    "B2_PT1082_DACA_PV__Value", "B2_PT1091_DACA_PV__Value",
                    "B2_PT1092_DACA_PV__Value", "B2_TE1111_DACA_PV__Value",
                    "B2_TE1112_DACA_PV__Value" 
                FROM "DCS_Items" 
                ORDER BY "CronTime" DESC 
                LIMIT 1
                '''
            PG_cursor.execute(query_DCS)
            DCS = PG_cursor.fetchone()
            DCS = [float(value) for value in DCS]
            values = [crontime] + [float(x) for x in input[0]] + [float(x) for x in DCS] + [0]
        else:
            if cron_datetime.strftime("%H:%M:%S") in target_times or abs(DCS_Items[0] - HistoryParameter_CoalConsumption[11]) >= 3:
                values = [crontime] + [float(x) for x in input_coalconsumption[0]] + [OptimizerParameter_CoalConsumption]
            else:
                if OptimizerParameter_CoalConsumption > HistoryParameter_CoalConsumption[-1]:
                    input_coalconsumption = HistoryParameter_CoalConsumption[:-1]
                    OptimizerParameter_CoalConsumption = HistoryParameter_CoalConsumption[-1]
                    # print("input_coalconsumption:", input_coalconsumption)
                    # print("OptimizerParameter_CoalConsumption:", OptimizerParameter_CoalConsumption)
                    if isinstance(input_coalconsumption, float):
                        input_coalconsumption = [input_coalconsumption]
                    values = [crontime] + list(input_coalconsumption) + [OptimizerParameter_CoalConsumption]
                else:
                    values = [crontime] + [float(x) for x in input_coalconsumption[0]] + [OptimizerParameter_CoalConsumption]
        # print("DATA_CTCN:", DATA_CTCN)
        # print("DCS_Items:", DCS_Items)
        # print("OptimizerParameter_CoalConsumption:", OptimizerParameter_CoalConsumption)

        # # Giai đoạn 6: Lưu thông số vào database
        # values = [
        #     crontime[0],
        #     row['LDA12080012000243'],
        #     row['LDA12080012000228'],
        #     row['LDA12080012000227'],
        #     row['LDA12080012000230'],
        #     row['LDA12080012000238'],
        #     row['LDA12080012000237'],
        #     row['LDA12080012000232'],
        #     row['LDA12080012000236'],
        #     row['LDA12080012000235'],
        #     row['LDA12080012000234'],
        #     row['LDA12080012000233'],
        #     row['B2_FT1151_DACA_PV__Value'],
        #     row['B2_TE1251_DACA_PV__Value'],
        #     row['B1_FT1151_DACA_PV__Value'],
        #     row['B2_Z_BEDT_DACA_PV__Value'],
        #     row['B2_PT1281_DACA_PV__Value'],
        #     row['B2_AT1011_DACA_PV__Value'],
        #     row['B2_AT1012_DACA_PV__Value'],
        #     row['B2_TE1212_DACA_PV__Value'],
        #     row['B2_PT1061_DACA_PV__Value'],
        #     row['B2_PT1071_DACA_PV__Value'],
        #     row['B2_PT1111_DACA_PV__Value'],
        #     row['B2_PT1112_DACA_PV__Value'],
        #     row['B2_PT1211_DACA_PV__Value'],
        #     row['B2_PT1212_DACA_PV__Value'],
        #     row['B2_TZ1131ZT_DACA_PV__Value'],
        #     row['B2_S051AIT_DACA_PV__Value'],
        #     row['B2_AZ1011ZT_DACA_PV__Value'],
        #     row['B2_S052AIT_DACA_PV__Value'],
        #     row['B2_S052AVFD_CRT_DACA_PV__Value'],
        #     row['B2_S052AVFD_FB_DACA_PV__Value'],
        #     row['B2_PT1081_DACA_PV__Value'],
        #     row['B2_PT1082_DACA_PV__Value'],
        #     row['B2_PT1091_DACA_PV__Value'],
        #     row['B2_PT1092_DACA_PV__Value'],
        #     row['B2_TE1111_DACA_PV__Value'],
        #     row['B2_TE1112_DACA_PV__Value'],
        #     row['B2_FT1151_DIVA_OUT__Value']
        # ]
        #     # Truy vấn bảng "DATA_LH2_HistoryParameter" để lấy tên cột
        PG_cursor.execute('SELECT * FROM "DATA_LH2_HistoryParameter" LIMIT 1')
        name_columns = [desc[0] for desc in PG_cursor.description]
            # Tạo chuỗi cột và placeholders cho câu lệnh INSERT
        placeholders = ', '.join(['%s'] * len(name_columns))
        columns = ', '.join([f'"{col}"' for col in name_columns])
        insert_query = f'''
            INSERT INTO "DATA_LH2_HistoryParameter" ({columns}) VALUES ({placeholders})
            '''
        PG_cursor.execute(insert_query, values)
        PG_conn.commit() 
    except Exception as e:
        PG_conn.rollback()
        print(f"An error occurred: {e}")
        pass