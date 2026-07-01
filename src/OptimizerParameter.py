import pickle
import numpy as np
from datetime import datetime, time, timedelta
from geneticalgorithm2 import geneticalgorithm2 as ga
import json

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
    X_sample = input_stage1
    input = np.concatenate((X_sample, X.reshape(1, -1)), axis=1)
    target = loaded_model_LH1.predict(input)
    target = target.item()
    return target

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
    X_sample = input_stage1
    input = np.concatenate((X_sample, X.reshape(1, -1)), axis=1)
    target = loaded_model_LH2.predict(input)
    target = target.item()
    return target

def target_times_function():
    base_times = [time(6,0), time(14,0), time(22,0)]
    # Tạo danh sách target_times ±1 phút
    target_times = []
    for t in base_times:
        for minute_offset in [0, 1, 2, 3, 4, 5]:  # 0 = đúng giờ, 1 = thêm 1 phút
            new_hour = t.hour
            new_minute = t.minute + minute_offset
            if new_minute >= 60:
                new_minute -= 60
                new_hour = (new_hour + 1) % 24
            target_times.append(f"{new_hour:02d}:{new_minute:02d}:00")
    return target_times

def LN_OptimizerParameter(PG_cursor, PG_conn, model_LN_OptimizerParameter_Stage1, model_LN_OptimizerParameter_Stage2, model_LN_OptimizerParameter_COConsumption):
    try:
        print("Start LN_OptimizerParameter")
        OptimizerRate = 0.995
        path_DATA_CTCN_LN_lastest = 'D:/001.Project/LDA_master/errorprocessing/DATA_CTCN_LN_lastest.txt'
        query_crontime = '''SELECT "CronTime" FROM "DCS_Items" ORDER BY "CronTime" DESC LIMIT 1'''
        PG_cursor.execute(query_crontime)
        crontime = PG_cursor.fetchone()
        # start_time = datetime.now()
        # Stage 1: Predict FanID and P04 
        # Quere lastest Data Lo Nung
            # Query DATA_CTCN
        query_DATA_CTCN = '''SELECT "LDA11070012000630", "LDA07060012000122",
            "LDA07060012000155", "LDA07060012000156", "LDA07060012000157",
            "LDA07060012000158", "LDA07060012000159", "LDA07060012000160",
            "LDA07060012000161", "LDA07060012000162", "LDA07060012000163",
            "LDA07060012000164", "LDA07060012000165", "LDA07060012000166" FROM "DATA_CTCN" ORDER BY "CronTime" DESC LIMIT 1'''
        PG_cursor.execute(query_DATA_CTCN)
        DATA_CTCN = PG_cursor.fetchone()
        # print("DATA_CTCN:", DATA_CTCN)
        if None in DATA_CTCN:
            with open(path_DATA_CTCN_LN_lastest, 'r') as file:
                lines = file.readlines()
                DATA_CTCN = [float(value.strip()) for value in lines[0].split(',')]
        else:
            with open(path_DATA_CTCN_LN_lastest, 'w') as file:
                file.write(','.join(map(str, DATA_CTCN)))
            DATA_CTCN = [float(value) for value in DATA_CTCN]
        # print("DATA_CTCN:", DATA_CTCN)

            # Query DCS_Items
        query_DCS_Items = '''SELECT "CM_A181_V19_COM_V19_IN_5_PV3__Value", "CM_A181FT0010_DACA_PV__Value",
            "CM_A181FT0001_DACA_PV__Value", "CM_A181PT0013_DACA_PV__Value" FROM "DCS_Items" ORDER BY "CronTime" DESC LIMIT 1'''
        PG_cursor.execute(query_DCS_Items)
        DCS_Items = PG_cursor.fetchone()
        DCS_Items = [float(value) for value in DCS_Items]
        # print("DCS_Items:", DCS_Items)

            # Query TIEUHAOCO
        query_TIEUHAOCO = '''SELECT "CM_A181_TIEUHAOCO_OUT__Value" FROM "DCS_Items" ORDER BY "CronTime" DESC LIMIT 1'''
        PG_cursor.execute(query_TIEUHAOCO)
        TIEUHAOCO = PG_cursor.fetchone()
        # print("TIEUHAOCO GOC:", TIEUHAOCO)
        TIEUHAOCO = [float(value*OptimizerRate) for value in TIEUHAOCO]
        # print("TIEUHAOCO:", TIEUHAOCO)

        # print(DCS_Items)
        query_DCS_Items_subparam = '''SELECT
            "CM_A181AT0001_DACA_PV__Value", "CM_A181PT0002_DACA_PV__Value", "CM_A181PT0003_DACA_PV__Value",
            "CM_A181PT0004_DACA_PV__Value", "CM_A181PDT0002_DACA_PV__Value", "CM_A181PT0005_DACA_PV__Value", 
            "CM_A181PT0006_DACA_PV__Value", "CM_A181PT0007_DACA_PV__Value", "CM_A181PT0008_DACA_PV__Value",
            "CM_A181TE0007_DACA_PV__Value", "CM_A181S015BPGPV_DACA_PV__Value" FROM "DCS_Items" ORDER BY "CronTime" DESC LIMIT 1'''
        PG_cursor.execute(query_DCS_Items_subparam)
        DCS_Items_subparam = PG_cursor.fetchone()
        DCS_Items_subparam = [float(value) for value in DCS_Items_subparam]

        # Create input:
        input_stage1 = DATA_CTCN + DCS_Items + DCS_Items_subparam
        # Predict Stage 1: 'CM_A181TE0007_DACA_PV__Value','CM_A181S015BPGPV_DACA_PV__Value'
        input_stage1 = np.array(input_stage1).reshape(1, -1)
        OptimizerParameter_Stage1 = model_LN_OptimizerParameter_Stage1.predict(input_stage1)
        
        # # Predict Stage 2: Cac thong so phu
        input_stage2 = np.hstack((input_stage1, OptimizerParameter_Stage1))
        OptimizerParameter_Stage2 = model_LN_OptimizerParameter_Stage2.predict(input_stage2)

        # Predict CoalConsumption:
        input_stage1 = DATA_CTCN + DCS_Items
        input_stage1 = np.array(input_stage1).reshape(1, -1)
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

        # Truy vấn bảng "DATA_LN_OptimizerParameter" để lấy tên cột
        PG_cursor.execute('SELECT * FROM "DATA_LN_OptimizerParameter" LIMIT 1')
        name_columns = [desc[0] for desc in PG_cursor.description]

        # Tạo chuỗi cột và placeholders cho câu lệnh INSERT
        placeholders = ', '.join(['%s'] * len(name_columns))
        columns = ', '.join([f'"{col}"' for col in name_columns])

        # crontime = datetime.now().strftime('%Y-%m-%d %H:%M:00')
        values = [crontime] + [float(x) for x in input_COconsumption[0]] + [float(x*OptimizerRate) for x in OptimizerParameter_COConsumption]
        # print(values)
        insert_query = f'''
        INSERT INTO "DATA_LN_OptimizerParameter" ({columns}) VALUES ({placeholders})
        '''
        PG_cursor.execute(insert_query, values)
        PG_conn.commit() 

        # end_time = datetime.now()
        # print(f"Duration: {end_time - start_time}")
    except Exception as e:
        PG_conn.rollback()
        print(f"An error occurred: {e}")
        pass

