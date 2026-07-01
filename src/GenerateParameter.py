import numpy as np
from datetime import datetime
from geneticalgorithm2 import geneticalgorithm2 as ga
import pickle
import pandas as pd

def load_model(filename):
    model = pickle.load(open(filename, 'rb'))
    return model

loaded_model_LH1 = load_model('D:/001.Project/LDA_master/models/LH1_ZML_2025.sav')
def objective_function_LH1(X):
    """
        Hàm mục tiêu (objective function) được sử dụng để đánh giá một bộ tham số đầu vào X.  
        Hàm này dự đoán giá trị mục tiêu bằng mô hình đã được huấn luyện.

        Tham số:
            X (numpy.ndarray): Một mảng đầu vào chứa các tham số cần tối ưu hóa.

        Quá trình thực hiện:
            1. Ghép nối X với dữ liệu đầu vào `input_stage1` để tạo thành mảng đầu vào hoàn chỉnh.
            2. Tải mô hình dự đoán từ tệp đã lưu.
            3. Dự đoán giá trị mục tiêu bằng mô hình đã tải.
            4. Trả về kết quả dự đoán dưới dạng một số duy nhất.

        Trả về:
            float: Giá trị dự đoán từ mô hình.
    """
    try:
        X_sample = input_stage1
        input_data = np.concatenate((X_sample, X.reshape(1, -1)), axis=1)
        target = loaded_model_LH1.predict(input_data)
        return float(target.item())
    except Exception as e:
        print(f"[Penalty] Invalid parameters {X}: {e}")
        return 1e6  

loaded_model_LH2 = load_model('D:/001.Project/LDA_master/models/LH2_ZML_2025.sav')
def objective_function_LH2(X):
    """
        Hàm mục tiêu (objective function) được sử dụng để đánh giá một bộ tham số đầu vào X.  
        Hàm này dự đoán giá trị mục tiêu bằng mô hình đã được huấn luyện.

        Tham số:
            X (numpy.ndarray): Một mảng đầu vào chứa các tham số cần tối ưu hóa.

        Quá trình thực hiện:
            1. Ghép nối X với dữ liệu đầu vào `input_stage1` để tạo thành mảng đầu vào hoàn chỉnh.
            2. Tải mô hình dự đoán từ tệp đã lưu.
            3. Dự đoán giá trị mục tiêu bằng mô hình đã tải.
            4. Trả về kết quả dự đoán dưới dạng một số duy nhất.

        Trả về:
            float: Giá trị dự đoán từ mô hình.
    """
    try:
        X_sample = input_stage1
        input_data = np.concatenate((X_sample, X.reshape(1, -1)), axis=1)
        target = loaded_model_LH2.predict(input_data)
        return float(target.item())
    except Exception as e:
        print(f"[Penalty] Invalid parameters {X}: {e}")
        return 1e6  

