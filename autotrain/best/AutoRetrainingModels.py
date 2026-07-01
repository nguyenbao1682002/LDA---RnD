import numpy as np
import pickle
import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import ExtraTreesRegressor

def LH1_AutoRetrainingModel(PG_cursor):
    try:
        path_data = "D:/001.Project/LDA_master/data/DATA_LH1.csv"
        get_DATA_LH1(PG_cursor, path_data)
        LH1_TrainModel(path_data)
    except Exception as e:
        print(f"An error occurred: {e}")
        pass

def get_DATA_LH1(PG_cursor, path_data):
    """
        Export dữ liệu từ DB về local
        1. Workflow:
            - Giai đoạn 1: Query data DATA_CTCN
            - Giai đoạn 2: Query data LH1_DCS_Items
            - Giai đoạn 3: Ghép DATA_CTCN và DCS_Items để tạo data DATA_LH.csv
        
        2. Parameters:
            PG_cursor: Cursor để thực thi truy vấn SQL.
            PG_conn: Kết nối đến database PostgreSQL.
    """
    try:
        # Giai đoạn 1: Query data DATA_CTCN
        columns_DATA_CTCN = [
            "CronTime", "LDA12080012000243", "LDA12080012000228", "LDA12080012000227", 
            "LDA12080012000230", "LDA12080012000238", "LDA12080012000237", 
            "LDA12080012000232", "LDA12080012000236", "LDA12080012000235", 
            "LDA12080012000234", "LDA12080012000233"]
        query_DATA_CTCN = '''
            SELECT "CronTime", "LDA12080012000243", "LDA12080012000228", "LDA12080012000227", 
            "LDA12080012000230", "LDA12080012000238", "LDA12080012000237", 
            "LDA12080012000232", "LDA12080012000236", "LDA12080012000235", 
            "LDA12080012000234", "LDA12080012000233" FROM "DATA_CTCN" ORDER BY "CronTime" DESC'''
        PG_cursor.execute(query_DATA_CTCN)
        DATA_CTCN = PG_cursor.fetchall()
        DATA_CTCN = pd.DataFrame(DATA_CTCN, columns=columns_DATA_CTCN)

        # Giai đoạn 2: Query data LH1_DCS_Items
        columns_DCS_Items = [
            "CronTime", "FT1151_DACA_PV__Value", "TE1251_DACA_PV__Value",
            "FT1151_DACA_PV__Value_Other", "Z_BEDT_DACA_PV__Value", "PT1281_DACA_PV__Value",
            "AT1011_DACA_PV__Value", "AT1012_DACA_PV__Value", "TE1212_DACA_PV__Value",
            "PT1061_DACA_PV__Value", "PT1071_DACA_PV__Value", "PT1111_DACA_PV__Value",
            "PT1112_DACA_PV__Value", "PT1211_DACA_PV__Value", "PT1212_DACA_PV__Value",
            "TZ1131ZT_DACA_PV__Value", "S051AIT_DACA_PV__Value", "AZ1011ZT_DACA_PV__Value",
            "S052AIT_DACA_PV__Value", "S052AVFD_CRT_DACA_PV__Value", "S052AVFD_FB_DACA_PV__Value",
            "PT1081_DACA_PV__Value", "PT1082_DACA_PV__Value", "PT1091_DACA_PV__Value",
            "PT1092_DACA_PV__Value", "TE1111_DACA_PV__Value", "TE1112_DACA_PV__Value",
            "FT1151_DIVA_OUT__Value"]
        
        query_LH1_DCS_Items = '''
            SELECT "CronTime", "B1_FT1151_DACA_PV__Value", "B1_TE1251_DACA_PV__Value",
            "B2_FT1151_DACA_PV__Value", "B1_Z_BEDT_DACA_PV__Value", "B1_PT1281_DACA_PV__Value",
            "B1_AT1011_DACA_PV__Value", "B1_AT1012_DACA_PV__Value", "B1_TE1212_DACA_PV__Value",
            "B1_PT1061_DACA_PV__Value", "B1_PT1071_DACA_PV__Value", "B1_PT1111_DACA_PV__Value",
            "B1_PT1112_DACA_PV__Value", "B1_PT1211_DACA_PV__Value", "B1_PT1212_DACA_PV__Value",
            "B1_TZ1131ZT_DACA_PV__Value", "B1_S051AIT_DACA_PV__Value", "B1_AZ1011ZT_DACA_PV__Value",
            "B1_S052AIT_DACA_PV__Value", "B1_S052AVFD_CRT_DACA_PV__Value", "B1_S052AVFD_FB_DACA_PV__Value",
            "B1_PT1081_DACA_PV__Value", "B1_PT1082_DACA_PV__Value", "B1_PT1091_DACA_PV__Value",
            "B1_PT1092_DACA_PV__Value", "B1_TE1111_DACA_PV__Value", "B1_TE1112_DACA_PV__Value",
            "B1_FT1151_DIVA_OUT__Value" FROM "DCS_Items" ORDER BY "CronTime" DESC
            '''
        PG_cursor.execute(query_LH1_DCS_Items)
        LH1_DCS_Items = PG_cursor.fetchall()
        LH1_DCS_Items = pd.DataFrame(LH1_DCS_Items , columns=columns_DCS_Items)

        # Giai đoạn 4: Tạo data DATA_LH.csv
        DATA_CTCN['CronTime'] = pd.to_datetime(DATA_CTCN['CronTime'])
        LH1_DCS_Items['CronTime'] = pd.to_datetime(LH1_DCS_Items['CronTime'])
        DATA_CTCN = DATA_CTCN.set_index('CronTime')
        DATA_CTCN = DATA_CTCN.resample('min').mean()
        DATA_CTCN = DATA_CTCN.interpolate(method='linear')
        df_LH1 = pd.merge(DATA_CTCN, LH1_DCS_Items, on="CronTime")
        df_LH1.to_csv(path_data, index=False)
    except Exception as e:
        print(f"An error occurred: {e}")
        pass