def LH2_OptimizerParameter(PG_cursor, PG_conn, model_LH2_OptimizerParameter):
    """
        1. Workflow:
            Tối ưu hóa tham số vận hành LH2 dựa trên dữ liệu từ các bảng DATA_CTCN và DCS_Items.
            - Giai đoạn 1: Lấy thời gian của dữ liệu mới nhất hiện tại CronTime.
            - Giai đoạn 2: Query dữ liệu mới nhất về Chất lượng than mới nhất từ bảng DATA_CTCN
            - Giai đoạn 3: Query dữ liệu mới nhất về Công suất tải và Nhiệt độ nước cấp mới nhất từ bảng DCS_Items
            - Giai đoạn 4: Tạo dữ liệu đầu vào cho mô hình ML để tạo bộ thông số phù hợp với chất lượng than và Công suất đó
            - Giai đoạn 5: Tạo ngưỡng tối ưu dựa trên bộ thông số đó
            - Giai đoạn 6: Cấu hình GA và khởi tạo GA
            - Giai đoạn 7: Chạy hàm GA để có bộ thông số tối ưu tốt nhất
            - Giai đoạn 8: Kiểm tra xem tiêu hao đó có phải tốt nhất chưa.
            - Giai đoạn 9: Lưu dữ liệu vào database 
        
        2. Parameters:
            PG_cursor: Cursor để thực thi truy vấn SQL.
            PG_conn: Kết nối đến database PostgreSQL.
            crontime: Thời gian cho bộ dữ liệu mới nhất.
            model_LH2_OptimizerParameter: Mô hình ML dự đoán tham số tối ưu hóa ban đầu.
            param_bounds: Tạo ngưỡng tối ưu dựa trên bộ thông số đó
            best_solution: Bộ thông số sau khi tối ưu
            best_fitness: Tiêu hao tối ưu
            OptimizerParameter_CoalConsumption: Bộ thông số tối ưu mới nhất
    """
    try:
        print("Start LH2_OptimizerParameter")
        # Giai đoạn 1: Lấy thời gian của dữ liệu mới nhất hiện tại CronTime.
        query_crontime = '''
            SELECT "CronTime" FROM "DCS_Items" ORDER BY "CronTime" DESC LIMIT 1
            '''
        PG_cursor.execute(query_crontime)
        crontime = PG_cursor.fetchone()

        # Giai đoạn 2: Query dữ liệu mới nhất về chất lượng than mới nhất từ bảng DATA_CTCN
        query_DATA_CTCN = '''
            SELECT "LDA12080012000243", "LDA12080012000228", "LDA12080012000227", "LDA12080012000230",
            "LDA12080012000238", "LDA12080012000237", "LDA12080012000232", "LDA12080012000236",
            "LDA12080012000235", "LDA12080012000234", "LDA12080012000233" FROM "DATA_CTCN" ORDER BY "CronTime" DESC LIMIT 1
            '''
        PG_cursor.execute(query_DATA_CTCN)
        DATA_CTCN = PG_cursor.fetchone()
        DATA_CTCN = [float(value) for value in DATA_CTCN]
        # print(DATA_CTCN)

        # Giai đoạn 3: Query dữ liệu mới nhất về Công suất tải và Nhiệt độ nước cấp mới nhất từ bảng DCS_Items
        query_DCS_Items = '''
            SELECT "B2_FT1151_DACA_PV__Value", "B2_TE1251_DACA_PV__Value","B1_FT1151_DACA_PV__Value" FROM "DCS_Items" ORDER BY "CronTime" DESC LIMIT 1
            '''
        PG_cursor.execute(query_DCS_Items)
        DCS_Items = PG_cursor.fetchone()
        DCS_Items = [float(value) for value in DCS_Items]
        # print(DCS_Items)

        # Giai đoạn 4: Tạo dữ liệu đầu vào cho mô hình ML để tạo bộ thông số phù hợp với chất lượng than và Công suất đó
        global input_stage1
        input_stage1 = DATA_CTCN + DCS_Items
        input_stage1 = np.array(input_stage1).reshape(1, -1)
        OptimizerParameter_Stage1 = model_LH2_OptimizerParameter.predict(input_stage1)
        # print('OptimizerParameter_Stage1:', OptimizerParameter_Stage1[0])

        # Giai đoạn 5: Tạo ngưỡng tối ưu dựa trên bộ thông số đó. Có thể tăng giảm
        # rate_high = 0.015 # Điều chỉnh +1.5%
        # rate_low = 0.015 # Điều chỉnh -1.5%
        # param_bounds = []
        # for pred in OptimizerParameter_Stage1[0]:
        #     lower_bound = pred * (1 - rate_low)
        #     upper_bound = pred * (1 + rate_high)
        #     if lower_bound >= upper_bound:
        #         lower_bound, upper_bound = sorted([lower_bound, upper_bound]) 
        #     param_bounds.append([lower_bound, upper_bound])
        # param_bounds = np.array(param_bounds)
        rate_high = 0.015  # Điều chỉnh +1.5%
        rate_low = 0.015   # Điều chỉnh -1.5%

        # Đọc file baseparameter.json
        with open("../baseparameters/baseparameter_LH2.json", "r", encoding="utf-8") as f:
            base_params = json.load(f)

        # Chọn công suất cần dùng gan nhat
        power_value = DCS_Items[0]  
        available_keys = list(map(int, base_params.keys()))
        power_key = str(min(available_keys, key=lambda x: abs(x - power_value)))  

        params_list = base_params[power_key]

        # Tạo dict để tiện truy cập min/max theo tag
        param_dict = {p["tag"]: {"min": p["min"], "max": p["max"]} for p in params_list}

        # Giả sử bạn có list columns_LH1 (tên tham số theo đúng thứ tự model output)
        columns_LH2 = [
            'B2_Z_BEDT_DACA_PV__Value', 'B2_PT1281_DACA_PV__Value',
            'B2_AT1011_DACA_PV__Value', 'B2_AT1012_DACA_PV__Value',
            'B2_TE1212_DACA_PV__Value', 'B2_PT1061_DACA_PV__Value',
            'B2_PT1071_DACA_PV__Value', 'B2_PT1111_DACA_PV__Value',
            'B2_PT1112_DACA_PV__Value', 'B2_PT1211_DACA_PV__Value',
            'B2_PT1212_DACA_PV__Value', 'B2_TZ1131ZT_DACA_PV__Value',
            'B2_S051AIT_DACA_PV__Value', 'B2_AZ1011ZT_DACA_PV__Value',
            'B2_S052AIT_DACA_PV__Value', 'B2_S052AVFD_CRT_DACA_PV__Value',
            'B2_S052AVFD_FB_DACA_PV__Value', 'B2_PT1081_DACA_PV__Value',
            'B2_PT1082_DACA_PV__Value', 'B2_PT1091_DACA_PV__Value',
            'B2_PT1092_DACA_PV__Value', 'B2_TE1111_DACA_PV__Value',
            'B2_TE1112_DACA_PV__Value']
        
        param_min = np.array([param_dict[tag]["min"] for tag in columns_LH2])
        param_max = np.array([param_dict[tag]["max"] for tag in columns_LH2])

        # Tạo ngưỡng
        param_bounds = []
        for i, pred in enumerate(OptimizerParameter_Stage1[0]):
            lower_bound = pred * (1 - rate_low)
            upper_bound = pred * (1 + rate_high)

            lower_bound = max(lower_bound, param_min[i])
            upper_bound = min(upper_bound, param_max[i])

            if lower_bound >= upper_bound:
                lower_bound, upper_bound = param_min[i], param_max[i]

            param_bounds.append([lower_bound, upper_bound])

        param_bounds = np.array(param_bounds)
        print("param_bounds:", param_bounds)

        # Giai đoạn 6: Cấu hình GA và khởi tạo GA
        algorithm_params = {
            'max_num_iteration': 1000,    # Tăng số thế hệ để cải thiện khả năng tìm kiếm giải pháp tốt hơn
            'population_size': 30,        # Tăng kích thước quần thể để đa dạng hóa gen, tránh kẹt ở cực trị địa phương
            'mutation_probability': 0.2,  # Giảm xác suất đột biến để duy trì sự ổn định nhưng vẫn đảm bảo khám phá không gian
            'elit_ratio': 0.1,            # Tăng tỷ lệ cá thể ưu tú để giữ lại nhiều giải pháp tốt hơn qua các thế hệ
            # 'crossover_probability': 0.8, # Tăng xác suất lai ghép để đẩy mạnh sự kết hợp gen tốt
            'parents_portion': 0.5,       # Tăng tỷ lệ chọn làm cha mẹ để đảm bảo nhiều nguồn gen tốt được kết hợp
            'crossover_type': 'one_point', # Chuyển sang lai ghép điểm đơn để tăng tính đột phá khi kết hợp gen
            'max_iteration_without_improv': 30, # Tăng ngưỡng dừng để tránh kết luận sớm khi mô hình chưa tối ưu
        }
        model = ga(
            dimension=len(OptimizerParameter_Stage1[0]),
            variable_type='real',
            variable_boundaries=param_bounds,
            algorithm_parameters=algorithm_params
        )

        # Giai đoạn 7: Chạy hàm GA để có bộ thông số tối ưu tốt nhất
        model.run(function=objective_function_LH2, no_plot = True, disable_printing=True, progress_bar_stream=None)
        best_solution = model.result['variable']
        best_fitness = model.result['score']/(input_stage1[0][11] + 1e-10)
        # print(f"Best Parameters: {best_solution}")
        print(f"Best Fitness: {best_fitness}")

        # Giai đoạn 8: Kiểm tra xem tiêu hao đó có phải tốt nhất chưa. Nếu thấp hơn thì sẽ lấy bộ thông số đó, không thì sẽ lấy bộ thông số cũ
        query_CoalConsumption = '''
            SELECT * FROM "DATA_LH2_OptimizerParameter" ORDER BY "CronTime" DESC LIMIT 1
            '''
        PG_cursor.execute(query_CoalConsumption)
        OptimizerParameter_CoalConsumption = PG_cursor.fetchone()
        OptimizerParameter_CoalConsumption = [float(value) for value in OptimizerParameter_CoalConsumption[1:]]
        # target_times = ["06:00:00", "14:00:00", "22:00:00","06:01:00", "14:01:00", "22:01:00"]
        target_times = target_times_function()
        cron_datetime = crontime[0]
            # Điều kiện Reset bộ thông số vào lúc giao ca 6h 14h 22h hoặc Công suất chênh lệch 5 tấn/h
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
            values = [crontime] + [float(x) for x in input_stage1[0]] + [float(x) for x in DCS] + [0]
        else:
            if cron_datetime.strftime("%H:%M:%S") in target_times or abs(DCS_Items[0] - OptimizerParameter_CoalConsumption[11]) >= 2:
                values = [crontime] + [float(x) for x in input_stage1[0]] + [float(x) for x in best_solution] + [float(best_fitness)]
            else:
                if best_fitness > OptimizerParameter_CoalConsumption[-1]:
                    # print(True)
                    input_coalconsumption = OptimizerParameter_CoalConsumption[:-1]
                    OptimizerParameter_CoalConsumption = OptimizerParameter_CoalConsumption[-1]
                    if isinstance(input_coalconsumption, float):
                        input_coalconsumption = [input_coalconsumption]
                    values = [crontime] + list(input_coalconsumption) + [OptimizerParameter_CoalConsumption]
                else:
                    values = [crontime] + [float(x) for x in input_stage1[0]] + [float(x) for x in best_solution] + [float(best_fitness)]

        # Giai đoạn 9: Lưu dữ liệu vào database 
            # Truy vấn bảng "DATA_LH2_OptimizerParameter" để lấy tên cột
        PG_cursor.execute('SELECT * FROM "DATA_LH2_OptimizerParameter" LIMIT 1')
        name_columns = [desc[0] for desc in PG_cursor.description]
            # Tạo chuỗi cột và placeholders cho câu lệnh INSERT
        placeholders = ', '.join(['%s'] * len(name_columns))
        columns = ', '.join([f'"{col}"' for col in name_columns])
        insert_query = f'''
            INSERT INTO "DATA_LH2_OptimizerParameter" ({columns}) VALUES ({placeholders})
            '''
        PG_cursor.execute(insert_query, values)
        PG_conn.commit() 
    except Exception as e:
        PG_conn.rollback()
        print(f"An error occurred: {e}")
        pass

