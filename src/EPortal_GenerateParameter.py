from datetime import datetime
import numpy as np

def LN_EPortal_GenerateParameter(input, PG_cursor, PG_conn, model_LN_EPortal, model_LN_EPortal_COconsumption, model_LN_EPortal_Nhietkhoithai):
    # try:
        crontime = datetime.now().strftime('%Y-%m-%d %H:%M:00')
        input_stage1 = [
            input.LDA07060012000157, 
            input.LDA07060012000158, 
            input.LDA07060012000166,
            input.LDA11070012000630, 
            input.CM_A181FT0001_DACA_PV__Value,
            input.CM_A181PT0013_DACA_PV__Value, 
            input.CM_A181_V19_COM_V19_IN_5_PV3__Value,
            input.CM_A181TE0023_DACA_PV__Value, 
            input.CM_A181FT0010_DACA_PV__Value,
            input.CM_A181AT0004_DACA_PV__Value, 
            input.CM_A181PDT0002_DACA_PV__Value,
            input.CM_A181PT0002_DACA_PV__Value, 
            input.CM_A181PT0003_DACA_PV__Value,
            input.CM_A181PT0004_DACA_PV__Value, 
            input.CM_A181PT0005_DACA_PV__Value,
            input.CM_A181PT0006_DACA_PV__Value, 
            input.CM_A181PT0007_DACA_PV__Value,
            input.CM_A181PT0008_DACA_PV__Value, 
            input.CM_A181_TIEUHAOCO_OUT__Value
        ]
        input_stage1 = np.array(input_stage1).reshape(1, -1)
        GenerateParameter_Stage1 = model_LN_EPortal.predict(input_stage1)
        print(GenerateParameter_Stage1)
        
        input_stage2 = np.hstack((input_stage1[0][:-1], GenerateParameter_Stage1[0])).reshape(1, -1)
        GenerateParameter_COconsumption = model_LN_EPortal_COconsumption.predict(input_stage2)
        print(GenerateParameter_COconsumption)

        input_stage3_DCS = [
            input.LDA07060012000157, 
            input.LDA07060012000158, 
            input.LDA07060012000166,
            input.LDA11070012000630, 
            input.CM_A181FT0001_DACA_PV__Value,
            input.CM_A181PT0013_DACA_PV__Value, 
            input.CM_A181_V19_COM_V19_IN_5_PV3__Value,
            input.CM_A181FT0010_DACA_PV__Value,
            input.CM_A181AT0004_DACA_PV__Value, 
            input.CM_A181PDT0002_DACA_PV__Value,
            input.CM_A181PT0002_DACA_PV__Value, 
            input.CM_A181PT0003_DACA_PV__Value,
            input.CM_A181PT0004_DACA_PV__Value, 
            input.CM_A181PT0005_DACA_PV__Value,
            input.CM_A181PT0006_DACA_PV__Value, 
            input.CM_A181PT0007_DACA_PV__Value,
            input.CM_A181PT0008_DACA_PV__Value
        ]
        input_stage3_DCS = np.array(input_stage3_DCS).reshape(1, -1)
        input_stage3_TSVH = GenerateParameter_Stage1[0]
        input_stage3 = np.hstack((input_stage3_DCS[0], input_stage3_TSVH, GenerateParameter_COconsumption)).reshape(1, -1)
        GenerateParameter_Nhietkhoithai = model_LN_EPortal_Nhietkhoithai.predict(input_stage3)
        
        # Truy vấn bảng "DATA_LN_EPortal_GenerateParameter" để lấy tên cột
        PG_cursor.execute('''
            SELECT * FROM "DATA_LN_EPortal_GenerateParameter" LIMIT 1
            ''')
        name_columns = [desc[0] for desc in PG_cursor.description]

        # Tạo chuỗi cột và placeholders cho câu lệnh INSERT
        placeholders = ', '.join(['%s'] * len(name_columns))
        columns = ', '.join([f'"{col}"' for col in name_columns])

        values = [crontime] + [float(x) for x in input_stage2[0]] + [float(GenerateParameter_COconsumption)] + [float(GenerateParameter_Nhietkhoithai)]
        print(values)
        
        insert_query = f'''
            INSERT INTO "DATA_LN_EPortal_GenerateParameter" ({columns}) VALUES ({placeholders})
            '''
        PG_cursor.execute(insert_query, values)
        PG_conn.commit() 

    # except Exception as e:
    #     PG_conn.rollback()
    #     print(f"An error occurred: {e}")
    #     pass