def LH1_TrainModel(path_data):
    """
        Huấn luyện mô hình dự đoán dựa trên dữ liệu từ file CSV
        1. Workflow:
            - Giai đoạn 1: Đọc và tiền xử lý dữ liệu từ file CSV
            - Giai đoạn 2: Lọc và dịch chuyển dữ liệu theo thời gian
            - Giai đoạn 3: Chia dữ liệu thành tập huấn luyện và kiểm tra
            - Giai đoạn 4: Huấn luyện mô hình và đánh giá hiệu suất
            - Giai đoạn 5: Lưu mô hình tốt nhất nếu vượt trội
            
        2. Parameters:
            path_data: Đường dẫn đến file CSV chứa dữ liệu đầu vào
    """
    try:
        # Khởi tạo ngày bắt đầu để lọc dữ liệu
        start_date = datetime(2024, 11, 1)
        
        # Đọc dữ liệu từ file CSV vào DataFrame
        df_LH = pd.read_csv(path_data)
        
        # Chuyển cột CronTime sang định dạng datetime để xử lý thời gian
        df_LH['CronTime'] = pd.to_datetime(df_LH['CronTime'])
        
        # Lọc dữ liệu từ ngày start_date trở đi
        df_LH = df_LH[df_LH['CronTime'] >= start_date]
        
        # Loại bỏ các giá trị bất thường (999999) trong cột FT1151_DIVA_OUT__Value
        df_LH = df_LH[df_LH["FT1151_DIVA_OUT__Value"] != 999999.000000]

        # Dịch chuyển dữ liệu của các cột được liệt kê lên 8*60*2 dòng (tương ứng với khoảng thời gian)
        for col in [
            'LDA12080012000243', 'LDA12080012000228', 'LDA12080012000227',
            'LDA12080012000230', 'LDA12080012000238', 'LDA12080012000237',
            'LDA12080012000232', 'LDA12080012000236', 'LDA12080012000235',
            'LDA12080012000234', 'LDA12080012000233']:
            df_LH[f"{col}"] = df_LH[col].shift(-8*60*2)
        
        # Loại bỏ các hàng chứa giá trị NaN sau khi dịch chuyển
        df_LH = df_LH.dropna()
        
        # Lọc dữ liệu dựa trên ngưỡng của cột FT1151_DIVA_OUT__Value (0.12 đến 0.16)
        df_LH = df_LH[(df_LH['FT1151_DIVA_OUT__Value'] <= 0.16) & (df_LH['FT1151_DIVA_OUT__Value'] >= 0.12)]

        # Chuyển index thành kiểu datetime nếu chưa
        df_LH.index = pd.to_datetime(df_LH.index)

        # Hàm gán khoảng thời gian (shift)
        def assign_shift(time):
            if "06:00" <= time < "14:00":
                return "06-14"
            elif "14:00" <= time < "22:00":
                return "14-22"
            else:
                return "22-06"

        # Tách ngày và ca làm hai cột
        df_LH["date"] = df_LH.index.date
        df_LH["shift"] = df_LH.index.strftime("%H:%M").map(assign_shift)

        # Trường hợp ca 22-06 thuộc ngày hôm sau nên cần điều chỉnh
        df_LH.loc[df_LH["shift"] == "22-06", "date"] = df_LH.loc[df_LH["shift"] == "22-06", "date"] + pd.to_timedelta(1, unit='D')

        # Gom nhóm theo ngày và ca, tính trung bình
        df_LH = df_LH.groupby(["date", "shift"]).mean()

        # Chuẩn bị dữ liệu đầu vào (X) và đầu ra (y) cho mô hình
        # CoalConsumption:
        X = df_LH[[
            "LDA12080012000243", "LDA12080012000228",
            "LDA12080012000227", "LDA12080012000230", "LDA12080012000238",
            "LDA12080012000237", "LDA12080012000232", "LDA12080012000236",
            "LDA12080012000235", "LDA12080012000234", "LDA12080012000233",
            "FT1151_DACA_PV__Value", "TE1251_DACA_PV__Value", "FT1151_DACA_PV__Value_Other",]]
        y = df_LH[[
            "Z_BEDT_DACA_PV__Value", "PT1281_DACA_PV__Value", "AT1011_DACA_PV__Value", 
            "AT1012_DACA_PV__Value", "TE1212_DACA_PV__Value", "PT1061_DACA_PV__Value",
            "PT1071_DACA_PV__Value", "PT1111_DACA_PV__Value", "PT1112_DACA_PV__Value", 
            "PT1211_DACA_PV__Value", "PT1212_DACA_PV__Value", "TZ1131ZT_DACA_PV__Value",
            "S051AIT_DACA_PV__Value", "AZ1011ZT_DACA_PV__Value", "S052AIT_DACA_PV__Value", 
            "S052AVFD_CRT_DACA_PV__Value", "S052AVFD_FB_DACA_PV__Value", "PT1081_DACA_PV__Value",
            "PT1082_DACA_PV__Value", "PT1091_DACA_PV__Value", "PT1092_DACA_PV__Value", 
            "TE1111_DACA_PV__Value", "TE1112_DACA_PV__Value"]]
        
        # Chia dữ liệu thành tập huấn luyện và tập kiểm tra (80% train, 20% test)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

        # Huấn luyện mô hình MultiOutputRegressor với ExtraTreesRegressor
        model = MultiOutputRegressor(
            ExtraTreesRegressor(n_estimators=50, max_depth=10, n_jobs=2, random_state=42))
        model.fit(X_train, y_train)
        
        # Dự đoán trên tập kiểm tra
        y_pred = model.predict(X_test)

        # Đánh giá hiệu suất mô hình cho từng đầu ra
        rmse_list, r2_list = [],[]
        for i in range(y_test.shape[1]):
            mse = mean_squared_error(y_test.iloc[:, i], y_pred[:, i])  # Tính MSE
            rmse = np.sqrt(mse)  # Tính RMSE từ MSE
            r2 = r2_score(y_test.iloc[:, i], y_pred[:, i])  # Tính R-squared
            rmse_list.append(rmse)
            r2_list.append(r2)

        # Tính giá trị trung bình của RMSE và R-squared
        rmse = np.mean(rmse_list)
        r2 = np.mean(r2_list)
        
        # Lấy thời gian hiện tại để ghi vào kết quả
        current = datetime.now().strftime("%Y%m%d")
        
        # Chuẩn bị chuỗi kết quả đánh giá
        results = f"RMSE: {rmse}\nR-squared: {r2}\nList Root Mean Squared Error: {rmse_list}\nList R2: {r2_list}\nDatetime: {current}"
        
        # Đường dẫn lưu mô hình tốt nhất và file đánh giá
        path_best_model = f'D:/001.Project/LDA_master/autotrain/best/LH1_Parameter_best.sav'
        path_best_evaluation = f'D:/001.Project/LDA_master/autotrain/best/LH1_Parameter_best.txt'
        
        # Đọc file đánh giá hiện tại để lấy RMSE và R-squared tốt nhất
        with open(path_best_evaluation, "r") as file:
            lines = file.readlines()
        for line in lines:
            if "RMSE" in line:
                rmse_best = float(line.split(":")[1].strip())
            elif "R-squared" in line:
                r2_best = float(line.split(":")[1].strip())
        
        # So sánh và lưu mô hình nếu hiệu suất tốt hơn
        if rmse < rmse_best and r2 > r2_best:
            pickle.dump(model, open(path_best_model, 'wb'))  # Lưu mô hình
            with open(path_best_evaluation, "w") as file:
                file.write(results)  # Ghi kết quả đánh giá mới
            # print("best")  # Dòng này bị comment, có thể bỏ hoặc bật để debug
    except Exception as e:
        # Xử lý lỗi nếu có và in thông báo
        print(f"An error occurred: {e}")
        pass