def LH1_OptimizerParameter(PG_cursor, PG_conn, model_LH1_OptimizerParameter):
    """
        1. Workflow:
            Tối ưu hóa tham số vận hành LH2 dựa trên dữ liệu từ các bảng DATA_CTCN và DCS_Items.
            - Giai đoạn 1: Lấy thời gian của dữ liệu mới nhất hiện tại CronTime.
            - Giai đoạn 2: Query dữ liệu mới nhất về Chất lượng than mới nhất từ bảng DATA_CTCN
            - Giai đoạn 3: Query dữ liệu mới nhất về Công suất tải và Nhiệt độ nước cấp mới nhất từ bảng DCS_Items
            - Giai đoạn 4: Tạo dữ liệu đầu vào cho mô hình ML để tạo bộ thông số phù hợp với chất lượng than và Công suất đó
            - Giai đoạn 5: Tạo ngưỡng tối ưu dựa trên bộ thông số đó
            - Giai đoạn 6: Cấu hình GA và khởi tạo GA
            - Giai đoạn 7: Chạy hàm GA để có bộ thông số tối ưu tốt nhất
            - Giai đoạn 8: Kiểm tra xem tiêu hao đó có phải tốt nhất chưa.
            - Giai đoạn 9: Lưu dữ liệu vào database 
        
        2. Parameters:
            PG_cursor: Cursor để thực thi truy vấn SQL.
            PG_conn: Kết nối đến database PostgreSQL.
            crontime: Thời gian cho bộ dữ liệu mới nhất.
            model_LH1_OptimizerParameter: Mô hình ML dự đoán tham số tối ưu hóa ban đầu.
            param_bounds: Tạo ngưỡng tối ưu dựa trên bộ thông số đó
            best_solution: Bộ thông số sau khi tối ưu
            best_fitness: Tiêu hao tối ưu
            OptimizerParameter_CoalConsumption: Bộ thông số tối ưu mới nhất
    """
    try:
        print("Start LH1_OptimizerParameter")
        # Giai đoạn 1: Lấy thời gian của dữ liệu mới nhất hiện tại CronTime.
        query_crontime = '''
            SELECT "CronTime" FROM "DCS_Items" ORDER BY "CronTime" DESC LIMIT 1
            '''
        PG_cursor.execute(query_crontime)
        crontime = PG_cursor.fetchone()
        
        # Giai đoạn 2: Query dữ liệu mới nhất về Chất lượng than mới nhất từ bảng DATA_CTCN
        query_DATA_CTCN = '''
            SELECT "LDA12080012000243", "LDA12080012000228", "LDA12080012000227", "LDA12080012000230",
            "LDA12080012000238", "LDA12080012000237", "LDA12080012000232", "LDA12080012000236",
            "LDA12080012000235", "LDA12080012000234", "LDA12080012000233" FROM "DATA_CTCN" ORDER BY "CronTime" DESC LIMIT 1
            '''
        PG_cursor.execute(query_DATA_CTCN)
        DATA_CTCN = PG_cursor.fetchone()
        DATA_CTCN = [float(value) for value in DATA_CTCN]
        # print(DATA_CTCN)

        # Giai đoạn 3: Query dữ liệu mới nhất về Công suất tải và Nhiệt độ nước cấp mới nhất từ bảng DCS_Items
        query_DCS_Items = '''SELECT "B1_FT1151_DACA_PV__Value", "B1_TE1251_DACA_PV__Value","B2_FT1151_DACA_PV__Value" FROM "DCS_Items" ORDER BY "CronTime" DESC LIMIT 1'''
        PG_cursor.execute(query_DCS_Items)
        DCS_Items = PG_cursor.fetchone()
        DCS_Items = [float(value) for value in DCS_Items]

        # Giai đoạn 4: Tạo dữ liệu đầu vào cho mô hình ML để tạo bộ thông số phù hợp với chất lượng than và Công suất đó
        global input_stage1
        input_stage1 = DATA_CTCN + DCS_Items
        input_stage1 = np.array(input_stage1).reshape(1, -1)
        OptimizerParameter_Stage1 = model_LH1_OptimizerParameter.predict(input_stage1)
        # print('OptimizerParameter_Stage1:', OptimizerParameter_Stage1[0])

        # Giai đoạn 5: Tạo ngưỡng tối ưu dựa trên bộ thông số đó
        # rate_high = 0.015 # Điều chỉnh +1.5%
        # rate_low = 0.015 # Điều chỉnh -1.5%
        # param_bounds = []
        # for pred in OptimizerParameter_Stage1[0]:
        #     lower_bound = pred * (1 - rate_low)
        #     upper_bound = pred * (1 + rate_high)
        #     if lower_bound >= upper_bound:
        #         lower_bound, upper_bound = sorted([lower_bound, upper_bound]) 
        #     param_bounds.append([lower_bound, upper_bound])
        # param_bounds = np.array(param_bounds)
        rate_high = 0.015  # Điều chỉnh +1.5%
        rate_low = 0.015   # Điều chỉnh -1.5%

        # Đọc file baseparameter.json
        with open("../baseparameters/baseparameter_LH1.json", "r", encoding="utf-8") as f:
            base_params = json.load(f)

        # Chọn công suất cần dùng gan nhat
        power_value = DCS_Items[0]  
        available_keys = list(map(int, base_params.keys()))
        power_key = str(min(available_keys, key=lambda x: abs(x - power_value)))  

        params_list = base_params[power_key]

        # Tạo dict để tiện truy cập min/max theo tag
        param_dict = {p["tag"]: {"min": p["min"], "max": p["max"]} for p in params_list}

        # Giả sử bạn có list columns_LH1 (tên tham số theo đúng thứ tự model output)
        columns_LH1 = [
            'B1_Z_BEDT_DACA_PV__Value', 'B1_PT1281_DACA_PV__Value',
            'B1_AT1011_DACA_PV__Value', 'B1_AT1012_DACA_PV__Value',
            'B1_TE1212_DACA_PV__Value', 'B1_PT1061_DACA_PV__Value',
            'B1_PT1071_DACA_PV__Value', 'B1_PT1111_DACA_PV__Value',
            'B1_PT1112_DACA_PV__Value', 'B1_PT1211_DACA_PV__Value',
            'B1_PT1212_DACA_PV__Value', 'B1_TZ1131ZT_DACA_PV__Value',
            'B1_S051AIT_DACA_PV__Value', 'B1_AZ1011ZT_DACA_PV__Value',
            'B1_S052AIT_DACA_PV__Value', 'B1_S052AVFD_CRT_DACA_PV__Value',
            'B1_S052AVFD_FB_DACA_PV__Value', 'B1_PT1081_DACA_PV__Value',
            'B1_PT1082_DACA_PV__Value', 'B1_PT1091_DACA_PV__Value',
            'B1_PT1092_DACA_PV__Value', 'B1_TE1111_DACA_PV__Value',
            'B1_TE1112_DACA_PV__Value']
        
        param_min = np.array([param_dict[tag]["min"] for tag in columns_LH1])
        param_max = np.array([param_dict[tag]["max"] for tag in columns_LH1])

        # Tạo ngưỡng
        param_bounds = []
        for i, pred in enumerate(OptimizerParameter_Stage1[0]):
            lower_bound = pred * (1 - rate_low)
            upper_bound = pred * (1 + rate_high)

            # if lower_bound >= upper_bound:
            #     lower_bound, upper_bound = sorted([lower_bound, upper_bound])

            lower_bound = max(lower_bound, param_min[i])
            upper_bound = min(upper_bound, param_max[i])

            if lower_bound >= upper_bound:
                lower_bound, upper_bound = param_min[i], param_max[i]

            param_bounds.append([lower_bound, upper_bound])

        param_bounds = np.array(param_bounds)
        print("param_bounds:", param_bounds)

        # Giai đoạn 6: Cấu hình GA và khởi tạo GA
        algorithm_params = {
            'max_num_iteration': 1000,    # Tăng số thế hệ để cải thiện khả năng tìm kiếm giải pháp tốt hơn
            'population_size': 20,        # Tăng kích thước quần thể để đa dạng hóa gen, tránh kẹt ở cực trị địa phương
            'mutation_probability': 0.2,  # Giảm xác suất đột biến để duy trì sự ổn định nhưng vẫn đảm bảo khám phá không gian
            'elit_ratio': 0.1,            # Tăng tỷ lệ cá thể ưu tú để giữ lại nhiều giải pháp tốt hơn qua các thế hệ
            # 'crossover_probability': 0.8, # Tăng xác suất lai ghép để đẩy mạnh sự kết hợp gen tốt
            'parents_portion': 0.5,       # Tăng tỷ lệ chọn làm cha mẹ để đảm bảo nhiều nguồn gen tốt được kết hợp
            'crossover_type': 'one_point', # Chuyển sang lai ghép điểm đơn để tăng tính đột phá khi kết hợp gen
            'max_iteration_without_improv': 30, # Tăng ngưỡng dừng để tránh kết luận sớm khi mô hình chưa tối ưu
        }
        model = ga(
            dimension=len(OptimizerParameter_Stage1[0]),
            variable_type='real',
            variable_boundaries=param_bounds,
            algorithm_parameters=algorithm_params
        )

        # Giai đoạn 7: Chạy hàm GA để có bộ thông số tối ưu tốt nhất
        model.run(function=objective_function_LH1, no_plot = True, disable_printing=True, progress_bar_stream=None)
        best_solution = model.result['variable']
        best_fitness = model.result['score']/(input_stage1[0][11] + 1e-10)
        # print(f"Best Parameters: {best_solution}")
        print(f"Best Fitness: {best_fitness}")

        # Giai đoạn 8: Kiểm tra xem tiêu hao đó có phải tốt nhất chưa.
        query_CoalConsumption = '''SELECT * FROM "DATA_LH1_OptimizerParameter" ORDER BY "CronTime" DESC LIMIT 1'''
        PG_cursor.execute(query_CoalConsumption)
        OptimizerParameter_CoalConsumption = PG_cursor.fetchone()
        OptimizerParameter_CoalConsumption = [float(value) for value in OptimizerParameter_CoalConsumption[1:]]
        # target_times = ["06:00:00", "14:00:00", "22:00:00","06:01:00", "14:01:00", "22:01:00"]
        target_times = target_times_function()
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
            values = [crontime] + [float(x) for x in input_stage1[0]] + [float(x) for x in DCS] + [0]
        else:
            if cron_datetime.strftime("%H:%M:%S") in target_times or abs(DCS_Items[0] - OptimizerParameter_CoalConsumption[11]) >= 2:
                values = [crontime] + [float(x) for x in input_stage1[0]] + [float(x) for x in best_solution] + [float(best_fitness)]
            else:
                if best_fitness > OptimizerParameter_CoalConsumption[-1]:
                    input_coalconsumption = OptimizerParameter_CoalConsumption[:-1]
                    OptimizerParameter_CoalConsumption = OptimizerParameter_CoalConsumption[-1]
                    if isinstance(input_coalconsumption, float):
                        input_coalconsumption = [input_coalconsumption]
                    values = [crontime] + list(input_coalconsumption) + [OptimizerParameter_CoalConsumption]
                else:
                    values = [crontime] + [float(x) for x in input_stage1[0]] + [float(x) for x in best_solution] + [float(best_fitness)]
        
        # Giai đoạn 9: Lưu dữ liệu vào database 
            # Truy vấn bảng "DATA_LH1_OptimizerParameter" để lấy tên cột
        PG_cursor.execute('SELECT * FROM "DATA_LH1_OptimizerParameter" LIMIT 1')
        name_columns = [desc[0] for desc in PG_cursor.description]

            # Tạo chuỗi cột và placeholders cho câu lệnh INSERT
        placeholders = ', '.join(['%s'] * len(name_columns))
        columns = ', '.join([f'"{col}"' for col in name_columns])
        insert_query = f'''
            INSERT INTO "DATA_LH1_OptimizerParameter" ({columns}) VALUES ({placeholders})
            '''
        PG_cursor.execute(insert_query, values)
        PG_conn.commit() 
    except Exception as e:
        PG_conn.rollback()
        print(f"An error occurred: {e}")
        pass