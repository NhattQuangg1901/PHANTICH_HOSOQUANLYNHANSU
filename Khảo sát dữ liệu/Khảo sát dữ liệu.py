import pandas as pd

# Đọc dữ liệu từ file 
df = pd.read_csv('employee_hr_records.csv')

# 1. Khảo sát Cấu trúc và Kiểu dữ liệu
print(df.info())
print("-"*15)

# 2. Khảo sát Mức độ thiếu sót (Missing Values)
# Đếm số giá trị Null/NaN trong mỗi cột
print(df.isnull().sum())
print("-"*15)

# 3. Khảo sát Tính nhất quán (Consistency & Formatting)
# Kiểm tra các biến phân loại có giá trị nào bị thiếu hoặc không hợp lệ
print(df['Gender'].value_counts(dropna=False))
print("-"*5)
print(df['Department'].value_counts(dropna=False))
print("-"*5)
print(df['Employment Status'].value_counts(dropna=False))
print("-"*15)

# 4. Khảo sát Phân phối và Ngoại lai (Distribution & Outliers)
print(df.describe())
print("-"*15)

# 5. Khảo sát Dữ liệu trùng lặp (Duplicates)
# Kiểm tra số dòng trùng lặp toàn bộ thông tin 
print("Dòng trùng lặp hoàn toàn:", df.duplicated().sum())
# Kiểm tra xem có ID nhân viên nào bị sử dụng nhiều lần không
print("ID bị trùng:", df.duplicated(subset=['Employee ID']).sum())
print("-"*15)

# 6. Khảo sát Logic và Ràng buộc (Data Logic)
# Ép kiểu thử cột Hire Date sang datetime, những ngày sai logic sẽ biến thành NaT (Not a Time)
invalid_dates = pd.to_datetime(df['Hire Date'], errors='coerce')
# Đếm số lượng ngày tháng bị lỗi logic so với ban đầu
loi_logic_date = invalid_dates.isnull().sum() - df['Hire Date'].isnull().sum()
print("Số ngày tháng sai logic:", loi_logic_date)
# Kiểm tra logic lương âm
print("Số nhân sự có lương âm:", (df['Annual Salary'] < 0).sum())