def LH_AutoRetrainingModel(PG_cursor):
    try:
        path_data = "D:/001.Project/LDA_master/data/DATA_LH.csv"
        get_DATA_LH(PG_cursor, path_data)
        # LH_TrainModel(path_data)
    except Exception as e:
        print(f"An error occurred: {e}")
        pass

def get_DATA_LH(PG_cursor, path_data):
    """
        Export dữ liệu từ DB về local
        1. Workflow:
            - Giai đoạn 1: Query data DATA_CTCN
            - Giai đoạn 2: Query data LH1_DCS_Items
            - Giai đoạn 2: Query data LH2_DCS_Items
            - Giai đoạn 4: Ghép DATA_CTCN và DCS_Items để tạo data DATA_LH.csv
        
        2. Parameters:
            PG_cursor: Cursor để thực thi truy vấn SQL.
            PG_conn: Kết nối đến database PostgreSQL.
    """
    try:
        # Giai đoạn 1: Query data DATA_CTCN
        columns_DATA_CTCN = [
            "CronTime", "LDA12080012000243", "LDA12080012000228", "LDA12080012000227", 
            "LDA12080012000230", "LDA12080012000238", "LDA12080012000237", 
            "LDA12080012000232", "LDA12080012000236", "LDA12080012000235", 
            "LDA12080012000234", "LDA12080012000233"]
        query_DATA_CTCN = '''
            SELECT "CronTime", "LDA12080012000243", "LDA12080012000228", "LDA12080012000227", 
            "LDA12080012000230", "LDA12080012000238", "LDA12080012000237", 
            "LDA12080012000232", "LDA12080012000236", "LDA12080012000235", 
            "LDA12080012000234", "LDA12080012000233" FROM "DATA_CTCN" ORDER BY "CronTime" DESC'''
        PG_cursor.execute(query_DATA_CTCN)
        DATA_CTCN = PG_cursor.fetchall()
        DATA_CTCN = pd.DataFrame(DATA_CTCN, columns=columns_DATA_CTCN)

        # Giai đoạn 2: Query data LH1_DCS_Items
        columns_DCS_Items = [
            "CronTime", "FT1151_DACA_PV__Value", "TE1251_DACA_PV__Value",
            "FT1151_DACA_PV__Value_Other", "Z_BEDT_DACA_PV__Value", "PT1281_DACA_PV__Value",
            "AT1011_DACA_PV__Value", "AT1012_DACA_PV__Value", "TE1212_DACA_PV__Value",
            "PT1061_DACA_PV__Value", "PT1071_DACA_PV__Value", "PT1111_DACA_PV__Value",
            "PT1112_DACA_PV__Value", "PT1211_DACA_PV__Value", "PT1212_DACA_PV__Value",
            "TZ1131ZT_DACA_PV__Value", "S051AIT_DACA_PV__Value", "AZ1011ZT_DACA_PV__Value",
            "S052AIT_DACA_PV__Value", "S052AVFD_CRT_DACA_PV__Value", "S052AVFD_FB_DACA_PV__Value",
            "PT1081_DACA_PV__Value", "PT1082_DACA_PV__Value", "PT1091_DACA_PV__Value",
            "PT1092_DACA_PV__Value", "TE1111_DACA_PV__Value", "TE1112_DACA_PV__Value",
            "FT1151_DIVA_OUT__Value"]
        
        query_LH1_DCS_Items = '''
            SELECT "CronTime", "B1_FT1151_DACA_PV__Value", "B1_TE1251_DACA_PV__Value",
            "B2_FT1151_DACA_PV__Value", "B1_Z_BEDT_DACA_PV__Value", "B1_PT1281_DACA_PV__Value",
            "B1_AT1011_DACA_PV__Value", "B1_AT1012_DACA_PV__Value", "B1_TE1212_DACA_PV__Value",
            "B1_PT1061_DACA_PV__Value", "B1_PT1071_DACA_PV__Value", "B1_PT1111_DACA_PV__Value",
            "B1_PT1112_DACA_PV__Value", "B1_PT1211_DACA_PV__Value", "B1_PT1212_DACA_PV__Value",
            "B1_TZ1131ZT_DACA_PV__Value", "B1_S051AIT_DACA_PV__Value", "B1_AZ1011ZT_DACA_PV__Value",
            "B1_S052AIT_DACA_PV__Value", "B1_S052AVFD_CRT_DACA_PV__Value", "B1_S052AVFD_FB_DACA_PV__Value",
            "B1_PT1081_DACA_PV__Value", "B1_PT1082_DACA_PV__Value", "B1_PT1091_DACA_PV__Value",
            "B1_PT1092_DACA_PV__Value", "B1_TE1111_DACA_PV__Value", "B1_TE1112_DACA_PV__Value",
            "B1_FT1151_DIVA_OUT__Value" FROM "DCS_Items" ORDER BY "CronTime" DESC
            '''
        PG_cursor.execute(query_LH1_DCS_Items)
        LH1_DCS_Items = PG_cursor.fetchall()
        LH1_DCS_Items = pd.DataFrame(LH1_DCS_Items , columns=columns_DCS_Items)

        # Giai đoạn 3: Query data LH2_DCS_Items
        query_LH2_DCS_Items = '''
            SELECT "CronTime", "B2_FT1151_DACA_PV__Value", "B2_TE1251_DACA_PV__Value",
            "B1_FT1151_DACA_PV__Value", "B2_Z_BEDT_DACA_PV__Value", "B2_PT1281_DACA_PV__Value",
            "B2_AT1011_DACA_PV__Value", "B2_AT1012_DACA_PV__Value", "B2_TE1212_DACA_PV__Value",
            "B2_PT1061_DACA_PV__Value", "B2_PT1071_DACA_PV__Value", "B2_PT1111_DACA_PV__Value",
            "B2_PT1112_DACA_PV__Value", "B2_PT1211_DACA_PV__Value", "B2_PT1212_DACA_PV__Value",
            "B2_TZ1131ZT_DACA_PV__Value", "B2_S051AIT_DACA_PV__Value", "B2_AZ1011ZT_DACA_PV__Value",
            "B2_S052AIT_DACA_PV__Value", "B2_S052AVFD_CRT_DACA_PV__Value", "B2_S052AVFD_FB_DACA_PV__Value",
            "B2_PT1081_DACA_PV__Value", "B2_PT1082_DACA_PV__Value", "B2_PT1091_DACA_PV__Value",
            "B2_PT1092_DACA_PV__Value", "B2_TE1111_DACA_PV__Value", "B2_TE1112_DACA_PV__Value",
            "B2_FT1151_DIVA_OUT__Value" FROM "DCS_Items" ORDER BY "CronTime" DESC
            '''
        PG_cursor.execute(query_LH2_DCS_Items)
        LH2_DCS_Items = PG_cursor.fetchall()
        LH2_DCS_Items = pd.DataFrame(LH2_DCS_Items , columns=columns_DCS_Items)

        # Giai đoạn 4: Tạo data DATA_LH.csv
        DATA_CTCN['CronTime'] = pd.to_datetime(DATA_CTCN['CronTime'])
        LH1_DCS_Items['CronTime'] = pd.to_datetime(LH1_DCS_Items['CronTime'])
        LH2_DCS_Items['CronTime'] = pd.to_datetime(LH2_DCS_Items['CronTime'])
        DATA_CTCN = DATA_CTCN.set_index('CronTime')
        DATA_CTCN = DATA_CTCN.resample('min').mean()
        DATA_CTCN = DATA_CTCN.interpolate(method='linear')
        df_LH1 = pd.merge(DATA_CTCN, LH1_DCS_Items, on="CronTime")
        df_LH2 = pd.merge(DATA_CTCN, LH2_DCS_Items, on="CronTime")
        df_LH = pd.concat([df_LH1, df_LH2], ignore_index=True)
        df_LH.to_csv(path_data, index=False)
    except Exception as e:
        print(f"An error occurred: {e}")
        pass

