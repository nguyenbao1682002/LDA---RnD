from datetime import datetime,timedelta
import os
import pyodbc
from dotenv import load_dotenv

def connect_XHQ():
    load_dotenv(dotenv_path="D:/001.Project/LDA_master/.env",override=True)
    XHQ_server = os.getenv("XHQ_SERVER")
    XHQ_database = os.getenv("XHQ_DATABASE")
    XHQ_username = os.getenv("XHQ_USERNAME")
    XHQ_password = os.getenv("XHQ_PASSWORD")
    XHQ_conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={XHQ_server};DATABASE={XHQ_database};UID={XHQ_username};PWD={XHQ_password}')
    XHQ_cursor = XHQ_conn.cursor()
    return XHQ_cursor, XHQ_conn

# Hàm xử lý tên cột cho phù hợp với định dạng mong muốn
def process_column(column):
    # Thay thế tên các cột từ định dạng gốc sang định dạng chuẩn hóa
    column = column.replace("B1_PT1211B_DACA_PV", "B1_PT1211.DACA.PV")
    column = column.replace("B1_PT1212B_DACA_PV", "B1_PT1212.DACA.PV")
    column = column.replace("B1_PT1011_DACA_PV", "B1_PT1011B.DACA.PV")
    column = column.replace("B1_FT1021B_DACA_PV", "B1_FT1021B.DACA.PV")
    column = column.replace("B1_FT1011B_DACA_PV", "B1_FT1011B.DACA.PV")
    column = column.replace("B1_FT1101_AUXCALCA_PV", "B1_FT1101.AUXCALCA.PV")
    column = column.replace("CM_A181FT0010_FLOWCOMPA_PV", "CM_A181FT0010.DACA.PV")
    column = column.replace("CM_A181_V19_COM_V19_IN_5_PV3", "CM_A181_V19_COM.V19_IN_5.PV[3]")
    column = column.replace("CM_D091_COM_PBI_IN_3_16_PV1", "CM_D091_COM.PBI_IN_3_16.PV[1]")
    column = column.replace("CM_D091_COM_PBI_IN_3_16_PV2", "CM_D091_COM.PBI_IN_3_16.PV[2]")
    # Thay thế các hậu tố theo chuẩn hóa
    column = column.replace("_DACA_PV", ".DACA.PV")
    column = column.replace("_TOTALIZERA_PV", ".TOTALIZERA.PV")
    column = column.replace("_DACA", ".DACA")
    column = column.replace("_LS101", ".LS101")
    column = column.replace("_ADDA_OUT", ".ADDA.OUT")
    column = column.replace("_DIVA_OUT", ".DIVA.OUT")
    column = column.replace("_DEVCTLA_GPV", ".DEVCTLA.GPV")
    column = column.replace("_OUT", ".OUT")
    column = column.replace("_PV", ".PV")
    return column

