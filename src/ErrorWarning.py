def LN_ErrorWarning(PG_cursor, PG_conn):
    try:
        query_ErrorWarning = '''SELECT "CronTime", 
            "CM_A181PT0013_DACA_PV__Value", 
            "CM_A181S015BPGIA_DACA_PV__Value",
            "CM_A181S020AIA_DACA_PV__Value", "CM_A181S020BIA_DACA_PV__Value", 
            "CM_A181M1AIA_DACA_PV__Value", "CM_A181M3AIA_DACA_PV__Value", 
            "CM_A181FT0003_DACA_PV__Value",
            "CM_A181TE0007_DACA_PV__Value" FROM "DCS_Items" ORDER BY "CronTime" DESC LIMIT 1'''
        PG_cursor.execute(query_ErrorWarning)
        ErrorWarning = PG_cursor.fetchone()
        # print("ErrorWarning:",ErrorWarning)
        # ErrorWarning = ['2024-11-29 13:54:00',1,2,3,4,5,6,7,8]
        if ErrorWarning[1] <= 0:
            CronTime = ErrorWarning[0]
            ErrorID = 1
            ErrorType = 'Sự cố ngừng Mỏ đốt V19'
            CM_A181PT0013_DACA_PV__Value = ErrorWarning[1]
            CM_A181S015BPGIA_DACA_PV__Value = ErrorWarning[2]
            CM_A181S020AIA_DACA_PV__Value = ErrorWarning[3]
            CM_A181S020BIA_DACA_PV__Value = ErrorWarning[4]
            CM_A181M1AIA_DACA_PV__Value = ErrorWarning[5]
            CM_A181M3AIA_DACA_PV__Value = ErrorWarning[6]
            CM_A181FT0003_DACA_PV__Value = ErrorWarning[7]
            CM_A181TE0007_DACA_PV__Value = ErrorWarning[8]
            Action = 'Đóng van điều tiết về 15%. Giảm tốc độ Quạt ID về 60%, duy trì 10p rồi sau đó sẽ giảm dần. Mở cửa gió A05'
            # Insert Error 1
            insert_query = f'''INSERT INTO "DATA_LN_ErrorWarning" ("CronTime", "ErrorID", "ErrorType",
                "CM_A181PT0013_DACA_PV__Value", "CM_A181S015BPGIA_DACA_PV__Value", "CM_A181S020AIA_DACA_PV__Value",
                "CM_A181S020BIA_DACA_PV__Value", "CM_A181M1AIA_DACA_PV__Value", "CM_A181M3AIA_DACA_PV__Value",
                "CM_A181FT0003_DACA_PV__Value", "CM_A181TE0007_DACA_PV__Value", "Action") 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            PG_cursor.execute(insert_query, (CronTime, ErrorID, ErrorType,
                CM_A181PT0013_DACA_PV__Value, CM_A181S015BPGIA_DACA_PV__Value, CM_A181S020AIA_DACA_PV__Value,
                CM_A181S020BIA_DACA_PV__Value, CM_A181M1AIA_DACA_PV__Value, CM_A181M3AIA_DACA_PV__Value,
                CM_A181FT0003_DACA_PV__Value, CM_A181TE0007_DACA_PV__Value, Action))
            PG_conn.commit() 
        if 0 <= ErrorWarning[2] <= 0.1:
            CronTime = ErrorWarning[0]
            ErrorID = 2
            ErrorType = 'Sự cố ngừng Quạt ID'
            CM_A181PT0013_DACA_PV__Value = ErrorWarning[1]
            CM_A181S015BPGIA_DACA_PV__Value = ErrorWarning[2]
            CM_A181S020AIA_DACA_PV__Value = ErrorWarning[3]
            CM_A181S020BIA_DACA_PV__Value = ErrorWarning[4]
            CM_A181M1AIA_DACA_PV__Value = ErrorWarning[5]
            CM_A181M3AIA_DACA_PV__Value = ErrorWarning[6]
            CM_A181FT0003_DACA_PV__Value = ErrorWarning[7]
            CM_A181TE0007_DACA_PV__Value = ErrorWarning[8]
            Action = 'Cảnh báo đến phân xưởng khí than, trưởng ca, nhân viên vận hành và phòng điều hành sản xuất. Mở van A05, cấp gió lạnh làm mát cho PO1 với lọc bụi tĩnh điện không kích hoạt điều kiện dừng.'
            # Insert Error 2
            insert_query = f'''INSERT INTO "DATA_LN_ErrorWarning" ("CronTime", "ErrorID", "ErrorType",
                "CM_A181PT0013_DACA_PV__Value", "CM_A181S015BPGIA_DACA_PV__Value", "CM_A181S020AIA_DACA_PV__Value",
                "CM_A181S020BIA_DACA_PV__Value", "CM_A181M1AIA_DACA_PV__Value", "CM_A181M3AIA_DACA_PV__Value",
                "CM_A181FT0003_DACA_PV__Value", "CM_A181TE0007_DACA_PV__Value", "Action") 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            PG_cursor.execute(insert_query, (CronTime, ErrorID, ErrorType,
                CM_A181PT0013_DACA_PV__Value, CM_A181S015BPGIA_DACA_PV__Value, CM_A181S020AIA_DACA_PV__Value,
                CM_A181S020BIA_DACA_PV__Value, CM_A181M1AIA_DACA_PV__Value, CM_A181M3AIA_DACA_PV__Value,
                CM_A181FT0003_DACA_PV__Value, CM_A181TE0007_DACA_PV__Value, Action))
            PG_conn.commit()
        if ErrorWarning[3] < 45 and ErrorWarning[4] < 45:
            CronTime = ErrorWarning[0]
            ErrorID = 3
            ErrorType = 'Sự cố dừng Hệ thống vận chuyển thu hồi bụi'
            CM_A181PT0013_DACA_PV__Value = ErrorWarning[1]
            CM_A181S015BPGIA_DACA_PV__Value = ErrorWarning[2]
            CM_A181S020AIA_DACA_PV__Value = ErrorWarning[3]
            CM_A181S020BIA_DACA_PV__Value = ErrorWarning[4]
            CM_A181M1AIA_DACA_PV__Value = ErrorWarning[5]
            CM_A181M3AIA_DACA_PV__Value = ErrorWarning[6]
            CM_A181FT0003_DACA_PV__Value = ErrorWarning[7]
            CM_A181TE0007_DACA_PV__Value = ErrorWarning[8]
            Action = 'Nếu dừng 1 bên S016A chạy 1 bên S016B hoặc ngược lại. Nếu dừng S018A hoặc S019B thì sửa chữa ở đó. Chạy lại cao áp và đánh rung lọc bụi tĩnh điện S014 ESP tại hiện trường'
            # Insert Error 3
            insert_query = f'''INSERT INTO "DATA_LN_ErrorWarning" ("CronTime", "ErrorID", "ErrorType",
                "CM_A181PT0013_DACA_PV__Value", "CM_A181S015BPGIA_DACA_PV__Value", "CM_A181S020AIA_DACA_PV__Value",
                "CM_A181S020BIA_DACA_PV__Value", "CM_A181M1AIA_DACA_PV__Value", "CM_A181M3AIA_DACA_PV__Value",
                "CM_A181FT0003_DACA_PV__Value", "CM_A181TE0007_DACA_PV__Value", "Action") 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            PG_cursor.execute(insert_query, (CronTime, ErrorID, ErrorType,
                CM_A181PT0013_DACA_PV__Value, CM_A181S015BPGIA_DACA_PV__Value, CM_A181S020AIA_DACA_PV__Value,
                CM_A181S020BIA_DACA_PV__Value, CM_A181M1AIA_DACA_PV__Value, CM_A181M3AIA_DACA_PV__Value,
                CM_A181FT0003_DACA_PV__Value, CM_A181TE0007_DACA_PV__Value, Action))
            PG_conn.commit()
        if ErrorWarning[5] < 0.2 and ErrorWarning[6] < 0.2:
            CronTime = ErrorWarning[0]
            ErrorID = 4
            ErrorType = 'Sự cố vận chuyển liệu'
            CM_A181PT0013_DACA_PV__Value = ErrorWarning[1]
            CM_A181S015BPGIA_DACA_PV__Value = ErrorWarning[2]
            CM_A181S020AIA_DACA_PV__Value = ErrorWarning[3]
            CM_A181S020BIA_DACA_PV__Value = ErrorWarning[4]
            CM_A181M1AIA_DACA_PV__Value = ErrorWarning[5]
            CM_A181M3AIA_DACA_PV__Value = ErrorWarning[6]
            CM_A181FT0003_DACA_PV__Value = ErrorWarning[7]
            CM_A181TE0007_DACA_PV__Value = ErrorWarning[8]
            Action = 'Nếu 1 bên gầu nâng bị hư thì sẽ chuyển đảo van chuyển liệu về 1 phía. Báo cáo trưởng ca và điều hành xin giảm tải liệu đầu vào, thông báo bên phòng khí hóa than giảm nhiên liệu đầu vào, giảm tốc độ quạt ID phù hợp với lượng liệu đầu vào'
            # Insert Error 4
            insert_query = f'''INSERT INTO "DATA_LN_ErrorWarning" ("CronTime", "ErrorID", "ErrorType",
                "CM_A181PT0013_DACA_PV__Value", "CM_A181S015BPGIA_DACA_PV__Value", "CM_A181S020AIA_DACA_PV__Value",
                "CM_A181S020BIA_DACA_PV__Value", "CM_A181M1AIA_DACA_PV__Value", "CM_A181M3AIA_DACA_PV__Value",
                "CM_A181FT0003_DACA_PV__Value", "CM_A181TE0007_DACA_PV__Value", "Action") 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            PG_cursor.execute(insert_query, (CronTime, ErrorID, ErrorType,
                CM_A181PT0013_DACA_PV__Value, CM_A181S015BPGIA_DACA_PV__Value, CM_A181S020AIA_DACA_PV__Value,
                CM_A181S020BIA_DACA_PV__Value, CM_A181M1AIA_DACA_PV__Value, CM_A181M3AIA_DACA_PV__Value,
                CM_A181FT0003_DACA_PV__Value, CM_A181TE0007_DACA_PV__Value, Action))
            PG_conn.commit()
        if 150 <= ErrorWarning[7] <= 300:
            CronTime = ErrorWarning[0]
            ErrorID = 5
            ErrorType = 'Mất nước cấp tuần hoàn từ khu D09'
            CM_A181PT0013_DACA_PV__Value = ErrorWarning[1]
            CM_A181S015BPGIA_DACA_PV__Value = ErrorWarning[2]
            CM_A181S020AIA_DACA_PV__Value = ErrorWarning[3]
            CM_A181S020BIA_DACA_PV__Value = ErrorWarning[4]
            CM_A181M1AIA_DACA_PV__Value = ErrorWarning[5]
            CM_A181M3AIA_DACA_PV__Value = ErrorWarning[6]
            CM_A181FT0003_DACA_PV__Value = ErrorWarning[7]
            CM_A181TE0007_DACA_PV__Value = ErrorWarning[8]
            Action = 'Nếu 1 bơm bị ngừng thì bên vận hành sẽ đảo bơm (dùng bơm dự phòng thay thế cho bơm hư). Trong trường hợp chạy 1 bơm thì phải giảm cấp liệu đầu vào và cho chạy ở mức 60-70 tấn, giảm van điều tiết khí than, chia liệu chạy về 1 bên.'
            # Insert Error 5
            insert_query = f'''INSERT INTO "DATA_LN_ErrorWarning" ("CronTime", "ErrorID", "ErrorType",
                "CM_A181PT0013_DACA_PV__Value", "CM_A181S015BPGIA_DACA_PV__Value", "CM_A181S020AIA_DACA_PV__Value",
                "CM_A181S020BIA_DACA_PV__Value", "CM_A181M1AIA_DACA_PV__Value", "CM_A181M3AIA_DACA_PV__Value",
                "CM_A181FT0003_DACA_PV__Value", "CM_A181TE0007_DACA_PV__Value", "Action") 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            PG_cursor.execute(insert_query, (CronTime, ErrorID, ErrorType,
                CM_A181PT0013_DACA_PV__Value, CM_A181S015BPGIA_DACA_PV__Value, CM_A181S020AIA_DACA_PV__Value,
                CM_A181S020BIA_DACA_PV__Value, CM_A181M1AIA_DACA_PV__Value, CM_A181M3AIA_DACA_PV__Value,
                CM_A181FT0003_DACA_PV__Value, CM_A181TE0007_DACA_PV__Value, Action))
            PG_conn.commit()
        if ErrorWarning[8] > 1100:
            CronTime = ErrorWarning[0]
            ErrorID = 6
            ErrorType = 'Sự cố hệ thống cấp liệu'
            CM_A181PT0013_DACA_PV__Value = ErrorWarning[1]
            CM_A181S015BPGIA_DACA_PV__Value = ErrorWarning[2]
            CM_A181S020AIA_DACA_PV__Value = ErrorWarning[3]
            CM_A181S020BIA_DACA_PV__Value = ErrorWarning[4]
            CM_A181M1AIA_DACA_PV__Value = ErrorWarning[5]
            CM_A181M3AIA_DACA_PV__Value = ErrorWarning[6]
            CM_A181FT0003_DACA_PV__Value = ErrorWarning[7]
            CM_A181TE0007_DACA_PV__Value = ErrorWarning[8]
            Action = 'Người vận hành thông báo cho trưởng ca, nhân viên sửa chữa để nhanh chóng khắc phục các sự cố ở phía dưới xưởng như thông bồn chứa liệu nếu tắc liệu (có thể lò vẫn đang hoạt động), làm sạch đóng bám vít, thay động cơ, hộp giảm tốc,…'
            # Insert Error 6
            insert_query = f'''INSERT INTO "DATA_LN_ErrorWarning" ("CronTime", "ErrorID", "ErrorType",
                "CM_A181PT0013_DACA_PV__Value", "CM_A181S015BPGIA_DACA_PV__Value", "CM_A181S020AIA_DACA_PV__Value",
                "CM_A181S020BIA_DACA_PV__Value", "CM_A181M1AIA_DACA_PV__Value", "CM_A181M3AIA_DACA_PV__Value",
                "CM_A181FT0003_DACA_PV__Value", "CM_A181TE0007_DACA_PV__Value", "Action") 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            PG_cursor.execute(insert_query, (CronTime, ErrorID, ErrorType,
                CM_A181PT0013_DACA_PV__Value, CM_A181S015BPGIA_DACA_PV__Value, CM_A181S020AIA_DACA_PV__Value,
                CM_A181S020BIA_DACA_PV__Value, CM_A181M1AIA_DACA_PV__Value, CM_A181M3AIA_DACA_PV__Value,
                CM_A181FT0003_DACA_PV__Value, CM_A181TE0007_DACA_PV__Value, Action))
            PG_conn.commit()
    except Exception as e:
        PG_conn.rollback()
        print(f"An error occurred: {e}")
        pass