def LH_TrainModel(path_data):
    """
        Huấn luyện mô hình dự đoán dựa trên dữ liệu từ file CSV
        1. Workflow:
            - Giai đoạn 1: Đọc và tiền xử lý dữ liệu từ file CSV
            - Giai đoạn 2: Lọc và dịch chuyển dữ liệu theo thời gian
            - Giai đoạn 3: Chia dữ liệu thành tập huấn luyện và kiểm tra
            - Giai đoạn 4: Huấn luyện mô hình và đánh giá hiệu suất
            - Giai đoạn 5: Lưu mô hình tốt nhất nếu vượt trội
            
        2. Parameters:
            path_data: Đường dẫn đến file CSV chứa dữ liệu đầu vào
    """
    try:
        # Khởi tạo ngày bắt đầu để lọc dữ liệu
        start_date = datetime(2024, 11, 1)
        
        # Đọc dữ liệu từ file CSV vào DataFrame
        df_LH = pd.read_csv(path_data)
        
        # Chuyển cột CronTime sang định dạng datetime để xử lý thời gian
        df_LH['CronTime'] = pd.to_datetime(df_LH['CronTime'])
        
        # Lọc dữ liệu từ ngày start_date trở đi
        df_LH = df_LH[df_LH['CronTime'] >= start_date]
        
        # Loại bỏ các giá trị bất thường (999999) trong cột FT1151_DIVA_OUT__Value
        df_LH = df_LH[df_LH["FT1151_DIVA_OUT__Value"] != 999999.000000]

        # Dịch chuyển dữ liệu của các cột được liệt kê lên 8*60*2 dòng (tương ứng với khoảng thời gian)
        for col in [
            'LDA12080012000243', 'LDA12080012000228', 'LDA12080012000227',
            'LDA12080012000230', 'LDA12080012000238', 'LDA12080012000237',
            'LDA12080012000232', 'LDA12080012000236', 'LDA12080012000235',
            'LDA12080012000234', 'LDA12080012000233']:
            df_LH[f"{col}"] = df_LH[col].shift(-8*60*2)
        
        # Loại bỏ các hàng chứa giá trị NaN sau khi dịch chuyển
        df_LH = df_LH.dropna()
        
        # Lọc dữ liệu dựa trên ngưỡng của cột FT1151_DIVA_OUT__Value (0.12 đến 0.16)
        df_LH = df_LH[(df_LH['FT1151_DIVA_OUT__Value'] <= 0.16) & (df_LH['FT1151_DIVA_OUT__Value'] >= 0.12)]

        # Chuẩn bị dữ liệu đầu vào (X) và đầu ra (y) cho mô hình
        # CoalConsumption:
        X = df_LH[[
            "LDA12080012000243", "LDA12080012000228",
            "LDA12080012000227", "LDA12080012000230", "LDA12080012000238",
            "LDA12080012000237", "LDA12080012000232", "LDA12080012000236",
            "LDA12080012000235", "LDA12080012000234", "LDA12080012000233",
            "FT1151_DACA_PV__Value", "TE1251_DACA_PV__Value", "FT1151_DACA_PV__Value_Other",]]
        y = df_LH[[
            "Z_BEDT_DACA_PV__Value", "PT1281_DACA_PV__Value", "AT1011_DACA_PV__Value", 
            "AT1012_DACA_PV__Value", "TE1212_DACA_PV__Value", "PT1061_DACA_PV__Value",
            "PT1071_DACA_PV__Value", "PT1111_DACA_PV__Value", "PT1112_DACA_PV__Value", 
            "PT1211_DACA_PV__Value", "PT1212_DACA_PV__Value", "TZ1131ZT_DACA_PV__Value",
            "S051AIT_DACA_PV__Value", "AZ1011ZT_DACA_PV__Value", "S052AIT_DACA_PV__Value", 
            "S052AVFD_CRT_DACA_PV__Value", "S052AVFD_FB_DACA_PV__Value", "PT1081_DACA_PV__Value",
            "PT1082_DACA_PV__Value", "PT1091_DACA_PV__Value", "PT1092_DACA_PV__Value", 
            "TE1111_DACA_PV__Value", "TE1112_DACA_PV__Value"]]
        
        # Chia dữ liệu thành tập huấn luyện và tập kiểm tra (80% train, 20% test)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Huấn luyện mô hình MultiOutputRegressor với ExtraTreesRegressor
        model = MultiOutputRegressor(
            ExtraTreesRegressor(n_estimators=1, max_depth=10, n_jobs=2, random_state=42))
        model.fit(X_train, y_train)
        
        # Dự đoán trên tập kiểm tra
        y_pred = model.predict(X_test)

        # Đánh giá hiệu suất mô hình cho từng đầu ra
        rmse_list, r2_list = [],[]
        for i in range(y_test.shape[1]):
            mse = mean_squared_error(y_test.iloc[:, i], y_pred[:, i])  # Tính MSE
            rmse = np.sqrt(mse)  # Tính RMSE từ MSE
            r2 = r2_score(y_test.iloc[:, i], y_pred[:, i])  # Tính R-squared
            rmse_list.append(rmse)
            r2_list.append(r2)

        # Tính giá trị trung bình của RMSE và R-squared
        rmse = np.mean(rmse_list)
        r2 = np.mean(r2_list)
        
        # Lấy thời gian hiện tại để ghi vào kết quả
        current = datetime.now().strftime("%Y%m%d")
        
        # Chuẩn bị chuỗi kết quả đánh giá
        results = f"RMSE: {rmse}\nR-squared: {r2}\nList Root Mean Squared Error: {rmse_list}\nList R2: {r2_list}\nDatetime: {current}"
        
        # Đường dẫn lưu mô hình tốt nhất và file đánh giá
        path_best_model = f'D:/001.Project/LDA_master/autotrain/best/LH_Parameter_best.sav'
        path_best_evaluation = f'D:/001.Project/LDA_master/autotrain/best/LH_Parameter_best.txt'
        
        # Đọc file đánh giá hiện tại để lấy RMSE và R-squared tốt nhất
        with open(path_best_evaluation, "r") as file:
            lines = file.readlines()
        for line in lines:
            if "RMSE" in line:
                rmse_best = float(line.split(":")[1].strip())
            elif "R-squared" in line:
                r2_best = float(line.split(":")[1].strip())
        
        # So sánh và lưu mô hình nếu hiệu suất tốt hơn
        if rmse < rmse_best and r2 > r2_best:
            pickle.dump(model, open(path_best_model, 'wb'))  # Lưu mô hình
            with open(path_best_evaluation, "w") as file:
                file.write(results)  # Ghi kết quả đánh giá mới
            # print("best")  # Dòng này bị comment, có thể bỏ hoặc bật để debug
    except Exception as e:
        # Xử lý lỗi nếu có và in thông báo
        print(f"An error occurred: {e}")
        pass