def LH1_GenerateParameter(input, PG_cursor, PG_conn, model_LH1_GenerateParameter):
    """
        1. Workflow:
            Tạo bộ thông số vận hành tối ưu và bộ thông số Local dựa trên dữ liệu từ API gửi về.
            - Giai đoạn 1: Tạo dữ liệu đầu vào để tạo bộ thông số tiêu chuẩn
            - Giai đoạn 2: Tạo ngưỡng tối ưu dựa trên bộ thông số đó
            - Giai đoạn 3: Cấu hình GA và khởi tạo GA
            - Giai đoạn 4: Chạy hàm GA để có bộ thông số tối ưu tốt nhất
            - Giai đoạn 5: Chạy model History để có bộ thông số phù hợp với tải và tính toán tiêu hao than dự kiến
            - Giai đoạn 6: Khởi tạo cấu trúc output dưới dạng json
            - Giai đoạn 7: Lưu vào database
        
        2. Parameters:
            PG_cursor: Cursor để thực thi truy vấn SQL.
            PG_conn: Kết nối đến database PostgreSQL.
            input_stage1: Dữ liệu đầu vào từ API
            model_LH1_GenerateParameter: Mô hình ML dự đoán tham số tối ưu hóa ban đầu.
            param_bounds: Tạo ngưỡng tối ưu dựa trên bộ thông số đó
            best_solution: Bộ thông số sau khi tối ưu
            best_fitness: Tiêu hao tối ưu
            OptimizerParameter_CoalConsumption: Bộ thông số tối ưu mới nhất
    """
    try:
        # Giai đoạn 1: Tạo dữ liệu đầu vào để tạo bộ thông số tiêu chuẩn
        global input_stage1
        input_stage1 = np.array(input).reshape(1, -1)
        print('input_stage1:', input_stage1)
        GenerateParameter = model_LH1_GenerateParameter.predict(input_stage1)
        
        # Giai đoạn 2: Tạo ngưỡng tối ưu dựa trên bộ thông số đó
        rate_high = 0.015 # Điều chỉnh +1.5%
        rate_low = 0.015 # Điều chỉnh -1.5%
        param_bounds = []
        for pred in GenerateParameter[0]:
            lower_bound = pred * (1 - rate_low)
            upper_bound = pred * (1 + rate_high)
            if lower_bound >= upper_bound:
                lower_bound, upper_bound = sorted([lower_bound, upper_bound]) 
            param_bounds.append([lower_bound, upper_bound])
        param_bounds = np.array(param_bounds)

        # Giai đoạn 3: Cấu hình GA và khởi tạo GA
        algorithm_params = {
            'max_num_iteration': 1000,    # Tăng số thế hệ để cải thiện khả năng tìm kiếm giải pháp tốt hơn
            'population_size': 50,        # Tăng kích thước quần thể để đa dạng hóa gen, tránh kẹt ở cực trị địa phương
            'mutation_probability': 0.2,  # Giảm xác suất đột biến để duy trì sự ổn định nhưng vẫn đảm bảo khám phá không gian
            'elit_ratio': 0.1,            # Tăng tỷ lệ cá thể ưu tú để giữ lại nhiều giải pháp tốt hơn qua các thế hệ
            # 'crossover_probability': 0.8, # Tăng xác suất lai ghép để đẩy mạnh sự kết hợp gen tốt
            'parents_portion': 0.5,       # Tăng tỷ lệ chọn làm cha mẹ để đảm bảo nhiều nguồn gen tốt được kết hợp
            'crossover_type': 'one_point', # Chuyển sang lai ghép điểm đơn để tăng tính đột phá khi kết hợp gen
            'max_iteration_without_improv': 50, # Tăng ngưỡng dừng để tránh kết luận sớm khi mô hình chưa tối ưu
        }
        model = ga(
            dimension=len(GenerateParameter[0]),
            variable_type='real',
            variable_boundaries=param_bounds,
            algorithm_parameters=algorithm_params
        )

        # Giai đoạn 4: Chạy hàm GA để có bộ thông số tối ưu tốt nhất
        model.run(function=objective_function_LH1, no_plot = True, disable_printing=True)
        OptimizerParameter = model.result['variable']
        OptimizerParameter_CoalConsumption = model.result['score']/(input_stage1[0][11] + 1e-10)
        print('OptimizerParameter:', OptimizerParameter)
        print('CoalConsumption:', OptimizerParameter_CoalConsumption)

        # Giai đoạn 5: Chạy model History để có bộ thông số phù hợp với tải và tính toán tiêu hao than dự kiến
        # HistoryParameter = model_LH1_HistoryParameter.predict(input_stage1)
        # input_HistoryParameter_coalconsumption = np.hstack((input_stage1, HistoryParameter))
        # HistoryParameter_CoalConsumption = model_LH1_CoalConsumption.predict(input_HistoryParameter_coalconsumption)
        # print("HistoryParameter:", HistoryParameter)
        # print("HistoryParameter_CoalConsumption:", HistoryParameter_CoalConsumption)
        power = input_stage1[0][11]
        df_baseparameter = pd.read_csv('../baseparameters/baseparameter_LH1.csv')
        bins = df_baseparameter['power_bin'].unique()
        # Tìm bin gần nhất với công suất hiện tại
        nearest_bin = min(bins, key=lambda x: abs(x - power))
        # Lấy bộ thông số tương ứng
        row = df_baseparameter[df_baseparameter['power_bin'] == nearest_bin].iloc[0]
        print("Selected base parameters row:", row)

        # Giai đoạn 6: Khởi tạo cấu trúc output dưới dạng json
        crontime = datetime.now().strftime('%Y-%m-%d %H:%M:00')
        local_parameters = [
            row['B1_Z_BEDT_DACA_PV__Value'],
            row['B1_PT1281_DACA_PV__Value'],
            row['B1_AT1011_DACA_PV__Value'],
            row['B1_AT1012_DACA_PV__Value'],
            row['B1_TE1212_DACA_PV__Value'],
            row['B1_PT1061_DACA_PV__Value'],
            row['B1_PT1071_DACA_PV__Value'],
            row['B1_PT1111_DACA_PV__Value'],
            row['B1_PT1112_DACA_PV__Value'],
            row['B1_PT1211_DACA_PV__Value'],
            row['B1_PT1212_DACA_PV__Value'],
            row['B1_TZ1131ZT_DACA_PV__Value'],
            row['B1_S051AIT_DACA_PV__Value'],
            row['B1_AZ1011ZT_DACA_PV__Value'],
            row['B1_S052AIT_DACA_PV__Value'],
            row['B1_S052AVFD_CRT_DACA_PV__Value'],
            row['B1_S052AVFD_FB_DACA_PV__Value'],
            row['B1_PT1081_DACA_PV__Value'],
            row['B1_PT1082_DACA_PV__Value'],
            row['B1_PT1091_DACA_PV__Value'],
            row['B1_PT1092_DACA_PV__Value'],
            row['B1_TE1111_DACA_PV__Value'],
            row['B1_TE1112_DACA_PV__Value']
        ]
        output = {
            "CronTime": crontime,
            "LDA12080012000243": input_stage1[0][0], 
            "LDA12080012000228": input_stage1[0][1],
            "LDA12080012000227": input_stage1[0][2], 
            "LDA12080012000230": input_stage1[0][3], 
            "LDA12080012000238": input_stage1[0][4],
            "LDA12080012000237": input_stage1[0][5], 
            "LDA12080012000232": input_stage1[0][6], 
            "LDA12080012000236": input_stage1[0][7],
            "LDA12080012000235": input_stage1[0][8], 
            "LDA12080012000234": input_stage1[0][9], 
            "LDA12080012000233": input_stage1[0][10],
            "B1_FT1151_DACA_PV__Value": input_stage1[0][11],
            "B1_TE1251_DACA_PV__Value": input_stage1[0][12],
            "B2_FT1151_DACA_PV__Value": input_stage1[0][13],
            "Global_B1_Z_BEDT_DACA_PV__Value": OptimizerParameter[0], 
            "Global_B1_PT1281_DACA_PV__Value": OptimizerParameter[1],
            "Global_B1_AT1011_DACA_PV__Value": OptimizerParameter[2], 
            "Global_B1_AT1012_DACA_PV__Value": OptimizerParameter[3],
            "Global_B1_TE1212_DACA_PV__Value": OptimizerParameter[4], 
            "Global_B1_PT1061_DACA_PV__Value": OptimizerParameter[5],
            "Global_B1_PT1071_DACA_PV__Value": OptimizerParameter[6], 
            "Global_B1_PT1111_DACA_PV__Value": OptimizerParameter[7],
            "Global_B1_PT1112_DACA_PV__Value": OptimizerParameter[8], 
            "Global_B1_PT1211_DACA_PV__Value": OptimizerParameter[9],
            "Global_B1_PT1212_DACA_PV__Value": OptimizerParameter[10], 
            "Global_B1_TZ1131ZT_DACA_PV__Value": OptimizerParameter[11],
            "Global_B1_S051AIT_DACA_PV__Value": OptimizerParameter[12], 
            "Global_B1_AZ1011ZT_DACA_PV__Value": OptimizerParameter[13],
            "Global_B1_S052AIT_DACA_PV__Value": OptimizerParameter[14], 
            "Global_B1_S052AVFD_CRT_DACA_PV__Value": OptimizerParameter[15],
            "Global_B1_S052AVFD_FB_DACA_PV__Value": OptimizerParameter[16], 
            "Global_B1_PT1081_DACA_PV__Value": OptimizerParameter[17],
            "Global_B1_PT1082_DACA_PV__Value": OptimizerParameter[18], 
            "Global_B1_PT1091_DACA_PV__Value": OptimizerParameter[19],
            "Global_B1_PT1092_DACA_PV__Value": OptimizerParameter[20], 
            "Global_B1_TE1111_DACA_PV__Value": OptimizerParameter[21],
            "Global_B1_TE1112_DACA_PV__Value": OptimizerParameter[22], 
            "Global_B1_FT1151_DIVA_OUT__Value": OptimizerParameter_CoalConsumption,
            # "Local_B1_Z_BEDT_DACA_PV__Value": HistoryParameter[0][0], 
            # "Local_B1_PT1281_DACA_PV__Value": HistoryParameter[0][1],
            # "Local_B1_AT1011_DACA_PV__Value": HistoryParameter[0][2], 
            # "Local_B1_AT1012_DACA_PV__Value": HistoryParameter[0][3],
            # "Local_B1_TE1212_DACA_PV__Value": HistoryParameter[0][4], 
            # "Local_B1_PT1061_DACA_PV__Value": HistoryParameter[0][5],
            # "Local_B1_PT1071_DACA_PV__Value": HistoryParameter[0][6], 
            # "Local_B1_PT1111_DACA_PV__Value": HistoryParameter[0][7],
            # "Local_B1_PT1112_DACA_PV__Value": HistoryParameter[0][8], 
            # "Local_B1_PT1211_DACA_PV__Value": HistoryParameter[0][9],
            # "Local_B1_PT1212_DACA_PV__Value": HistoryParameter[0][10], 
            # "Local_B1_TZ1131ZT_DACA_PV__Value": HistoryParameter[0][11],
            # "Local_B1_S051AIT_DACA_PV__Value": HistoryParameter[0][12], 
            # "Local_B1_AZ1011ZT_DACA_PV__Value": HistoryParameter[0][13],
            # "Local_B1_S052AIT_DACA_PV__Value": HistoryParameter[0][14], 
            # "Local_B1_S052AVFD_CRT_DACA_PV__Value": HistoryParameter[0][15],
            # "Local_B1_S052AVFD_FB_DACA_PV__Value": HistoryParameter[0][16], 
            # "Local_B1_PT1081_DACA_PV__Value": HistoryParameter[0][17],
            # "Local_B1_PT1082_DACA_PV__Value": HistoryParameter[0][18], 
            # "Local_B1_PT1091_DACA_PV__Value": HistoryParameter[0][19],
            # "Local_B1_PT1092_DACA_PV__Value": HistoryParameter[0][20], 
            # "Local_B1_TE1111_DACA_PV__Value": HistoryParameter[0][21],
            # "Local_B1_TE1112_DACA_PV__Value": HistoryParameter[0][22], 
            # "Local_B1_FT1151_DIVA_OUT__Value": float(HistoryParameter_CoalConsumption[0])
            "Local_B1_Z_BEDT_DACA_PV__Value": row['B1_Z_BEDT_DACA_PV__Value'], 
            "Local_B1_PT1281_DACA_PV__Value": row['B1_PT1281_DACA_PV__Value'],
            "Local_B1_AT1011_DACA_PV__Value": row['B1_AT1011_DACA_PV__Value'],
            "Local_B1_AT1012_DACA_PV__Value": row['B1_AT1012_DACA_PV__Value'],
            "Local_B1_TE1212_DACA_PV__Value": row['B1_TE1212_DACA_PV__Value'],
            "Local_B1_PT1061_DACA_PV__Value": row['B1_PT1061_DACA_PV__Value'],
            "Local_B1_PT1071_DACA_PV__Value": row['B1_PT1071_DACA_PV__Value'], 
            "Local_B1_PT1111_DACA_PV__Value": row['B1_PT1111_DACA_PV__Value'],
            "Local_B1_PT1112_DACA_PV__Value": row['B1_PT1112_DACA_PV__Value'],
            "Local_B1_PT1211_DACA_PV__Value": row['B1_PT1211_DACA_PV__Value'],
            "Local_B1_PT1212_DACA_PV__Value": row['B1_PT1212_DACA_PV__Value'], 
            "Local_B1_TZ1131ZT_DACA_PV__Value": row['B1_TZ1131ZT_DACA_PV__Value'],
            "Local_B1_S051AIT_DACA_PV__Value": row['B1_S051AIT_DACA_PV__Value'],
            "Local_B1_AZ1011ZT_DACA_PV__Value": row['B1_AZ1011ZT_DACA_PV__Value'],
            "Local_B1_S052AIT_DACA_PV__Value": row['B1_S052AIT_DACA_PV__Value'],
            "Local_B1_S052AVFD_CRT_DACA_PV__Value": row['B1_S052AVFD_CRT_DACA_PV__Value'],
            "Local_B1_S052AVFD_FB_DACA_PV__Value": row['B1_S052AVFD_FB_DACA_PV__Value'],
            "Local_B1_PT1081_DACA_PV__Value": row['B1_PT1081_DACA_PV__Value'],
            "Local_B1_PT1082_DACA_PV__Value": row['B1_PT1082_DACA_PV__Value'],
            "Local_B1_PT1091_DACA_PV__Value": row['B1_PT1091_DACA_PV__Value'],
            "Local_B1_PT1092_DACA_PV__Value": row['B1_PT1092_DACA_PV__Value'],
            "Local_B1_TE1111_DACA_PV__Value": row['B1_TE1111_DACA_PV__Value'],
            "Local_B1_TE1112_DACA_PV__Value": row['B1_TE1112_DACA_PV__Value'],
            "Local_B1_FT1151_DIVA_OUT__Value": row['B1_FT1151_DIVA_OUT__Value']
        }
        print(output)

        # Giai đoạn 7: Lưu vào database
            # Truy vấn bảng "DATA_LH1_GenerateParameter" để lấy tên cột
        PG_cursor.execute('SELECT * FROM "DATA_LH1_GenerateParameter" LIMIT 1')
        name_columns = [desc[0] for desc in PG_cursor.description]
            # Tạo chuỗi cột và placeholders cho câu lệnh INSERT
        placeholders = ', '.join(['%s'] * len(name_columns))
        columns = ', '.join([f'"{col}"' for col in name_columns])
        values = [crontime] + [float(x) for x in input_stage1[0]] + [float(x) for x in OptimizerParameter] + [float(OptimizerParameter_CoalConsumption)] + [float(x) for x in local_parameters] + [float(row['B1_FT1151_DIVA_OUT__Value'])]
        print(values)
        insert_query = f'''
            INSERT INTO "DATA_LH1_GenerateParameter" ({columns}) VALUES ({placeholders})
            '''
        PG_cursor.execute(insert_query, values)
        PG_conn.commit()
        return output
    except Exception as e:
        PG_conn.rollback()
        print(f"An error occurred: {e}")
        return {"error": str(e)} 