# Hàm lấy dữ liệu từ bảng DCS_Items và chèn vào bảng trong PostgreSQL
def getdataXHQ_DCS_Items(PG_cursor, XHQ_cursor, PG_conn):
    try:
        XHQ_cursor, XHQ_conn = connect_XHQ()
        # Lấy toàn bộ dữ liệu từ bảng DCS.Items của XHQ
        XHQ_cursor.execute('SELECT * FROM DCS.Items')
        XHQ_data = XHQ_cursor.fetchall()

        # Lấy tên cột từ bảng DCS_Items trong PostgreSQL
        PG_cursor.execute('SELECT * FROM "DCS_Items" LIMIT 1')
        column_DCS_Items = [desc[0] for desc in PG_cursor.description]
        values = []
        for column in column_DCS_Items:
            # Chuẩn hóa tên cột
            column = process_column(column)
            if column == "CronTime":
                # Thêm thời gian hiện tại vào cột CronTime
                values.append(datetime.now().strftime('%Y-%m-%d %H:%M:00'))
            elif "Value" in column:
                # Xử lý các cột chứa "Value" trong tên
                column = column.replace("__Value", "")
                for item in XHQ_data:
                    name_column, value, _, datetime_val, _ = item
                    if name_column == column:
                        if value == 999999.0:
                            value = 0.14
                        values.append(value)
                        break
                else:
                    values.append(False)
                    print(column)
            elif "TimeStamp" in column:
                # Xử lý các cột chứa "TimeStamp" trong tên
                column = column.replace("__TimeStamp", "")
                for item in XHQ_data:
                    name_column, value, _, datetime_val, _ = item
                    if name_column == column:
                        values.append(datetime_val)
                        break
                else:
                    values.append(False)
                    print(column)
            elif "AVG" in column:
                # Tính trung bình cho các cột AVG
                tags = column.split("_")
                tag_1 = tags[0] + "_" + tags[2] + ".DACA.PV"
                tag_2 = tags[0] + "_" + tags[3] + ".DACA.PV"
                for item in XHQ_data:
                    name_column, value, _, datetime_val, _ = item
                    if name_column == tag_1:
                        tag_1_value = float(value)
                    if name_column == tag_2:
                        tag_2_value = float(value)
                values.append((tag_1_value + tag_2_value) / 2)
            else:
                values.append(0)
                print(column)

        # Thực hiện câu lệnh chèn dữ liệu vào bảng DCS_Items trong PostgreSQL
        PG_cursor = PG_conn.cursor()
        placeholders = ', '.join(['%s'] * len(column_DCS_Items))
        columns = [f'"{col}"' for col in column_DCS_Items]
        columns = ', '.join(columns)
        insert_query = f'INSERT INTO "DCS_Items" ({columns}) VALUES ({placeholders})'
        PG_cursor.execute(insert_query, values)
        PG_conn.commit()
    except Exception as e:
        PG_conn.rollback()
        print(f"An error occurred: {e}")
        pass
    