# Lo Nung ######################################################################################

def LN_AutoRetrainingModel(PG_cursor):
    try:
        path_data = "D:/001.Project/LDA_master/data/DATA_LN.csv"
        start_time = datetime.now()
        get_DATA_LN(PG_cursor, path_data)
        df_LH = pd.read_csv(path_data)
        LN_TrainModel_Stage1(df_LH)
        LN_TrainModel_Stage2(df_LH)
        LN_TrainModel_COconsumption(df_LH)
        end_time = datetime.now()
        print(f"Duration: {end_time - start_time}")
    except Exception as e:
        print(f"An error occurred: {e}")
        pass

def get_DATA_LN(PG_cursor,path_data):
    try:
        columns_DATA_CTCN = ["CronTime", "LDA11070012000630", "LDA07060012000122",
                        "LDA07060012000155", "LDA07060012000156", "LDA07060012000157",
                        "LDA07060012000158", "LDA07060012000159", "LDA07060012000160",
                        "LDA07060012000161", "LDA07060012000162", "LDA07060012000163",
                        "LDA07060012000164", "LDA07060012000165", "LDA07060012000166"]
        query_DATA_CTCN = '''SELECT "CronTime", "LDA11070012000630", "LDA07060012000122",
                        "LDA07060012000155", "LDA07060012000156", "LDA07060012000157",
                        "LDA07060012000158", "LDA07060012000159", "LDA07060012000160",
                        "LDA07060012000161", "LDA07060012000162", "LDA07060012000163",
                        "LDA07060012000164", "LDA07060012000165", "LDA07060012000166" FROM "DATA_CTCN" ORDER BY "CronTime" DESC'''
        PG_cursor.execute(query_DATA_CTCN)
        DATA_CTCN = PG_cursor.fetchall()
        DATA_CTCN = pd.DataFrame(DATA_CTCN, columns=columns_DATA_CTCN)

        columns_DCS_Items = ["CronTime","CM_A181_V19_COM_V19_IN_5_PV3__Value", "CM_A181FT0010_DACA_PV__Value",
                        "CM_A181FT0001_DACA_PV__Value", "CM_A181PT0013_DACA_PV__Value",
                        "CM_A181AT0001_DACA_PV__Value", "CM_A181PT0002_DACA_PV__Value",
                        "CM_A181PT0003_DACA_PV__Value", "CM_A181PT0004_DACA_PV__Value",
                        "CM_A181PDT0002_DACA_PV__Value", "CM_A181PT0005_DACA_PV__Value",
                        "CM_A181PT0006_DACA_PV__Value", "CM_A181PT0007_DACA_PV__Value",
                        "CM_A181PT0008_DACA_PV__Value", "CM_A181TE0007_DACA_PV__Value",
                        "CM_A181S015BPGPV_DACA_PV__Value", "CM_A181_TIEUHAOCO_OUT__Value"]
        query_DCS_Items = '''SELECT "CronTime","CM_A181_V19_COM_V19_IN_5_PV3__Value", "CM_A181FT0010_DACA_PV__Value",
                        "CM_A181FT0001_DACA_PV__Value", "CM_A181PT0013_DACA_PV__Value",
                        "CM_A181AT0001_DACA_PV__Value", "CM_A181PT0002_DACA_PV__Value",
                        "CM_A181PT0003_DACA_PV__Value", "CM_A181PT0004_DACA_PV__Value",
                        "CM_A181PDT0002_DACA_PV__Value", "CM_A181PT0005_DACA_PV__Value",
                        "CM_A181PT0006_DACA_PV__Value", "CM_A181PT0007_DACA_PV__Value",
                        "CM_A181PT0008_DACA_PV__Value", "CM_A181TE0007_DACA_PV__Value",
                        "CM_A181S015BPGPV_DACA_PV__Value", "CM_A181_TIEUHAOCO_OUT__Value" FROM "DCS_Items" ORDER BY "CronTime" DESC'''
        PG_cursor.execute(query_DCS_Items)
        DCS_Items = PG_cursor.fetchall()
        DCS_Items = pd.DataFrame(DCS_Items , columns=columns_DCS_Items)

        DATA_CTCN['CronTime'] = pd.to_datetime(DATA_CTCN['CronTime'])
        DCS_Items['CronTime'] = pd.to_datetime(DCS_Items['CronTime'])
        DATA_CTCN = DATA_CTCN.set_index('CronTime')
        DATA_CTCN = DATA_CTCN.resample('min').mean()
        DATA_CTCN = DATA_CTCN.interpolate(method='linear')

        df_LN = pd.merge(DATA_CTCN, DCS_Items, on="CronTime")
        # print("df_LN:",df_LN)
        df_LN.to_csv(path_data, index=False)
    except Exception as e:
        print(f"An error occurred: {e}")
        pass

