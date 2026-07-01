from dotenv import load_dotenv
import os
import psycopg2
import schedule
from getdataXHQ import *
from OptimizerParameter import load_model, LH1_OptimizerParameter, LH2_OptimizerParameter, LN_OptimizerParameter
from HistoryParameter import LH1_HistoryParameter, LH2_HistoryParameter
from GenerateParameter import LH1_GenerateParameter, LH2_GenerateParameter, LN_GenerateParameter
from ModelEvaluation import LH1_Evaluation, LH2_Evaluation, LN_Evaluation
from ErrorWarning import LN_ErrorWarning
from AutoRetrainingModels import LH1_AutoRetrainingModel, LH2_AutoRetrainingModel, LN_AutoRetrainingModel
from EPortal_OptimizerParameter import LN_EPortal
from EPortal_GenerateParameter import *
from Forecasting import *
import time
import pyodbc
from fastapi import FastAPI
import uvicorn
import threading
import warnings
from pydantic import BaseModel
from GA2 import *
from Forecasting_ARORSL import *

warnings.filterwarnings("ignore", message=".*does not have valid feature names.*")

# Config
app = FastAPI()

load_dotenv(dotenv_path="../.env",override=True)

# Database Connections Config
PG_host = os.getenv("PG_HOST")
PG_port = os.getenv("PG_PORT")
PG_database = os.getenv("PG_DATABASE")
PG_username = os.getenv("PG_USERNAME")
PG_password = os.getenv("PG_PASSWORD")
PG_conn = psycopg2.connect(
    host=PG_host,
    port=PG_port,
    database=PG_database,
    user=PG_username,
    password=PG_password
)
PG_cursor = PG_conn.cursor()

XHQ_server = os.getenv("XHQ_SERVER")
XHQ_database = os.getenv("XHQ_DATABASE")
XHQ_username = os.getenv("XHQ_USERNAME")
XHQ_password = os.getenv("XHQ_PASSWORD")
XHQ_conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={XHQ_server};DATABASE={XHQ_database};UID={XHQ_username};PWD={XHQ_password}')
XHQ_cursor = XHQ_conn.cursor()

    # LoHoi1============================
    # Path models
        # Global: RandomForestRegression Models
path_LH1_OptimizerParameter = 'D:/001.Project/LDA_master/models/LH1_Step1_0703.sav'
path_LH1_GenerateParameter = 'D:/001.Project/LDA_master/models/LH1_Step1_0703.sav'
# path_LH1_CoalConsumption = 'D:/001.Project/LDA_master/models/LH_Step2.sav'
# path_LH1_CoalConsumption = 'D:/001.Project/LDA_master/models/LH1_RandomForestRegressor.sav'
# path_LH1_CoalConsumption = 'D:/001.Project/LDA_master/autotrain/best/LH_modelOptimizerParameter_CoalConsumption_best.sav'

        # Local: KNN Models (k=1 is nearest values)
# path_LH1_HistoryParameter = 'D:/001.Project/LDA_master/models/LH_modelHistoryParameter_2025.sav'
# path_LH1_HistoryParameter = 'D:/001.Project/LDA_master/models/LH1_modelHistoryParameter_112025.sav'
# path_LH1_HistoryParameter = 'D:/001.Project/LDA_master/models/LH1_knn_model_0703.sav'
# path_LH1_HistoryParameter = 'D:/001.Project/LDA_master/autotrain/best/LH1_History_best.sav'
path_LH1_HistoryParameter = 'D:/001.Project/LDA_master/models/LH1_ZML_Local_2025.sav'
    # Models:
        # Global: RandomForestRegression Models
model_LH1_OptimizerParameter = load_model(path_LH1_OptimizerParameter)
model_LH1_GenerateParameter = load_model(path_LH1_GenerateParameter)
# model_LH1_CoalConsumption = load_model(path_LH1_CoalConsumption)
        # Local: KNN Models (k=1 is nearest values)
model_LH1_HistoryParameter = load_model(path_LH1_HistoryParameter)

# LoHoi2============================
    # Path models
        # Global: RandomForestRegression Models
