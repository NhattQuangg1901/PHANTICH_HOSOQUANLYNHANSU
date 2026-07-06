import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Thiết lập style cho biểu đồ
sns.set_theme(style="whitegrid")

# 1. Đọc dữ liệu
df = pd.read_csv('employee_hr_records_cleaned.csv')
# Chuyển đổi cột Hire Date sang định dạng datetime
df['Hire Date'] = pd.to_datetime(df['Hire Date'])

# 2. Thông tin tổng quan
print("--- THÔNG TIN CHUNG VỀ DỮ LIỆU ---")
print(df.info())

# 3. Kiểm tra dữ liệu thiếu (Missing values)
print("\n--- KIỂM TRA DỮ LIỆU KHUYẾT THIẾU ---")
print(df.isnull().sum())

# 4. Thống kê mô tả cho các biến định lượng (Numeric)
print("\n--- THỐNG KÊ MÔ TẢ (BIẾN ĐỊNH LƯỢNG) ---")
print(df.describe())

# 5. Thống kê mô tả cho các biến định tính (Categorical/Object)
print("\n--- THỐNG KÊ MÔ TẢ (BIẾN ĐỊNH TÍNH) ---")
print(df.describe(include=['object']))