# Auto training LN_Stage 1##################################
def LN_TrainModel_Stage1(df_LH):
    try:
        df_LH = df_LH[((df_LH["CM_A181_TIEUHAOCO_OUT__Value"] < 575) & (df_LH["CM_A181_TIEUHAOCO_OUT__Value"] > 425))] 
        columns_to_shift = [
            'CM_A181TE0007_DACA_PV__Value','CM_A181S015BPGPV_DACA_PV__Value'
        ]
        df_LH = pd.DataFrame(df_LH)
        for col in columns_to_shift:
            df_LH[col + '_t+1'] = df_LH[col].shift(-1)
        df_LH = df_LH.dropna()
        X_stage1 = df_LH[["LDA11070012000630", "LDA07060012000122",
            "LDA07060012000155", "LDA07060012000156", "LDA07060012000157",
            "LDA07060012000158", "LDA07060012000159", "LDA07060012000160",
            "LDA07060012000161", "LDA07060012000162", "LDA07060012000163",
            "LDA07060012000164", "LDA07060012000165", "LDA07060012000166",
            "CM_A181_V19_COM_V19_IN_5_PV3__Value", "CM_A181FT0010_DACA_PV__Value",
            "CM_A181FT0001_DACA_PV__Value", "CM_A181PT0013_DACA_PV__Value",
            "CM_A181AT0001_DACA_PV__Value", "CM_A181PT0002_DACA_PV__Value",
            "CM_A181PT0003_DACA_PV__Value", "CM_A181PT0004_DACA_PV__Value",
            "CM_A181PDT0002_DACA_PV__Value", "CM_A181PT0005_DACA_PV__Value",
            "CM_A181PT0006_DACA_PV__Value", "CM_A181PT0007_DACA_PV__Value",
            "CM_A181PT0008_DACA_PV__Value", "CM_A181TE0007_DACA_PV__Value", "CM_A181S015BPGPV_DACA_PV__Value"]]
        y_stage1 = df_LH[["CM_A181TE0007_DACA_PV__Value_t+1", "CM_A181S015BPGPV_DACA_PV__Value_t+1"]]

        X_train, X_test, y_train, y_test = train_test_split(X_stage1, y_stage1, test_size=0.2, random_state=42)
        model = MultiOutputRegressor(HistGradientBoostingRegressor())
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        rmse_list, r2_list = [],[]
        for i in range(y_test.shape[1]):
            mse = mean_squared_error(y_test.iloc[:, i], y_pred[:, i])
            rmse = np.sqrt(mse)
            r2 = r2_score(y_test.iloc[:, i], y_pred[:, i])
            # print(f"RMSE {y_stage1[i]}: {rmse}")
            # print(f"R-squared {y_stage1[i]}: {r2}")
            rmse_list.append(rmse)
            r2_list.append(r2)

        rmse = np.mean(rmse_list)
        r2 = np.mean(r2_list)
        current = datetime.now().strftime("%Y%m%d")
        results = f"RMSE: {rmse}\nR-squared: {r2}\nList Root Mean Squared Error: {rmse_list}\nList R2: {r2_list}\nDatetime: {current}"
        path_best_model = f'D:/001.Project/LDA_master/autotrain/best/LN_modelOptimizerParameter_Stage1_best.sav'
        path_best_evaluation = f'D:/001.Project/LDA_master/autotrain/best/LN_modelOptimizerParameter_Stage1_best.txt'
        
        with open(path_best_evaluation, "r") as file:
            lines = file.readlines()
        for line in lines:
            if "RMSE" in line:
                rmse_best = float(line.split(":")[1].strip())
            elif "R-squared" in line:
                r2_best = float(line.split(":")[1].strip())
        if rmse < rmse_best and r2 > r2_best:
            pickle.dump(model, open(path_best_model, 'wb'))
            with open(path_best_evaluation, "w") as file:
                file.write(results)
            # print("best")
    except Exception as e:
        print(f"An error occurred: {e}")
        pass

