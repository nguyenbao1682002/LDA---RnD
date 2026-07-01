from geneticalgorithm2 import geneticalgorithm2 as ga
import numpy as np
import warnings
from sklearn.exceptions import InconsistentVersionWarning
import pickle
warnings.filterwarnings("ignore", message=".*does not have valid feature names.*")
warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

# Hàm mục tiêu
def objective_function(X):
    X_sample = np.array([
        7.90935833e+00, 6.34340846e+00, 2.85660873e+01, 5.94713854e+03,
        1.98885402e+01, 3.56498297e+01, 8.07381821e-01, 1.80021469e+01,
        1.47019277e+01, 9.62603549e+00, 1.32414671e+00, 88, 160, 90
    ]).reshape(1, -1)

    X = X.reshape(1, -1)
    input = np.concatenate((X_sample, X), axis=1)
    with open('D:/001.Project/LDA_master/autotrain/best/LH_modelOptimizerParameter_CoalConsumption_best.sav', 'rb') as file:
        loaded_model = pickle.load(file)
    target = loaded_model.predict(input)
    target = target.item()
    return target

def GA():

    # Giới hạn tham số
    prediction = [919.65052863,   4.85783073,   5.44505379,   3.7680271,  443.49258168,
      8.37573576,   8.35691288, 320.42093672, 237.8896149,    5.6223664,
      35.6285846,   37.98631245,  57.81989222,  99.76675955,   3.90354244,
      22.38410475,  17.52999337,  30.61334483,  30.70673682,  30.20266311,
      30.26147073, 162.15625889, 149.33635326]

    rate = 0.01 # Điều chỉnh +-1%

    param_bounds = np.array([
        [prediction[0]*(1-rate), prediction[0]*(1+rate)],
        [prediction[1]*(1-rate), prediction[1]*(1+rate)],
        [prediction[2]*(1-rate), prediction[2]*(1+rate)],
        [prediction[3]*(1-rate), prediction[3]*(1+rate)],
        [prediction[4]*(1-rate), prediction[4]*(1+rate)],
        [prediction[5]*(1-rate), prediction[5]*(1+rate)],
        [prediction[6]*(1-rate), prediction[6]*(1+rate)],
        [prediction[7]*(1-rate), prediction[7]*(1+rate)],
        [prediction[8]*(1-rate), prediction[8]*(1+rate)],
        [prediction[9]*(1-rate), prediction[9]*(1+rate)],
        [prediction[10]*(1-rate), prediction[10]*(1+rate)],
        [prediction[11]*(1-rate), prediction[11]*(1+rate)],
        [prediction[12]*(1-rate), prediction[12]*(1+rate)],
        [prediction[13]*(1-rate), prediction[13]*(1+rate)],
        [prediction[14]*(1-rate), prediction[14]*(1+rate)],
        [prediction[15]*(1-rate), prediction[15]*(1+rate)],
        [prediction[16]*(1-rate), prediction[16]*(1+rate)],
        [prediction[17]*(1-rate), prediction[17]*(1+rate)],
        [prediction[18]*(1-rate), prediction[18]*(1+rate)],
        [prediction[19]*(1-rate), prediction[19]*(1+rate)],
        [prediction[20]*(1-rate), prediction[20]*(1+rate)],
        [prediction[21]*(1-rate), prediction[21]*(1+rate)],
        [prediction[22]*(1-rate), prediction[22]*(1+rate)]])

    # Cấu hình GA
    algorithm_params = {
        'max_num_iteration': 500,    # Số thế hệ tối đa
        'population_size': 20,       # Kích thước quần thể
        'mutation_probability': 0.2, # Xác suất đột biến
        'elit_ratio': 0.05,          # Tỷ lệ cá thể tốt nhất giữ lại
        'crossover_probability': 0.5,# Xác suất lai ghép
        'parents_portion': 0.3,      # Tỷ lệ chọn làm cha mẹ
        'crossover_type': 'uniform', # Kiểu lai ghép (uniform, single_point, ...)
        'max_iteration_without_improv': 10, # Dừng nếu không cải thiện
    }
    
    # Khởi tạo GA
    model = ga(
        function=objective_function,
        dimension=len(prediction),
        variable_type='real',
        variable_boundaries=param_bounds,
        algorithm_parameters=algorithm_params
    )

    # Chạy GA
    model.run(no_plot = True)

    # Kết quả tốt nhất
    best_solution = model.output_dict['variable']
    best_fitness = model.output_dict['function']
    print(f"Best Parameters: {best_solution}")
    print(f"Best Fitness: {best_fitness}")
    return best_solution, best_fitness

# best_solution, best_fitness = GA()