# Hàm lấy dữ liệu từ bảng DATA_CTCN trong XHQ và chèn vào bảng DATA_CTCN trong PostgreSQL
def getdataXHQ_DATA_CTCN(PG_cursor, XHQ_cursor, PG_conn):
    try:
        XHQ_cursor, XHQ_conn = connect_XHQ()
        path_DATA_CTCN_lastest = 'D:/001.Project/LDA_master/errorprocessing/DATA_CTCN_lastest.txt'
        # Định nghĩa tên cột cho bảng DATA_CTCN
        column_DCS_Items = ("LDA07060012000122", "LDA07060012000140", "LDA07060012000141", "LDA07060012000142", "LDA07060012000155", 
                "LDA07060012000156", "LDA07060012000157", "LDA07060012000158", "LDA07060012000159", "LDA07060012000160", 
                "LDA07060012000161", "LDA07060012000162", "LDA07060012000163", "LDA07060012000164", "LDA07060012000165", 
                "LDA07060012000166", "LDA07060012000176", "LDA08060012000244", "LDA11070012000630", "LDA12080012000126", 
                "LDA12080012000127", "LDA12080012000128", "LDA12080012000130", "LDA12080012000131", "LDA12080012000132", 
                "LDA12080012000133", "LDA12080012000134", "LDA12080012000135", "LDA12080012000136", "LDA12080012000137", 
                "LDA12080012000138", "LDA12080012000143", "LDA12080012000226", "LDA12080012000227", "LDA12080012000228", 
                "LDA12080012000230", "LDA12080012000231", "LDA12080012000232", "LDA12080012000233", "LDA12080012000234", 
                "LDA12080012000235", "LDA12080012000236", "LDA12080012000237", "LDA12080012000238", "LDA12080012000243", 
                "LDA12080012004679", "LDA12080012004779", "LDA12080012004879", "LDA12080012004979", "LDA07060012000144")
        # Xác định ca làm việc dựa trên thời gian hiện tại
        # date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        time = int(datetime.now().strftime('%H'))
        # Ca 1 se lay du lieu Ca 1 cua ngay truoc do
        if 6 <= time < 14:
            shift = 2
            date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        # Ca 2 se lay du lieu Ca 2 cua ngay truoc do
        elif 14 <= time < 22:
            shift = 3
            date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        # Ca 3 se lay du lieu Ca 3 cua ngay truoc do, nhung tu 0h se lay du lieu cach nhau 2 ngay
        elif 22 <= time:
            shift = 1
            date = (datetime.now() - timedelta(days=0)).strftime('%Y-%m-%d')
        elif time < 6:
            shift = 1
            date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

        # Truy vấn dữ liệu từ bảng CHAT_LUONG.DATA_CTCN trong XHQ với điều kiện thời gian và ca làm việc
        XHQ_cursor.execute(f'SELECT "MA_DINH_DANH", "KET_QUA" FROM CHAT_LUONG.DATA_CTCN WHERE THOI_GIAN = ? AND CA = ?', date, shift)
        results = XHQ_cursor.fetchall()
        # print(results, date, shift)
        # Chuẩn bị giá trị để chèn vào bảng PostgreSQL
        values = [datetime.now().strftime('%Y-%m-%d %H:%M:00')]
        for column in column_DCS_Items:
            for item in results:
                name_column, value = item
                if name_column == column:
                    values.append(value)
                    break
            else:
                values.append(None)
        # Get DATA_CTCN_lastest in .txt file
        with open(path_DATA_CTCN_lastest, 'r') as file:
            lines = file.readlines()
            DATA_CTCN_lastest = [value.strip() for value in lines[0].split(',')]
        # Replace None value to lastest value
        for i in range(len(values)):
            if values[i] == None:
                values[i] = DATA_CTCN_lastest[i]
        # Write lastest values in .txt file
        with open(path_DATA_CTCN_lastest, 'w') as file:
            file.write(','.join(map(str, values)))

        # Thực hiện câu lệnh chèn dữ liệu vào bảng DATA_CTCN trong PostgreSQL
        columns = ["CronTime","LDA07060012000122", "LDA07060012000140", "LDA07060012000141", "LDA07060012000142", "LDA07060012000155", 
                "LDA07060012000156", "LDA07060012000157", "LDA07060012000158", "LDA07060012000159", "LDA07060012000160", 
                "LDA07060012000161", "LDA07060012000162", "LDA07060012000163", "LDA07060012000164", "LDA07060012000165", 
                "LDA07060012000166", "LDA07060012000176", "LDA08060012000244", "LDA11070012000630", "LDA12080012000126", 
                "LDA12080012000127", "LDA12080012000128", "LDA12080012000130", "LDA12080012000131", "LDA12080012000132", 
                "LDA12080012000133", "LDA12080012000134", "LDA12080012000135", "LDA12080012000136", "LDA12080012000137", 
                "LDA12080012000138", "LDA12080012000143", "LDA12080012000226", "LDA12080012000227", "LDA12080012000228", 
                "LDA12080012000230", "LDA12080012000231", "LDA12080012000232", "LDA12080012000233", "LDA12080012000234", 
                "LDA12080012000235", "LDA12080012000236", "LDA12080012000237", "LDA12080012000238", "LDA12080012000243", 
                "LDA12080012004679", "LDA12080012004779", "LDA12080012004879", "LDA12080012004979", "LDA07060012000144"]
        placeholders = ', '.join(['%s'] * len(columns))
        columns = [f'"{col}"' for col in columns]
        columns = ', '.join(columns)
        insert_query = f'INSERT INTO "DATA_CTCN" ({columns}) VALUES ({placeholders})'
        PG_cursor.execute(insert_query, values)
        PG_conn.commit()
    except Exception as e:
        PG_conn.rollback()
        print(f"An error occurred: {e}")
        pass