path_LH2_OptimizerParameter = 'D:/001.Project/LDA_master/models/LH2_Step1_0703.sav'
# path_LH2_OptimizerParameter = 'D:/001.Project/LDA_master/autotrain/best/LH2_Optimizer_best.sav'
path_LH2_GenerateParameter = 'D:/001.Project/LDA_master/models/LH2_Step1_0703.sav'
# path_LH2_GenerateParameter = 'D:/001.Project/LDA_master/autotrain/best/LH2_Optimizer_best.sav'
# path_LH2_CoalConsumption = 'D:/001.Project/LDA_master/models/LH_Step2.sav'
# path_LH2_CoalConsumption = 'D:/001.Project/LDA_master/autotrain/best/LH_modelOptimizerParameter_CoalConsumption_best.sav'
        # Local: KNN Models (k=1 is nearest values)
# path_LH2_HistoryParameter = 'D:/001.Project/LDA_master/models/LH2_knn_model_0703.sav'
# path_LH2_HistoryParameter = 'D:/001.Project/LDA_master/models/LH1_modelHistoryParameter_112025.sav'
# path_LH2_HistoryParameter = 'D:/001.Project/LDA_master/autotrain/best/LH2_History_best.sav'
path_LH2_HistoryParameter = 'D:/001.Project/LDA_master/models/LH2_ZML_Local_2025.sav'
    # Models:
        # Global: RandomForestRegression Models
model_LH2_OptimizerParameter = load_model(path_LH2_OptimizerParameter)
model_LH2_GenerateParameter = load_model(path_LH2_GenerateParameter)
# model_LH2_CoalConsumption = load_model(path_LH2_CoalConsumption)
        # Local: KNN Models (k=1 is nearest values)
model_LH2_HistoryParameter = load_model(path_LH2_HistoryParameter)
    
    # Model Forcasting 
path_LH_Forcasting = 'D:/001.Project/LDA_master/models/LH_Predict5M.sav'
model_LH_Forecasting = load_model(path_LH_Forcasting)

path_LN_modelForcasting = 'D:/001.Project/LDA_master/models/LN_Forecasting.sav'
model_LN_Forecasting = load_model(path_LN_modelForcasting)

# LoNung============================
# Path models
path_LN_modelOptimizerParameter_Stage1 = 'D:/001.Project/LDA_master/autotrain/best/LN_modelOptimizerParameter_Stage1_best.sav'
path_LN_modelOptimizerParameter_Stage2 = 'D:/001.Project/LDA_master/autotrain/best/LN_modelOptimizerParameter_Stage2_best.sav'
path_LN_modelOptimizerParameter_COconsumption = 'D:/001.Project/LDA_master/autotrain/best/LN_modelOptimizerParameter_COconsumption_best.sav'
# Models:
    # Global: RandomForestRegression Models
model_LN_OptimizerParameter_Stage1 = load_model(path_LN_modelOptimizerParameter_Stage1)
model_LN_OptimizerParameter_Stage2 = load_model(path_LN_modelOptimizerParameter_Stage2)
model_LN_OptimizerParameter_COconsumption = load_model(path_LN_modelOptimizerParameter_COconsumption)

path_LN_EPortal = 'D:/001.Project/LDA_master/models/LoNung.sav'
path_LN_EPortal_COconsumption = 'D:/001.Project/LDA_master/models/LoNung_tieuhao.sav'
path_LN_EPortal_Nhietkhoithai = 'D:/001.Project/LDA_master/models/LoNung_nhietkhoithai.sav'
model_LN_EPortal = load_model(path_LN_EPortal)
model_LN_EPortal_COconsumption = load_model(path_LN_EPortal_COconsumption)
model_LN_EPortal_Nhietkhoithai = load_model(path_LN_EPortal_Nhietkhoithai)

def backup_database():
    os.system("docker-compose -f D:/001.Project/LDA_master/docker-compose.yaml exec postgres pg_dump -U LDA LDA > D:/001.Project/LDA_master/backup/database/backup.sql")

# from concurrent.futures import ThreadPoolExecutor
# executor = ThreadPoolExecutor(max_workers=10)  # max 10 job đồng thời
# def run_threaded(job_func):
#     executor.submit(job_func)

schedule.every(1).minutes.do(lambda: getdataXHQ_DATA_CTCN(PG_cursor, XHQ_cursor,PG_conn))
schedule.every(1).minutes.do(lambda: getdataXHQ_DCS_Items(PG_cursor, XHQ_cursor,PG_conn))

schedule.every(1).minutes.do(lambda: LH1_OptimizerParameter(PG_cursor, PG_conn, model_LH1_OptimizerParameter))
schedule.every(1).minutes.do(lambda: LH1_HistoryParameter(PG_cursor, PG_conn, model_LH1_HistoryParameter))

