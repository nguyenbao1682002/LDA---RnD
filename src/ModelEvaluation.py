import numpy as np
import pandas as pd
from datetime import datetime

def LH1_Evaluation(PG_cursor, PG_conn):
    try:
        columns_DCS_Items = ["CronTime","B1_Z_BEDT_DACA_PV__Value", "B1_PT1281_DACA_PV__Value","B1_AT1011_DACA_PV__Value", 
            "B1_AT1012_DACA_PV__Value","B1_TE1212_DACA_PV__Value", "B1_PT1061_DACA_PV__Value","B1_PT1071_DACA_PV__Value", 
            "B1_PT1111_DACA_PV__Value","B1_PT1112_DACA_PV__Value", "B1_PT1211_DACA_PV__Value","B1_PT1212_DACA_PV__Value", 
            "B1_TZ1131ZT_DACA_PV__Value","B1_S051AIT_DACA_PV__Value", "B1_AZ1011ZT_DACA_PV__Value","B1_S052AIT_DACA_PV__Value", 
            "B1_S052AVFD_CRT_DACA_PV__Value","B1_S052AVFD_FB_DACA_PV__Value", "B1_PT1081_DACA_PV__Value","B1_PT1082_DACA_PV__Value", 
            "B1_PT1091_DACA_PV__Value","B1_PT1092_DACA_PV__Value", "B1_TE1111_DACA_PV__Value","B1_TE1112_DACA_PV__Value", 
            "B1_FT1151_DIVA_OUT__Value"]
        columns_DATA_LH1_OptimizerParameter = ["CronTime","B1_Z_BEDT_DACA_PV__Value_OP", "B1_PT1281_DACA_PV__Value_OP","B1_AT1011_DACA_PV__Value_OP", 
            "B1_AT1012_DACA_PV__Value_OP","B1_TE1212_DACA_PV__Value_OP", "B1_PT1061_DACA_PV__Value_OP","B1_PT1071_DACA_PV__Value_OP", 
            "B1_PT1111_DACA_PV__Value_OP","B1_PT1112_DACA_PV__Value_OP", "B1_PT1211_DACA_PV__Value_OP","B1_PT1212_DACA_PV__Value_OP", 
            "B1_TZ1131ZT_DACA_PV__Value_OP","B1_S051AIT_DACA_PV__Value_OP", "B1_AZ1011ZT_DACA_PV__Value_OP","B1_S052AIT_DACA_PV__Value_OP", 
            "B1_S052AVFD_CRT_DACA_PV__Value_OP","B1_S052AVFD_FB_DACA_PV__Value_OP", "B1_PT1081_DACA_PV__Value_OP","B1_PT1082_DACA_PV__Value_OP", 
            "B1_PT1091_DACA_PV__Value_OP","B1_PT1092_DACA_PV__Value_OP", "B1_TE1111_DACA_PV__Value_OP","B1_TE1112_DACA_PV__Value_OP", 
            "B1_FT1151_DIVA_OUT__Value_OP"]

        query_DCS_Items = '''SELECT "CronTime","B1_Z_BEDT_DACA_PV__Value", "B1_PT1281_DACA_PV__Value","B1_AT1011_DACA_PV__Value", 
            "B1_AT1012_DACA_PV__Value","B1_TE1212_DACA_PV__Value", "B1_PT1061_DACA_PV__Value","B1_PT1071_DACA_PV__Value", 
            "B1_PT1111_DACA_PV__Value","B1_PT1112_DACA_PV__Value", "B1_PT1211_DACA_PV__Value","B1_PT1212_DACA_PV__Value", 
            "B1_TZ1131ZT_DACA_PV__Value","B1_S051AIT_DACA_PV__Value", "B1_AZ1011ZT_DACA_PV__Value","B1_S052AIT_DACA_PV__Value", 
            "B1_S052AVFD_CRT_DACA_PV__Value","B1_S052AVFD_FB_DACA_PV__Value", "B1_PT1081_DACA_PV__Value","B1_PT1082_DACA_PV__Value", 
            "B1_PT1091_DACA_PV__Value","B1_PT1092_DACA_PV__Value", "B1_TE1111_DACA_PV__Value","B1_TE1112_DACA_PV__Value", 
            "B1_FT1151_DIVA_OUT__Value" FROM "DCS_Items" ORDER BY "CronTime" DESC LIMIT 1000'''
        PG_cursor.execute(query_DCS_Items)
        DCS_Items = PG_cursor.fetchall()
        df_DCS_Items = pd.DataFrame(DCS_Items, columns=columns_DCS_Items)
        # print("DCS_Items:", df_DCS_Items)

        query_DATA_LH1_OptimizerParameter = '''SELECT "CronTime","B1_Z_BEDT_DACA_PV__Value", "B1_PT1281_DACA_PV__Value","B1_AT1011_DACA_PV__Value", 
            "B1_AT1012_DACA_PV__Value","B1_TE1212_DACA_PV__Value", "B1_PT1061_DACA_PV__Value","B1_PT1071_DACA_PV__Value", 
            "B1_PT1111_DACA_PV__Value","B1_PT1112_DACA_PV__Value", "B1_PT1211_DACA_PV__Value","B1_PT1212_DACA_PV__Value", 
            "B1_TZ1131ZT_DACA_PV__Value","B1_S051AIT_DACA_PV__Value", "B1_AZ1011ZT_DACA_PV__Value","B1_S052AIT_DACA_PV__Value", 
            "B1_S052AVFD_CRT_DACA_PV__Value","B1_S052AVFD_FB_DACA_PV__Value", "B1_PT1081_DACA_PV__Value","B1_PT1082_DACA_PV__Value", 
            "B1_PT1091_DACA_PV__Value","B1_PT1092_DACA_PV__Value", "B1_TE1111_DACA_PV__Value","B1_TE1112_DACA_PV__Value", 
            "B1_FT1151_DIVA_OUT__Value" FROM "DATA_LH1_OptimizerParameter" ORDER BY "CronTime" DESC LIMIT 1000'''
        PG_cursor.execute(query_DATA_LH1_OptimizerParameter)
        DATA_LH1_OptimizerParameter = PG_cursor.fetchall()
        df_DATA_LH1_OptimizerParameter = pd.DataFrame(DATA_LH1_OptimizerParameter, columns=columns_DATA_LH1_OptimizerParameter)
        # print("DATA_LH1_OptimizerParameter:", df_DATA_LH1_OptimizerParameter)

        df_LH1_Evaluation = pd.merge(df_DCS_Items,df_DATA_LH1_OptimizerParameter, on="CronTime")
        df_LH1_Evaluation = df_LH1_Evaluation.dropna()
        # print("df_LH1_Evaluation:", df_LH1_Evaluation)

        crontime = datetime.now().strftime('%Y-%m-%d %H:%M:00')
        values_MAPE = [crontime]
        epsilon = 1e-10
        for col in columns_DCS_Items[1:]:
            y_true = df_LH1_Evaluation[col].values
            y_pred = df_LH1_Evaluation[col+'_OP'].values
            mape = np.mean(np.abs((y_true - y_pred) / (y_true + epsilon))) * 100
            values_MAPE.append(mape)
        #     print(f"Metrics for {col}:")
        #     print(f"MAPE: {mape:.2f}%\n")
        # print(f"values_MAPE: {values_MAPE}")

        # Tạo chuỗi cột và placeholders cho câu lệnh INSERT
        PG_cursor.execute('SELECT * FROM "DATA_LH1_ModelEvaluation" LIMIT 1')
        name_columns = [desc[0] for desc in PG_cursor.description]
        placeholders = ', '.join(['%s'] * len(name_columns))
        columns = ', '.join([f'"{col}"' for col in name_columns])
        
        insert_query = f'''
        INSERT INTO "DATA_LH1_ModelEvaluation" ({columns}) VALUES ({placeholders})
        '''
        PG_cursor.execute(insert_query, values_MAPE)
        PG_conn.commit() 
    except Exception as e:
        PG_conn.rollback()
        print(f"An error occurred: {e}")
        pass