def LH2_GenerateParameter(input, PG_cursor, PG_conn, model_LH2_GenerateParameter):
    """
        1. Workflow:
            Tạo bộ thông số vận hành tối ưu và bộ thông số Local dựa trên dữ liệu từ API gửi về.
            - Giai đoạn 1: Tạo dữ liệu đầu vào để tạo bộ thông số tiêu chuẩn
            - Giai đoạn 2: Tạo ngưỡng tối ưu dựa trên bộ thông số đó
            - Giai đoạn 3: Cấu hình GA và khởi tạo GA
            - Giai đoạn 4: Chạy hàm GA để có bộ thông số tối ưu tốt nhất
            - Giai đoạn 5: Chạy model History để có bộ thông số phù hợp với tải và tính toán tiêu hao than dự kiến
            - Giai đoạn 6: Khởi tạo cấu trúc output dưới dạng json
            - Giai đoạn 7: Lưu vào database
        
        2. Parameters:
            PG_cursor: Cursor để thực thi truy vấn SQL.
            PG_conn: Kết nối đến database PostgreSQL.
            input_stage1: Dữ liệu đầu vào từ API
            model_LH1_GenerateParameter: Mô hình ML dự đoán tham số tối ưu hóa ban đầu.
            param_bounds: Tạo ngưỡng tối ưu dựa trên bộ thông số đó
            best_solution: Bộ thông số sau khi tối ưu
            best_fitness: Tiêu hao tối ưu
            OptimizerParameter_CoalConsumption: Bộ thông số tối ưu mới nhất
    """
    try:
        # Giai đoạn 1: Tạo dữ liệu đầu vào để tạo bộ thông số tiêu chuẩn
        global input_stage1
        input_stage1 = np.array(input).reshape(1, -1)
        print('input_stage1:', input_stage1)
        GenerateParameter = model_LH2_GenerateParameter.predict(input_stage1)
        
        # Giai đoạn 2: Tạo ngưỡng tối ưu dựa trên bộ thông số đó
        rate_high = 0.015 # Điều chỉnh +1.5%
        rate_low = 0.015 # Điều chỉnh -1.5%
        param_bounds = []
        for pred in GenerateParameter[0]:
            lower_bound = pred * (1 - rate_low)
            upper_bound = pred * (1 + rate_high)
            if lower_bound >= upper_bound:
                lower_bound, upper_bound = sorted([lower_bound, upper_bound]) 
            param_bounds.append([lower_bound, upper_bound])
        param_bounds = np.array(param_bounds)

        # Giai đoạn 3: Cấu hình GA và khởi tạo GA
        algorithm_params = {
            'max_num_iteration': 1000,    # Tăng số thế hệ để cải thiện khả năng tìm kiếm giải pháp tốt hơn
            'population_size': 50,        # Tăng kích thước quần thể để đa dạng hóa gen, tránh kẹt ở cực trị địa phương
            'mutation_probability': 0.2,  # Giảm xác suất đột biến để duy trì sự ổn định nhưng vẫn đảm bảo khám phá không gian
            'elit_ratio': 0.1,            # Tăng tỷ lệ cá thể ưu tú để giữ lại nhiều giải pháp tốt hơn qua các thế hệ
            # 'crossover_probability': 0.8, # Tăng xác suất lai ghép để đẩy mạnh sự kết hợp gen tốt
            'parents_portion': 0.5,       # Tăng tỷ lệ chọn làm cha mẹ để đảm bảo nhiều nguồn gen tốt được kết hợp
            'crossover_type': 'one_point', # Chuyển sang lai ghép điểm đơn để tăng tính đột phá khi kết hợp gen
            'max_iteration_without_improv': 1, # Tăng ngưỡng dừng để tránh kết luận sớm khi mô hình chưa tối ưu
        }
        model = ga(
            dimension=len(GenerateParameter[0]),
            variable_type='real',
            variable_boundaries=param_bounds,
            algorithm_parameters=algorithm_params
        )

        # Giai đoạn 4: Chạy hàm GA để có bộ thông số tối ưu tốt nhất
        model.run(function=objective_function_LH2, no_plot = True, disable_printing=True)
        OptimizerParameter = model.result['variable']
        OptimizerParameter_CoalConsumption = model.result['score']/(input_stage1[0][11] + 1e-10)
        # print('OptimizerParameter:', OptimizerParameter)
        # print('CoalConsumption:', OptimizerParameter_CoalConsumption)

        # Giai đoạn 5: Chạy model History để có bộ thông số phù hợp với tải và tính toán tiêu hao than dự kiến
        # HistoryParameter = model_LH2_HistoryParameter.predict(input_stage1)
        # input_HistoryParameter_coalconsumption = np.hstack((input_stage1, HistoryParameter))
        # HistoryParameter_CoalConsumption = model_LH2_CoalConsumption.predict(input_HistoryParameter_coalconsumption)
        # print("HistoryParameter:", HistoryParameter)
        # print("HistoryParameter_CoalConsumption:", HistoryParameter_CoalConsumption)
        power = input_stage1[0][11]
        df_baseparameter = pd.read_csv('../baseparameters/baseparameter_LH2.csv')
        bins = df_baseparameter['power_bin'].unique()
        # Tìm bin gần nhất với công suất hiện tại
        nearest_bin = min(bins, key=lambda x: abs(x - power))
        # Lấy bộ thông số tương ứng
        row = df_baseparameter[df_baseparameter['power_bin'] == nearest_bin].iloc[0]
        print("Selected base parameters row:", row)

        # Giai đoạn 6: Khởi tạo cấu trúc output dưới dạng json
        crontime = datetime.now().strftime('%Y-%m-%d %H:%M:00')
        local_parameters = [
            row['B2_Z_BEDT_DACA_PV__Value'],
            row['B2_PT1281_DACA_PV__Value'],
            row['B2_AT1011_DACA_PV__Value'],
            row['B2_AT1012_DACA_PV__Value'],
            row['B2_TE1212_DACA_PV__Value'],
            row['B2_PT1061_DACA_PV__Value'],
            row['B2_PT1071_DACA_PV__Value'],
            row['B2_PT1111_DACA_PV__Value'],
            row['B2_PT1112_DACA_PV__Value'],
            row['B2_PT1211_DACA_PV__Value'],
            row['B2_PT1212_DACA_PV__Value'],
            row['B2_TZ1131ZT_DACA_PV__Value'],
            row['B2_S051AIT_DACA_PV__Value'],
            row['B2_AZ1011ZT_DACA_PV__Value'],
            row['B2_S052AIT_DACA_PV__Value'],
            row['B2_S052AVFD_CRT_DACA_PV__Value'],
            row['B2_S052AVFD_FB_DACA_PV__Value'],
            row['B2_PT1081_DACA_PV__Value'],
            row['B2_PT1082_DACA_PV__Value'],
            row['B2_PT1091_DACA_PV__Value'],
            row['B2_PT1092_DACA_PV__Value'],
            row['B2_TE1111_DACA_PV__Value'],
            row['B2_TE1112_DACA_PV__Value']
        ]
        output = {
            "CronTime": crontime,
            "LDA12080012000243": input_stage1[0][0], 
            "LDA12080012000228": input_stage1[0][1],
            "LDA12080012000227": input_stage1[0][2], 
            "LDA12080012000230": input_stage1[0][3], 
            "LDA12080012000238": input_stage1[0][4],
            "LDA12080012000237": input_stage1[0][5], 
            "LDA12080012000232": input_stage1[0][6], 
            "LDA12080012000236": input_stage1[0][7],
            "LDA12080012000235": input_stage1[0][8], 
            "LDA12080012000234": input_stage1[0][9], 
            "LDA12080012000233": input_stage1[0][10],
            "B2_FT1151_DACA_PV__Value": input_stage1[0][11],
            "B2_TE1251_DACA_PV__Value": input_stage1[0][12],
            "B1_FT1151_DACA_PV__Value": input_stage1[0][13],
            "Global_B2_Z_BEDT_DACA_PV__Value": OptimizerParameter[0], 
            "Global_B2_PT1281_DACA_PV__Value": OptimizerParameter[1],
            "Global_B2_AT1011_DACA_PV__Value": OptimizerParameter[2], 
            "Global_B2_AT1012_DACA_PV__Value": OptimizerParameter[3],
            "Global_B2_TE1212_DACA_PV__Value": OptimizerParameter[4], 
            "Global_B2_PT1061_DACA_PV__Value": OptimizerParameter[5],
            "Global_B2_PT1071_DACA_PV__Value": OptimizerParameter[6], 
            "Global_B2_PT1111_DACA_PV__Value": OptimizerParameter[7],
            "Global_B2_PT1112_DACA_PV__Value": OptimizerParameter[8], 
            "Global_B2_PT1211_DACA_PV__Value": OptimizerParameter[9],
            "Global_B2_PT1212_DACA_PV__Value": OptimizerParameter[10], 
            "Global_B2_TZ1131ZT_DACA_PV__Value": OptimizerParameter[11],
            "Global_B2_S051AIT_DACA_PV__Value": OptimizerParameter[12], 
            "Global_B2_AZ1011ZT_DACA_PV__Value": OptimizerParameter[13],
            "Global_B2_S052AIT_DACA_PV__Value": OptimizerParameter[14], 
            "Global_B2_S052AVFD_CRT_DACA_PV__Value": OptimizerParameter[15],
            "Global_B2_S052AVFD_FB_DACA_PV__Value": OptimizerParameter[16], 
            "Global_B2_PT1081_DACA_PV__Value": OptimizerParameter[17],
            "Global_B2_PT1082_DACA_PV__Value": OptimizerParameter[18], 
            "Global_B2_PT1091_DACA_PV__Value": OptimizerParameter[19],
            "Global_B2_PT1092_DACA_PV__Value": OptimizerParameter[20], 
            "Global_B2_TE1111_DACA_PV__Value": OptimizerParameter[21],
            "Global_B2_TE1112_DACA_PV__Value": OptimizerParameter[22], 
            "Global_B2_FT1151_DIVA_OUT__Value": OptimizerParameter_CoalConsumption,
            # "Local_B2_Z_BEDT_DACA_PV__Value": HistoryParameter[0][0], 
            # "Local_B2_PT1281_DACA_PV__Value": HistoryParameter[0][1],
            # "Local_B2_AT1011_DACA_PV__Value": HistoryParameter[0][2], 
            # "Local_B2_AT1012_DACA_PV__Value": HistoryParameter[0][3],
            # "Local_B2_TE1212_DACA_PV__Value": HistoryParameter[0][4], 
            # "Local_B2_PT1061_DACA_PV__Value": HistoryParameter[0][5],
            # "Local_B2_PT1071_DACA_PV__Value": HistoryParameter[0][6], 
            # "Local_B2_PT1111_DACA_PV__Value": HistoryParameter[0][7],
            # "Local_B2_PT1112_DACA_PV__Value": HistoryParameter[0][8], 
            # "Local_B2_PT1211_DACA_PV__Value": HistoryParameter[0][9],
            # "Local_B2_PT1212_DACA_PV__Value": HistoryParameter[0][10], 
            # "Local_B2_TZ1131ZT_DACA_PV__Value": HistoryParameter[0][11],
            # "Local_B2_S051AIT_DACA_PV__Value": HistoryParameter[0][12], 
            # "Local_B2_AZ1011ZT_DACA_PV__Value": HistoryParameter[0][13],
            # "Local_B2_S052AIT_DACA_PV__Value": HistoryParameter[0][14], 
            # "Local_B2_S052AVFD_CRT_DACA_PV__Value": HistoryParameter[0][15],
            # "Local_B2_S052AVFD_FB_DACA_PV__Value": HistoryParameter[0][16], 
            # "Local_B2_PT1081_DACA_PV__Value": HistoryParameter[0][17],
            # "Local_B2_PT1082_DACA_PV__Value": HistoryParameter[0][18], 
            # "Local_B2_PT1091_DACA_PV__Value": HistoryParameter[0][19],
            # "Local_B2_PT1092_DACA_PV__Value": HistoryParameter[0][20], 
            # "Local_B2_TE1111_DACA_PV__Value": HistoryParameter[0][21],
            # "Local_B2_TE1112_DACA_PV__Value": HistoryParameter[0][22], 
            # "Local_B2_FT1151_DIVA_OUT__Value": float(HistoryParameter_CoalConsumption[0])
            "Local_B2_Z_BEDT_DACA_PV__Value": row['B2_Z_BEDT_DACA_PV__Value'], 
            "Local_B2_PT1281_DACA_PV__Value": row['B2_PT1281_DACA_PV__Value'],
            "Local_B2_AT1011_DACA_PV__Value": row['B2_AT1011_DACA_PV__Value'],
            "Local_B2_AT1012_DACA_PV__Value": row['B2_AT1012_DACA_PV__Value'],
            "Local_B2_TE1212_DACA_PV__Value": row['B2_TE1212_DACA_PV__Value'],
            "Local_B2_PT1061_DACA_PV__Value": row['B2_PT1061_DACA_PV__Value'],
            "Local_B2_PT1071_DACA_PV__Value": row['B2_PT1071_DACA_PV__Value'], 
            "Local_B2_PT1111_DACA_PV__Value": row['B2_PT1111_DACA_PV__Value'],
            "Local_B2_PT1112_DACA_PV__Value": row['B2_PT1112_DACA_PV__Value'],
            "Local_B2_PT1211_DACA_PV__Value": row['B2_PT1211_DACA_PV__Value'],
            "Local_B2_PT1212_DACA_PV__Value": row['B2_PT1212_DACA_PV__Value'], 
            "Local_B2_TZ1131ZT_DACA_PV__Value": row['B2_TZ1131ZT_DACA_PV__Value'],
            "Local_B2_S051AIT_DACA_PV__Value": row['B2_S051AIT_DACA_PV__Value'],
            "Local_B2_AZ1011ZT_DACA_PV__Value": row['B2_AZ1011ZT_DACA_PV__Value'],
            "Local_B2_S052AIT_DACA_PV__Value": row['B2_S052AIT_DACA_PV__Value'],
            "Local_B2_S052AVFD_CRT_DACA_PV__Value": row['B2_S052AVFD_CRT_DACA_PV__Value'],
            "Local_B2_S052AVFD_FB_DACA_PV__Value": row['B2_S052AVFD_FB_DACA_PV__Value'],
            "Local_B2_PT1081_DACA_PV__Value": row['B2_PT1081_DACA_PV__Value'],
            "Local_B2_PT1082_DACA_PV__Value": row['B2_PT1082_DACA_PV__Value'],
            "Local_B2_PT1091_DACA_PV__Value": row['B2_PT1091_DACA_PV__Value'],
            "Local_B2_PT1092_DACA_PV__Value": row['B2_PT1092_DACA_PV__Value'],
            "Local_B2_TE1111_DACA_PV__Value": row['B2_TE1111_DACA_PV__Value'],
            "Local_B2_TE1112_DACA_PV__Value": row['B2_TE1112_DACA_PV__Value'],
            "Local_B2_FT1151_DIVA_OUT__Value": row['B2_FT1151_DIVA_OUT__Value']
        }
        # print(output)

        # Giai đoạn 7: Lưu vào database
            # Truy vấn bảng "DATA_LH2_GenerateParameter" để lấy tên cột
        PG_cursor.execute('SELECT * FROM "DATA_LH2_GenerateParameter" LIMIT 1')
        name_columns = [desc[0] for desc in PG_cursor.description]
            # Tạo chuỗi cột và placeholders cho câu lệnh INSERT
        placeholders = ', '.join(['%s'] * len(name_columns))
        columns = ', '.join([f'"{col}"' for col in name_columns])
        # values = [crontime] + [float(x) for x in input_stage1[0]] + [float(x) for x in OptimizerParameter] + [float(OptimizerParameter_CoalConsumption)] + [float(x) for x in HistoryParameter[0]] + [float(x) for x in HistoryParameter_CoalConsumption]
        values = [crontime] + [float(x) for x in input_stage1[0]] + [float(x) for x in OptimizerParameter] + [float(OptimizerParameter_CoalConsumption)] + [float(x) for x in local_parameters] + [float(row['B2_FT1151_DIVA_OUT__Value'])]
        # print(values)
        insert_query = f'''
            INSERT INTO "DATA_LH2_GenerateParameter" ({columns}) VALUES ({placeholders})
            '''
        PG_cursor.execute(insert_query, values)
        PG_conn.commit()
    except Exception as e:
        PG_conn.rollback()
        print(f"An error occurred: {e}")
        pass
    return output

