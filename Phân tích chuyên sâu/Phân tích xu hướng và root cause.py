import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('employee_hr_records_cleaned.csv')
df['Hire Year'] = pd.to_datetime(df['Hire Date']).dt.year
df['Is_Resigned'] = (df['Employment Status'] == 'Resigned').astype(int)

print("=== 1. XU HƯỚNG TUYỂN DỤNG & QUẢN LÝ LƯƠNG ĐỐI VỚI PHÒNG BAN ===")
# Biến động tuyển dụng qua các năm
hiring_trend = df.groupby('Hire Year').size()
hiring_trend.plot(kind='line', marker='o', title='Xu huong tuyen dung theo nam', color='teal')
plt.ylabel('So luong tuyen moi')
plt.show()

# Quỹ lương, lương trung bình và điểm hài lòng theo phòng ban
dept_stats = df.groupby('Department').agg(
    Tong_Quy_Luong=('Annual Salary', 'sum'),
    Luong_Trung_Binh=('Annual Salary', 'mean'),
    Hai_Long_TB=('Satisfaction Score', 'mean'),
    Ty_Le_Nghi_Viec_Percent=('Is_Resigned', lambda x: x.mean() * 100)
).sort_values(by='Tong_Quy_Luong', ascending=False)
print(dept_stats.round(2))

print("\n=== 2. TOP 5 NHÂN VIÊN CÓ LƯƠNG CAO NHẤT ===")
print(df.nlargest(5, 'Annual Salary')[['Full Name', 'Department', 'Job Title', 'Annual Salary']])

print("\n=== 3. PHÂN TÍCH ROOT CAUSE NGHỈ VIỆC ===")
# Tỷ lệ nghỉ việc theo Điểm hài lòng và Điểm hiệu suất
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
(df.groupby('Satisfaction Score')['Is_Resigned'].mean() * 100).plot(kind='bar', ax=axes[0], color='skyblue', title='Ty le nghi viec (%) theo Diem hai long')
(df.groupby('Performance Rating')['Is_Resigned'].mean() * 100).plot(kind='bar', ax=axes[1], color='salmon', title='Ty le nghi viec (%) theo Diem hieu suat')
plt.tight_layout()
plt.show()

print("\n=== 4. PHÁT HIỆN NHÂN TÀI HIỆU SUẤT CAO NHƯNG BẤT MÃN ===")
critical_talents = df[
    (df['Employment Status'] == 'Active') & 
    (df['Performance Rating'] >= 4) & 
    (df['Satisfaction Score'] <= 2)
]
print(f"Phat hien {len(critical_talents)} nhan su nguy co cao:")
print(critical_talents[['Employee ID', 'Full Name', 'Department', 'Performance Rating', 'Satisfaction Score']])

# Xuất danh sách nhân sự nguy cơ cao nghỉ việc ra file riêng
critical_talents.to_csv('Nhan_su_nguy_co_cao.csv', index=False)