def LH2_Evaluation(PG_cursor, PG_conn):
    try:
        columns_DCS_Items = ["CronTime","B2_Z_BEDT_DACA_PV__Value", "B2_PT1281_DACA_PV__Value","B2_AT1011_DACA_PV__Value", 
            "B2_AT1012_DACA_PV__Value","B2_TE1212_DACA_PV__Value", "B2_PT1061_DACA_PV__Value","B2_PT1071_DACA_PV__Value", 
            "B2_PT1111_DACA_PV__Value","B2_PT1112_DACA_PV__Value", "B2_PT1211_DACA_PV__Value","B2_PT1212_DACA_PV__Value", 
            "B2_TZ1131ZT_DACA_PV__Value","B2_S051AIT_DACA_PV__Value", "B2_AZ1011ZT_DACA_PV__Value","B2_S052AIT_DACA_PV__Value", 
            "B2_S052AVFD_CRT_DACA_PV__Value","B2_S052AVFD_FB_DACA_PV__Value", "B2_PT1081_DACA_PV__Value","B2_PT1082_DACA_PV__Value", 
            "B2_PT1091_DACA_PV__Value","B2_PT1092_DACA_PV__Value", "B2_TE1111_DACA_PV__Value","B2_TE1112_DACA_PV__Value", 
            "B2_FT1151_DIVA_OUT__Value"]
        columns_DATA_LH2_OptimizerParameter = ["CronTime","B2_Z_BEDT_DACA_PV__Value_OP", "B2_PT1281_DACA_PV__Value_OP","B2_AT1011_DACA_PV__Value_OP", 
            "B2_AT1012_DACA_PV__Value_OP","B2_TE1212_DACA_PV__Value_OP", "B2_PT1061_DACA_PV__Value_OP","B2_PT1071_DACA_PV__Value_OP", 
            "B2_PT1111_DACA_PV__Value_OP","B2_PT1112_DACA_PV__Value_OP", "B2_PT1211_DACA_PV__Value_OP","B2_PT1212_DACA_PV__Value_OP", 
            "B2_TZ1131ZT_DACA_PV__Value_OP","B2_S051AIT_DACA_PV__Value_OP", "B2_AZ1011ZT_DACA_PV__Value_OP","B2_S052AIT_DACA_PV__Value_OP", 
            "B2_S052AVFD_CRT_DACA_PV__Value_OP","B2_S052AVFD_FB_DACA_PV__Value_OP", "B2_PT1081_DACA_PV__Value_OP","B2_PT1082_DACA_PV__Value_OP", 
            "B2_PT1091_DACA_PV__Value_OP","B2_PT1092_DACA_PV__Value_OP", "B2_TE1111_DACA_PV__Value_OP","B2_TE1112_DACA_PV__Value_OP", 
            "B2_FT1151_DIVA_OUT__Value_OP"]

        query_DCS_Items = '''SELECT "CronTime","B2_Z_BEDT_DACA_PV__Value", "B2_PT1281_DACA_PV__Value","B2_AT1011_DACA_PV__Value", 
            "B2_AT1012_DACA_PV__Value","B2_TE1212_DACA_PV__Value", "B2_PT1061_DACA_PV__Value","B2_PT1071_DACA_PV__Value", 
            "B2_PT1111_DACA_PV__Value","B2_PT1112_DACA_PV__Value", "B2_PT1211_DACA_PV__Value","B2_PT1212_DACA_PV__Value", 
            "B2_TZ1131ZT_DACA_PV__Value","B2_S051AIT_DACA_PV__Value", "B2_AZ1011ZT_DACA_PV__Value","B2_S052AIT_DACA_PV__Value", 
            "B2_S052AVFD_CRT_DACA_PV__Value","B2_S052AVFD_FB_DACA_PV__Value", "B2_PT1081_DACA_PV__Value","B2_PT1082_DACA_PV__Value", 
            "B2_PT1091_DACA_PV__Value","B2_PT1092_DACA_PV__Value", "B2_TE1111_DACA_PV__Value","B2_TE1112_DACA_PV__Value", 
            "B2_FT1151_DIVA_OUT__Value" FROM "DCS_Items" ORDER BY "CronTime" DESC LIMIT 1000'''
        PG_cursor.execute(query_DCS_Items)
        DCS_Items = PG_cursor.fetchall()
        df_DCS_Items = pd.DataFrame(DCS_Items, columns=columns_DCS_Items)
        # print("DCS_Items:", df_DCS_Items)

        query_DATA_LH2_OptimizerParameter = '''SELECT "CronTime","B2_Z_BEDT_DACA_PV__Value", "B2_PT1281_DACA_PV__Value","B2_AT1011_DACA_PV__Value", 
            "B2_AT1012_DACA_PV__Value","B2_TE1212_DACA_PV__Value", "B2_PT1061_DACA_PV__Value","B2_PT1071_DACA_PV__Value", 
            "B2_PT1111_DACA_PV__Value","B2_PT1112_DACA_PV__Value", "B2_PT1211_DACA_PV__Value","B2_PT1212_DACA_PV__Value", 
            "B2_TZ1131ZT_DACA_PV__Value","B2_S051AIT_DACA_PV__Value", "B2_AZ1011ZT_DACA_PV__Value","B2_S052AIT_DACA_PV__Value", 
            "B2_S052AVFD_CRT_DACA_PV__Value","B2_S052AVFD_FB_DACA_PV__Value", "B2_PT1081_DACA_PV__Value","B2_PT1082_DACA_PV__Value", 
            "B2_PT1091_DACA_PV__Value","B2_PT1092_DACA_PV__Value", "B2_TE1111_DACA_PV__Value","B2_TE1112_DACA_PV__Value", 
            "B2_FT1151_DIVA_OUT__Value" FROM "DATA_LH2_OptimizerParameter" ORDER BY "CronTime" DESC LIMIT 1000'''
        PG_cursor.execute(query_DATA_LH2_OptimizerParameter)
        DATA_LH2_OptimizerParameter = PG_cursor.fetchall()
        df_DATA_LH2_OptimizerParameter = pd.DataFrame(DATA_LH2_OptimizerParameter, columns=columns_DATA_LH2_OptimizerParameter)
        # print("DATA_LH2_OptimizerParameter:", df_DATA_LH2_OptimizerParameter)

        df_LH2_Evaluation = pd.merge(df_DCS_Items,df_DATA_LH2_OptimizerParameter, on="CronTime")
        df_LH2_Evaluation = df_LH2_Evaluation.dropna()
        # print("df_LH2_Evaluation:", df_LH2_Evaluation)

        crontime = datetime.now().strftime('%Y-%m-%d %H:%M:00')
        values_MAPE = [crontime]
        epsilon = 1e-10 
        for col in columns_DCS_Items[1:]:
            y_true = df_LH2_Evaluation[col].values
            y_pred = df_LH2_Evaluation[col+'_OP'].values
            mape = np.mean(np.abs((y_true - y_pred) / (y_true + epsilon))) * 100
            values_MAPE.append(mape)
        #     print(f"Metrics for {col}:")
        #     print(f"MAPE: {mape:.2f}%\n")
        # print(f"values_MAPE: {values_MAPE}")

        # Tạo chuỗi cột và placeholders cho câu lệnh INSERT
        PG_cursor.execute('SELECT * FROM "DATA_LH2_ModelEvaluation" LIMIT 1')
        name_columns = [desc[0] for desc in PG_cursor.description]
        placeholders = ', '.join(['%s'] * len(name_columns))
        columns = ', '.join([f'"{col}"' for col in name_columns])
        
        insert_query = f'''
        INSERT INTO "DATA_LH2_ModelEvaluation" ({columns}) VALUES ({placeholders})
        '''
        PG_cursor.execute(insert_query, values_MAPE)
        PG_conn.commit() 
    except Exception as e:
        PG_conn.rollback()
        print(f"An error occurred: {e}")
        pass