# Auto training LN_Stage 2##################################
def LN_TrainModel_Stage2(df_LH):
    try:
        df_LH = df_LH[((df_LH["CM_A181_TIEUHAOCO_OUT__Value"] < 575) & (df_LH["CM_A181_TIEUHAOCO_OUT__Value"] > 425))] 
        columns_to_shift = [
            "CM_A181AT0001_DACA_PV__Value",
            "CM_A181PT0002_DACA_PV__Value",
            "CM_A181PT0003_DACA_PV__Value",
            "CM_A181PT0004_DACA_PV__Value",
            "CM_A181PDT0002_DACA_PV__Value",
            "CM_A181PT0005_DACA_PV__Value",
            "CM_A181PT0006_DACA_PV__Value",
            "CM_A181PT0007_DACA_PV__Value",
            "CM_A181PT0008_DACA_PV__Value",
            "CM_A181TE0007_DACA_PV__Value",
            "CM_A181S015BPGPV_DACA_PV__Value"]
        df_LH = pd.DataFrame(df_LH)
        for col in columns_to_shift:
            df_LH[col + '_t+1'] = df_LH[col].shift(-1)
        df_LH = df_LH.dropna()

        X_stage2 = df_LH[["LDA11070012000630", "LDA07060012000122",
            "LDA07060012000155", "LDA07060012000156", "LDA07060012000157",
            "LDA07060012000158", "LDA07060012000159", "LDA07060012000160",
            "LDA07060012000161", "LDA07060012000162", "LDA07060012000163",
            "LDA07060012000164", "LDA07060012000165", "LDA07060012000166",
            "CM_A181_V19_COM_V19_IN_5_PV3__Value", "CM_A181FT0010_DACA_PV__Value",
            "CM_A181FT0001_DACA_PV__Value", "CM_A181PT0013_DACA_PV__Value",
            "CM_A181AT0001_DACA_PV__Value", "CM_A181PT0002_DACA_PV__Value",
            "CM_A181PT0003_DACA_PV__Value", "CM_A181PT0004_DACA_PV__Value",
            "CM_A181PDT0002_DACA_PV__Value", "CM_A181PT0005_DACA_PV__Value",
            "CM_A181PT0006_DACA_PV__Value", "CM_A181PT0007_DACA_PV__Value",
            "CM_A181PT0008_DACA_PV__Value", "CM_A181TE0007_DACA_PV__Value",
            "CM_A181S015BPGPV_DACA_PV__Value","CM_A181TE0007_DACA_PV__Value_t+1",
            "CM_A181S015BPGPV_DACA_PV__Value_t+1"]]
        y_stage2 = df_LH[["CM_A181AT0001_DACA_PV__Value_t+1", "CM_A181PT0002_DACA_PV__Value_t+1",
            "CM_A181PT0003_DACA_PV__Value_t+1", "CM_A181PT0004_DACA_PV__Value_t+1",
            "CM_A181PDT0002_DACA_PV__Value_t+1", "CM_A181PT0005_DACA_PV__Value_t+1",
            "CM_A181PT0006_DACA_PV__Value_t+1", "CM_A181PT0007_DACA_PV__Value_t+1",
            "CM_A181PT0008_DACA_PV__Value_t+1"]]

        X_train, X_test, y_train, y_test = train_test_split(X_stage2, y_stage2, test_size=0.2, random_state=42)
        model = MultiOutputRegressor(HistGradientBoostingRegressor())
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        rmse_list, r2_list = [],[]
        for i in range(y_test.shape[1]):
            mse = mean_squared_error(y_test.iloc[:, i], y_pred[:, i])
            rmse = np.sqrt(mse)
            r2 = r2_score(y_test.iloc[:, i], y_pred[:, i])
            # print(f"RMSE {y_stage2[i]}: {rmse}")
            # print(f"R-squared {y_stage2[i]}: {r2}")
            rmse_list.append(rmse)
            r2_list.append(r2)

        rmse = np.mean(rmse_list)
        r2 = np.mean(r2_list)
        current = datetime.now().strftime("%Y%m%d")
        results = f"RMSE: {rmse}\nR-squared: {r2}\nList Root Mean Squared Error: {rmse_list}\nList R2: {r2_list}\nDatetime: {current}"
        path_best_model = f'D:/001.Project/LDA_master/autotrain/best/LN_modelOptimizerParameter_Stage2_best.sav'
        path_best_evaluation = f'D:/001.Project/LDA_master/autotrain/best/LN_modelOptimizerParameter_Stage2_best.txt'
        
        with open(path_best_evaluation, "r") as file:
            lines = file.readlines()
        for line in lines:
            if "RMSE" in line:
                rmse_best = float(line.split(":")[1].strip())
            elif "R-squared" in line:
                r2_best = float(line.split(":")[1].strip())
        if rmse < rmse_best and r2 > r2_best:
            pickle.dump(model, open(path_best_model, 'wb'))
            with open(path_best_evaluation, "w") as file:
                file.write(results)
            # print("best")
    except Exception as e:
        print(f"An error occurred: {e}")
        pass

