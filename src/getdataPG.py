def getdataPG_Recommended_LH1(PG_cursor):
    # Thực hiện truy vấn lấy bản ghi mới nhất từ bảng "DCS_Items" theo thứ tự thời gian (CronTime).
    query_DCS_Items = '''SELECT "CronTime", "B1_FT1151_DACA_PV__Value", "B1_PT1281_DACA_PV__Value", 
    "B1_TE1212_DACA_PV__Value", "B1_TE1251_DACA_PV__Value", "B1_Z_BEDT_DACA_PV__Value",
    "B1_PT1061_DACA_PV__Value", "B1_PT1071_DACA_PV__Value", "B1_PT1111_DACA_PV__Value",
    "B1_PT1112_DACA_PV__Value", "B1_PT1211_DACA_PV__Value", "B1_PT1212_DACA_PV__Value",
    "B1_TZ1131ZT_DACA_PV__Value", "B1_S051AIT_DACA_PV__Value", "B1_AZ1011ZT_DACA_PV__Value",
    "B1_S052AIT_DACA_PV__Value","B1_S052AVFD_CRT_DACA_PV__Value", "B1_S052AVFD_FB_DACA_PV__Value",
    "B1_AT1011_DACA_PV__Value","B1_AT1012_DACA_PV__Value", "B1_PT1081_DACA_PV__Value",
    "B1_PT1082_DACA_PV__Value","B1_PT1091_DACA_PV__Value", "B1_PT1092_DACA_PV__Value",
    "B1_TE1111_DACA_PV__Value","B1_TE1112_DACA_PV__Value", "B1_Z_ZML_DACA_PV__Value",
    "B1_FT1151_DIVA_OUT__Value" FROM "DCS_Items" ORDER BY "CronTime" DESC LIMIT 1'''
    PG_cursor.execute(query_DCS_Items)
    data_DCS_Items = PG_cursor.fetchone()

    # Truy vấn các bản ghi gần đây từ bảng "DATA_CTCN" với giới hạn tối đa 10 bản ghi.
    query_DATA_CTCN = '''SELECT "LDA12080012000243", "LDA12080012000228", "LDA12080012000227", "LDA12080012000230",
    "LDA12080012000238", "LDA12080012000237", "LDA12080012000232", "LDA12080012000236",
    "LDA12080012000235", "LDA12080012000234", "LDA12080012000233" FROM "DATA_CTCN" ORDER BY "CronTime" DESC LIMIT 10'''
    data_DATA_CTCN =[]
    PG_cursor.execute(query_DATA_CTCN)
    result_query_DATA_CTCN = PG_cursor.fetchall()

    # Duyệt qua các bản ghi để lấy dữ liệu có giá trị hợp lệ (không có giá trị None).
    for data in result_query_DATA_CTCN:
        if None not in data:
            data_DATA_CTCN = data
        break

    # print(data_DCS_Items)
    # print(data_DATA_CTCN)
    return None

def Auto_getdataPG_Recommended_LH1(PG_cursor):
    # Truy vấn 24 bản ghi gần nhất từ bảng "DATA_CTCN" để lấy dữ liệu có giá trị hợp lệ.
    query_DATA_CTCN = '''SELECT "CronTime","LDA12080012000243", "LDA12080012000228", "LDA12080012000227", "LDA12080012000230",
    "LDA12080012000238", "LDA12080012000237", "LDA12080012000232", "LDA12080012000236",
    "LDA12080012000235", "LDA12080012000234", "LDA12080012000233" FROM "DATA_CTCN" ORDER BY "CronTime" DESC LIMIT 24'''
    data_DATA_CTCN =[]
    PG_cursor.execute(query_DATA_CTCN)
    result_query_DATA_CTCN = PG_cursor.fetchall()

    # Chọn bản ghi đầu tiên không chứa giá trị None hoặc lấy bản ghi đầu tiên trong kết quả.
    for data in result_query_DATA_CTCN:
        if None not in data:
            data_DATA_CTCN = data
            break
    else:
        data_DATA_CTCN = result_query_DATA_CTCN[0]
    # print(data_DATA_CTCN)

    # Truy vấn bản ghi mới nhất từ "DCS_Items" cho cột "B1_FT1151_DACA_PV__Value".
    query_DCS_Items = '''SELECT "B1_FT1151_DACA_PV__Value" FROM "DCS_Items" ORDER BY "CronTime" DESC LIMIT 1'''
    PG_cursor.execute(query_DCS_Items)
    data_DCS_Items = PG_cursor.fetchone()
    # print(data_DCS_Items)

    # Ghép dữ liệu từ hai bảng "DATA_CTCN" và "DCS_Items" lại.
    data_input = data_DATA_CTCN + data_DCS_Items
    return data_input

def Auto_getdataPG_Recommended_LH2(PG_cursor):
    # Truy vấn 24 bản ghi gần nhất từ bảng "DATA_CTCN" để lấy dữ liệu có giá trị hợp lệ.
    query_DATA_CTCN = '''SELECT "CronTime","LDA12080012000243", "LDA12080012000228", "LDA12080012000227", "LDA12080012000230",
    "LDA12080012000238", "LDA12080012000237", "LDA12080012000232", "LDA12080012000236",
    "LDA12080012000235", "LDA12080012000234", "LDA12080012000233" FROM "DATA_CTCN" ORDER BY "CronTime" DESC LIMIT 24'''
    data_DATA_CTCN =[]
    PG_cursor.execute(query_DATA_CTCN)
    result_query_DATA_CTCN = PG_cursor.fetchall()

    # Chọn bản ghi đầu tiên không chứa giá trị None hoặc lấy bản ghi đầu tiên trong kết quả.
    for data in result_query_DATA_CTCN:
        if None not in data:
            data_DATA_CTCN = data
            break
    else:
        data_DATA_CTCN = result_query_DATA_CTCN[0]
    # print(data_DATA_CTCN)

    # Truy vấn bản ghi mới nhất từ "DCS_Items" cho cột "B1_FT1151_DACA_PV__Value".
    query_DCS_Items = '''SELECT "B2_FT1151_DACA_PV__Value" FROM "DCS_Items" ORDER BY "CronTime" DESC LIMIT 1'''
    PG_cursor.execute(query_DCS_Items)
    data_DCS_Items = PG_cursor.fetchone()
    # print(data_DCS_Items)

    # Ghép dữ liệu từ hai bảng "DATA_CTCN" và "DCS_Items" lại.
    data_input = data_DATA_CTCN + data_DCS_Items
    return data_input