def LN_Evaluation(PG_cursor, PG_conn):
    try:
        columns_DCS_Items = ["CronTime","CM_A181_V19_COM_V19_IN_5_PV3__Value", "CM_A181FT0010_DACA_PV__Value", "CM_A181FT0001_DACA_PV__Value",
                            "CM_A181TE0007_DACA_PV__Value", "CM_A181S015BPGPV_DACA_PV__Value", "CM_A181AT0001_DACA_PV__Value", "CM_A181PT0002_DACA_PV__Value",
                            "CM_A181PT0003_DACA_PV__Value","CM_A181PT0004_DACA_PV__Value", "CM_A181PDT0002_DACA_PV__Value", "CM_A181PT0005_DACA_PV__Value", 
                            "CM_A181PT0006_DACA_PV__Value", "CM_A181PT0007_DACA_PV__Value","CM_A181PT0008_DACA_PV__Value", "CM_A181_TIEUHAOCO_OUT__Value"]
        columns_DATA_LN_OptimizerParameter = ["CronTime","CM_A181_V19_COM_V19_IN_5_PV3__Value_OP", "CM_A181FT0010_DACA_PV__Value_OP", "CM_A181FT0001_DACA_PV__Value_OP",
                            "CM_A181TE0007_DACA_PV__Value_OP", "CM_A181S015BPGPV_DACA_PV__Value_OP", "CM_A181AT0001_DACA_PV__Value_OP", "CM_A181PT0002_DACA_PV__Value_OP",
                            "CM_A181PT0003_DACA_PV__Value_OP","CM_A181PT0004_DACA_PV__Value_OP", "CM_A181PDT0002_DACA_PV__Value_OP", "CM_A181PT0005_DACA_PV__Value_OP", 
                            "CM_A181PT0006_DACA_PV__Value_OP", "CM_A181PT0007_DACA_PV__Value_OP","CM_A181PT0008_DACA_PV__Value_OP", "CM_A181_TIEUHAOCO_OUT__Value_OP"]

        query_DCS_Items = '''SELECT "CronTime","CM_A181_V19_COM_V19_IN_5_PV3__Value", "CM_A181FT0010_DACA_PV__Value", "CM_A181FT0001_DACA_PV__Value",
                            "CM_A181TE0007_DACA_PV__Value", "CM_A181S015BPGPV_DACA_PV__Value", "CM_A181AT0001_DACA_PV__Value", "CM_A181PT0002_DACA_PV__Value",
                            "CM_A181PT0003_DACA_PV__Value","CM_A181PT0004_DACA_PV__Value", "CM_A181PDT0002_DACA_PV__Value", "CM_A181PT0005_DACA_PV__Value", 
                            "CM_A181PT0006_DACA_PV__Value", "CM_A181PT0007_DACA_PV__Value","CM_A181PT0008_DACA_PV__Value", "CM_A181_TIEUHAOCO_OUT__Value" FROM "DCS_Items" ORDER BY "CronTime" DESC LIMIT 1000'''
        PG_cursor.execute(query_DCS_Items)
        DCS_Items = PG_cursor.fetchall()
        df_DCS_Items = pd.DataFrame(DCS_Items, columns=columns_DCS_Items)
        # print("DCS_Items:", df_DCS_Items)

        query_DATA_LN_OptimizerParameter = '''SELECT "CronTime","CM_A181_V19_COM_V19_IN_5_PV3__Value", "CM_A181FT0010_DACA_PV__Value", "CM_A181FT0001_DACA_PV__Value",
                                "CM_A181TE0007_DACA_PV__Value", "CM_A181S015BPGPV_DACA_PV__Value", "CM_A181AT0001_DACA_PV__Value", "CM_A181PT0002_DACA_PV__Value",
                                "CM_A181PT0003_DACA_PV__Value","CM_A181PT0004_DACA_PV__Value", "CM_A181PDT0002_DACA_PV__Value", "CM_A181PT0005_DACA_PV__Value",
                                "CM_A181PT0006_DACA_PV__Value", "CM_A181PT0007_DACA_PV__Value","CM_A181PT0008_DACA_PV__Value", "CM_A181_TIEUHAOCO_OUT__Value" FROM "DATA_LN_OptimizerParameter" ORDER BY "CronTime" DESC LIMIT 1000'''
        PG_cursor.execute(query_DATA_LN_OptimizerParameter)
        DATA_LN_OptimizerParameter = PG_cursor.fetchall()
        df_DATA_LN_OptimizerParameter = pd.DataFrame(DATA_LN_OptimizerParameter, columns=columns_DATA_LN_OptimizerParameter)
        # print("DATA_LN_OptimizerParameter:", df_DATA_LN_OptimizerParameter)

        df_LN_Evaluation = pd.merge(df_DCS_Items,df_DATA_LN_OptimizerParameter, on="CronTime")
        df_LN_Evaluation = df_LN_Evaluation.dropna()
        # print("df_LN_Evaluation:", df_LN_Evaluation)

        crontime = datetime.now().strftime('%Y-%m-%d %H:%M:00')
        values_MAPE = [crontime]
        epsilon = 1e-10
        for col in columns_DCS_Items[1:]:
            y_true = df_LN_Evaluation[col].values
            y_pred = df_LN_Evaluation[col+'_OP'].values
            mape = np.mean(np.abs((y_true - y_pred) / (y_true + epsilon))) * 100
            values_MAPE.append(mape)
        #     print(f"Metrics for {col}:")
        #     print(f"MAPE: {mape:.2f}%\n")
        # print(f"values_MAPE: {values_MAPE}")

        # Tạo chuỗi cột và placeholders cho câu lệnh INSERT
        PG_cursor.execute('SELECT * FROM "DATA_LN_ModelEvaluation" LIMIT 1')
        name_columns = [desc[0] for desc in PG_cursor.description]
        placeholders = ', '.join(['%s'] * len(name_columns))
        columns = ', '.join([f'"{col}"' for col in name_columns])
        
        insert_query = f'''
        INSERT INTO "DATA_LN_ModelEvaluation" ({columns}) VALUES ({placeholders})
        '''
        PG_cursor.execute(insert_query, values_MAPE)
        PG_conn.commit() 
    except Exception as e:
        PG_conn.rollback()
        print(f"An error occurred: {e}")
        pass