schedule.every(1).minutes.do(lambda: LH2_OptimizerParameter(PG_cursor, PG_conn, model_LH2_OptimizerParameter))
schedule.every(1).minutes.do(lambda: LH2_HistoryParameter(PG_cursor, PG_conn, model_LH2_HistoryParameter))

schedule.every(1).minutes.do(lambda: LN_OptimizerParameter(PG_cursor, PG_conn, model_LN_OptimizerParameter_Stage1, model_LN_OptimizerParameter_Stage2, model_LN_OptimizerParameter_COconsumption))
schedule.every(1).minutes.do(lambda: LN_ErrorWarning(PG_cursor, PG_conn))
schedule.every(1).minutes.do(lambda: LN_Evaluation(PG_cursor, PG_conn))

schedule.every(1).minutes.do(lambda: LH1_Evaluation(PG_cursor, PG_conn))
schedule.every(1).minutes.do(lambda: LH2_Evaluation(PG_cursor, PG_conn))
# schedule.every(1).minutes.do(lambda: LH1_Forecasting(PG_cursor, PG_conn, model_LH_Forecasting))
# schedule.every(1).minutes.do(lambda: LH2_Forecasting(PG_cursor, PG_conn, model_LH_Forecasting))
schedule.every(1).minutes.do(lambda: LH1_Forecasting_ARORSL(PG_cursor, PG_conn, "../models_rls"))
schedule.every(1).minutes.do(lambda: LH2_Forecasting_ARORSL(PG_cursor, PG_conn, "../models_rls"))

# schedule.every(1).minutes.do(lambda: LN_Forecasting(PG_cursor, PG_conn, model_LN_Forecasting))
schedule.every(1).minutes.do(lambda: LN_Forecasting_ARORSL(PG_cursor, PG_conn, model_dir="../models_rls"))
schedule.every(1).minutes.do(lambda: LN_EPortal(PG_cursor, PG_conn, model_LN_EPortal, model_LN_EPortal_COconsumption))
# schedule.every(1).minutes.do(lambda: run_threaded(lambda: LN_EPortal(PG_cursor, PG_conn, model_LN_EPortal)))

schedule.every().day.at("00:01").do(lambda: LH1_AutoRetrainingModel(PG_cursor))
schedule.every().day.at("00:01").do(lambda: LH2_AutoRetrainingModel(PG_cursor))
schedule.every().day.at("00:01").do(lambda: LN_AutoRetrainingModel(PG_cursor))
schedule.every().day.at("00:01").do(backup_database)

# Function to run the scheduler
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()

class InputLH1(BaseModel):
    CronTime: datetime
    LDA12080012000243: float
    LDA12080012000228: float
    LDA12080012000227: float
    LDA12080012000230: float
    LDA12080012000238: float
    LDA12080012000237: float
    LDA12080012000232: float
    LDA12080012000236: float
    LDA12080012000235: float
    LDA12080012000234: float
    LDA12080012000233: float
    B1_FT1151_DACA_PV__Value: float
    B1_TE1251_DACA_PV__Value: float
    B2_FT1151_DACA_PV__Value: float

class InputLH2(BaseModel):
    CronTime: datetime
    LDA12080012000243: float
    LDA12080012000228: float
    LDA12080012000227: float
    LDA12080012000230: float
    LDA12080012000238: float
    LDA12080012000237: float
    LDA12080012000232: float
    LDA12080012000236: float
    LDA12080012000235: float
    LDA12080012000234: float
    LDA12080012000233: float
    B2_FT1151_DACA_PV__Value: float
    B2_TE1251_DACA_PV__Value: float
    B1_FT1151_DACA_PV__Value: float

class InputLN(BaseModel):
    CronTime: datetime
    LDA11070012000630: float
    LDA07060012000122: float
    LDA07060012000155: float 
    LDA07060012000156: float 
    LDA07060012000157: float
    LDA07060012000158: float 
    LDA07060012000159: float 
    LDA07060012000160: float
    LDA07060012000161: float 
    LDA07060012000162: float 
    LDA07060012000163: float
    LDA07060012000164: float 
    LDA07060012000165: float 
    LDA07060012000166: float
    CM_A181_V19_COM_V19_IN_5_PV3__Value: float 
    CM_A181FT0010_DACA_PV__Value: float
    CM_A181FT0001_DACA_PV__Value: float
    CM_A181PT0013_DACA_PV__Value: float 
    CM_A181AT0001_DACA_PV__Value: float
    CM_A181PT0002_DACA_PV__Value: float 
    CM_A181PT0003_DACA_PV__Value: float
    CM_A181PT0004_DACA_PV__Value: float 
    CM_A181PDT0002_DACA_PV__Value: float
    CM_A181PT0005_DACA_PV__Value: float 
    CM_A181PT0006_DACA_PV__Value: float
    CM_A181PT0007_DACA_PV__Value: float 
    CM_A181PT0008_DACA_PV__Value: float
    CM_A181TE0007_DACA_PV__Value: float 
    CM_A181S015BPGPV_DACA_PV__Value: float
    CM_A181_TIEUHAOCO_OUT__Value: float