# Auto training LN_COconsumption##################################
def LN_TrainModel_COconsumption(df_LH):
    try:
        df_LH = df_LH[((df_LH["CM_A181_TIEUHAOCO_OUT__Value"] < 575) & (df_LH["CM_A181_TIEUHAOCO_OUT__Value"] > 425))] 
        X_COconsumption = df_LH[["LDA11070012000630", "LDA07060012000122",
            "LDA07060012000155", "LDA07060012000156", "LDA07060012000157",
            "LDA07060012000158", "LDA07060012000159", "LDA07060012000160",
            "LDA07060012000161", "LDA07060012000162", "LDA07060012000163",
            "LDA07060012000164", "LDA07060012000165", "LDA07060012000166",
            "CM_A181_V19_COM_V19_IN_5_PV3__Value", "CM_A181FT0010_DACA_PV__Value",
            "CM_A181FT0001_DACA_PV__Value", "CM_A181PT0013_DACA_PV__Value",
            "CM_A181AT0001_DACA_PV__Value", "CM_A181PT0002_DACA_PV__Value",
            "CM_A181PT0003_DACA_PV__Value", "CM_A181PT0004_DACA_PV__Value",
            "CM_A181PDT0002_DACA_PV__Value", "CM_A181PT0005_DACA_PV__Value",
            "CM_A181PT0006_DACA_PV__Value", "CM_A181PT0007_DACA_PV__Value",
            "CM_A181PT0008_DACA_PV__Value","CM_A181TE0007_DACA_PV__Value","CM_A181S015BPGPV_DACA_PV__Value"]]
        y_COconsumption = df_LH[["CM_A181_TIEUHAOCO_OUT__Value"]]

        X_train, X_test, y_train, y_test = train_test_split(X_COconsumption, y_COconsumption, test_size=0.2, random_state=42)
        model = HistGradientBoostingRegressor()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        mse = mean_squared_error(y_test.iloc[:], y_pred[:])
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test.iloc[:], y_pred[:])

        current = datetime.now().strftime("%Y%m%d")
        results = f"RMSE: {rmse}\nR-squared: {r2}\nDatetime: {current}"
        path_best_model = f'D:/001.Project/LDA_master/autotrain/best/LN_modelOptimizerParameter_COconsumption_best.sav'
        path_best_evaluation = f'D:/001.Project/LDA_master/autotrain/best/LN_modelOptimizerParameter_COconsumption_best.txt'
        
        with open(path_best_evaluation, "r") as file:
            lines = file.readlines()
        for line in lines:
            if "RMSE" in line:
                rmse_best = float(line.split(":")[1].strip())
            elif "R-squared" in line:
                r2_best = float(line.split(":")[1].strip())
        if rmse < rmse_best and r2 > r2_best:
            pickle.dump(model, open(path_best_model, 'wb'))
            with open(path_best_evaluation, "w") as file:
                file.write(results)
            # print("best")
    except Exception as e:
        print(f"An error occurred: {e}")
        pass