def LN_GenerateParameter(crontime, input, PG_cursor, PG_conn, model_LN_OptimizerParameter_Stage1, model_LN_OptimizerParameter_Stage2, model_LN_OptimizerParameter_COConsumption):
    try:
        DATA_CTCN = input[:14]
        DCS_Items = input[14:18]
        DCS_Items_subparam = input[18:-1]
        crontime = datetime.now().strftime('%Y-%m-%d %H:%M:00')
        # Create input:
        input_stage1 = DATA_CTCN + DCS_Items + DCS_Items_subparam
        # print(input_stage1)
        # Predict Stage 1: 'CM_A181TE0007_DACA_PV__Value','CM_A181S015BPGPV_DACA_PV__Value'
        input_stage1 = np.array(input_stage1).reshape(1, -1)
        OptimizerParameter_Stage1 = model_LN_OptimizerParameter_Stage1.predict(input_stage1)
        
        # # Predict Stage 2: Cac thong so phu
        input_stage2 = np.hstack((input_stage1, OptimizerParameter_Stage1))
        # print(input_stage2)
        OptimizerParameter_Stage2 = model_LN_OptimizerParameter_Stage2.predict(input_stage2)

        # Predict CoalConsumption:
        input_stage1 = DATA_CTCN + DCS_Items
        input_stage1 = np.array(input_stage1).reshape(1, -1)
        # print(DATA_CTCN)
        # print(DCS_Items)
        # print(OptimizerParameter_Stage2)
        # print(OptimizerParameter_Stage1)
        input_COconsumption = np.hstack((input_stage1, OptimizerParameter_Stage2))
        input_COconsumption = np.hstack((input_COconsumption, OptimizerParameter_Stage1))
        # print(input_COconsumption)
        OptimizerParameter_COConsumption = model_LN_OptimizerParameter_COConsumption.predict(input_COconsumption)
        
        # print("DATA_CTCN:", DATA_CTCN)
        # print("DCS_Items:", DCS_Items)
        # print("TIEUHAOCO:", TIEUHAOCO)
        # print("OptimizerParameter_Stage2:", OptimizerParameter_Stage2)
        # print("OptimizerParameter_Stage3:", OptimizerParameter_Stage3)
        # print("OptimizerParameter_COConsumption:", OptimizerParameter_COConsumption)

        # Truy vấn bảng "DATA_LN_GenerateParameter" để lấy tên cột
        PG_cursor.execute('SELECT * FROM "DATA_LN_GenerateParameter" LIMIT 1')
        name_columns = [desc[0] for desc in PG_cursor.description]

        # Tạo chuỗi cột và placeholders cho câu lệnh INSERT
        placeholders = ', '.join(['%s'] * len(name_columns))
        columns = ', '.join([f'"{col}"' for col in name_columns])

        # crontime = datetime.now().strftime('%Y-%m-%d %H:%M:00')
        values = [crontime] + [float(x) for x in input_COconsumption[0]] + [float(x) for x in OptimizerParameter_COConsumption]
        # print(values)
        
        insert_query = f'''
        INSERT INTO "DATA_LN_GenerateParameter" ({columns}) VALUES ({placeholders})
        '''
        PG_cursor.execute(insert_query, values)
        PG_conn.commit() 

        # end_time = datetime.now()
        # print(f"Duration: {end_time - start_time}")
    except Exception as e:
        PG_conn.rollback()
        print(f"An error occurred: {e}")
        pass