# API:
@app.post("/API_LH1_GenerateParameter")
def API_LH1_GenerateParameter(input: InputLH1):
    input = list(input.dict().values())
    input = input[1:]
    # print(input)
    output = LH1_GenerateParameter(input, PG_cursor, PG_conn, model_LH1_GenerateParameter)
    return output

@app.post("/API_LH2_GenerateParameter")
def API_LH2_GenerateParameter(input: InputLH2):
    input = list(input.dict().values())
    input = input[1:]
    # print(input)
    output = LH2_GenerateParameter(input, PG_cursor, PG_conn, model_LH2_GenerateParameter)
    return output

@app.post("/API_LN_GenerateParameter")
def API_LN_GenerateParameter(input: InputLN):
    input = list(input.dict().values())
    input = input[1:]
    crontime = input[0]
    # print(input)
    output = LN_GenerateParameter(crontime, input, PG_cursor, PG_conn, model_LN_OptimizerParameter_Stage1, model_LN_OptimizerParameter_Stage2, model_LN_OptimizerParameter_COconsumption)
    return output

class InputLN_EPortal(BaseModel):
    CronTime: datetime
    LDA07060012000157: float
    LDA07060012000158: float
    LDA07060012000166: float    
    LDA11070012000630: float
    CM_A181FT0001_DACA_PV__Value: float 
    CM_A181PT0013_DACA_PV__Value: float
    CM_A181_V19_COM_V19_IN_5_PV3__Value: float
    CM_A181TE0023_DACA_PV__Value: float 
    CM_A181FT0010_DACA_PV__Value: float
    CM_A181AT0004_DACA_PV__Value: float 
    CM_A181PDT0002_DACA_PV__Value: float
    CM_A181PT0002_DACA_PV__Value: float 
    CM_A181PT0003_DACA_PV__Value: float
    CM_A181PT0004_DACA_PV__Value: float 
    CM_A181PT0005_DACA_PV__Value: float
    CM_A181PT0006_DACA_PV__Value: float 
    CM_A181PT0007_DACA_PV__Value: float
    CM_A181PT0008_DACA_PV__Value: float 
    CM_A181_TIEUHAOCO_OUT__Value: float

@app.post("/LN_EPortal_GenerateParameter")
def API_LN_EPortal_GenerateParameter(input: InputLN_EPortal):
    output = LN_EPortal_GenerateParameter(input,
                                          PG_cursor, PG_conn,
                                          model_LN_EPortal,
                                          model_LN_EPortal_COconsumption,
                                          model_LN_EPortal_Nhietkhoithai)
    return {"status": "success"}

# @app.post("/LH1_Evaluation")
# def API_LH1_Evaluation():
#     output = LH1_Evaluation(PG_cursor, PG_conn)
#     return output

# @app.post("/LH2_Evaluation")
# def API_LH2_Evaluation():
#     output = LH2_Evaluation(PG_cursor, PG_conn)
#     return output

# @app.post("/LN_Evaluation")
# def API_LN_Evaluation():
#     output = LN_Evaluation(PG_cursor, PG_conn)
#     return output

# @app.post("/LH_Forecasting")
# def API_LH_Forecasting():
#     output = LH2_Forecasting(PG_cursor, PG_conn, model_LH_Forecasting)
#     return output

@app.post("/Autotraining")
def Autotraining():
    LH1_AutoRetrainingModel(PG_cursor)
    LH2_AutoRetrainingModel(PG_cursor)
    return None

@app.post("/GenAI")
def GenAI():
    best_solution, best_fitness = GA()
    return best_fitness

@app.post("/Test")
def Test():
    # LN_EPortal(PG_cursor, PG_conn, model_LN_EPortal)
    # LH2_Forecasting_ARORSL(PG_cursor, PG_conn, "../models_rls")
    LH2_HistoryParameter(PG_cursor, PG_conn)
    return None

if __name__ == "__main__":
    uvicorn.run(app, host="192.168.1.92", port=8000)