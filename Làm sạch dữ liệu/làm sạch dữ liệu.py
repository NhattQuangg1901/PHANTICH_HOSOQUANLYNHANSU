import pandas as pd
import numpy as np
import time 

# --- HÀM XỬ LÝ IQR CHO LƯƠNG ---
def cap_outliers_iqr_salary(series):
    # Ép kiểu về số, chuỗi ký tự lạ biến thành NaN
    series = pd.to_numeric(series, errors='coerce')
    # tính IQR
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = max(0, Q1 - 1.5 * IQR)
    upper_bound = Q3 + 1.5 * IQR

    series_capped = series.clip(lower=lower_bound, upper=upper_bound)
    # Điền các giá trị trống (NaN) bằng trung vị của chuỗi đã xử lý
    return series_capped.fillna(series_capped.median())

# ===========================
#   LÀM SẠCH DỮ LIỆU CHÍNH
# ===========================
df = pd.read_csv('employee_hr_records.csv')

# 2. Loại bỏ các dòng trùng lặp hoàn toàn
df = df.drop_duplicates()

# 3. Mã hóa cột 'Gender' (Giới tính)
df['Gender'] = df['Gender'].replace({'M': 'Male', 'F': 'Female'})
df = df.dropna(subset=['Gender'])
df['Gender_Encoded'] = df['Gender'].map({'Female': 0, 'Male': 1})

# 4. cột 'Hire Date' (Ngày vào làm)
# Ép kiểu dữ liệu về dạng Ngày tháng, ép lỗi thành NaT
df['Hire Date'] = pd.to_datetime(df['Hire Date'], errors='coerce')
# Xóa các dòng có ngày không hợp lệ
df = df.dropna(subset=['Hire Date'])
# Xóa bỏ các ngày lớn hơn ngày hiện tại 
df = df[df['Hire Date'] <= pd.Timestamp.now()]

# 5. Xử lý 'Annual Salary' bằng IQR
df['Annual Salary'] = cap_outliers_iqr_salary(df['Annual Salary'])

# 6. Xử lý 'Performance Rating' (Thang 1-5) & 'Satisfaction Score' (Thang 1-10)
# 6.1: Ép sang kiểu số (chuỗi lỗi gõ nhầm thành NaN)
df['Performance Rating'] = pd.to_numeric(df['Performance Rating'], errors='coerce')
df['Satisfaction Score'] = pd.to_numeric(df['Satisfaction Score'], errors='coerce')

# 6.2: Giới hạn giá trị theo đúng nghiệp vụ (Cắt ngọn những số ngoài khoảng)
df['Performance Rating'] = df['Performance Rating'].clip(lower=1, upper=5)
df['Satisfaction Score'] = df['Satisfaction Score'].clip(lower=1, upper=10)

# 7. Xóa các dòng thiếu thông tin công việc
df = df.dropna(subset=['Job Title'])

# 8. Điền giá trị 'Unknown' cho các cột quan trọng còn thiếu thông tin nhưng không thể xóa 
unknown_cols = ['Employee ID', 'Full Name', 'Department']
df[unknown_cols] = df[unknown_cols].fillna('Unknown')

# 9. Reset lại index cho gọn gàng sau khi xóa dòng
df = df.reset_index(drop=True)

# Lưu và kiểm tra lại kết quả
df.to_csv('employee_hr_records_cleaned.csv', index=False)
print("Đã lưu dữ liệu làm sạch thành công vào file 'employee_hr_records_cleaned.csv'!")
print("Thông tin dữ liệu sau khi làm sạch:")
print(df.info())
print("\n5 dòng dữ liệu đầu tiên:")
print(df.head())