import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('employee_hr_records_cleaned.csv')
sns.set_theme(style="whitegrid")
# Lọc ra các cột chứa dữ liệu số (Numeric)
numeric_cols = ['Annual Salary', 'Performance Rating', 'Satisfaction Score', 'Gender_Encoded']

# 1. Heatmap 
corr_matrix = df[numeric_cols].corr()
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1, linewidths=0.5)
plt.title('Ma trận tương quan giữa các biến số')
plt.tight_layout()
plt.show()



# 2. Histogram mức lương (Annual Salary)
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(data=df, x='Annual Salary', bins=30, kde=True, color='dodgerblue', ax=ax)
mean_salary = df['Annual Salary'].mean()
median_salary = df['Annual Salary'].median()
ax.axvline(mean_salary, color='red', linestyle='--', linewidth=2, 
           label=f'Trung bình: ${mean_salary:,.0f}')
ax.axvline(median_salary, color='green', linestyle='-', linewidth=2, 
           label=f'Trung vị: ${median_salary:,.0f}')
ax.set_title('Biểu đồ phân phối Mức lương', fontsize=14, pad=15)
ax.set_xlabel('Mức lương (Annual Salary)', fontsize=12)
ax.set_ylabel('Tần suất (Số nhân viên)', fontsize=12)
ax.legend() 
plt.tight_layout()
plt.show()



# 3. Scatter plot giữa Annual Salary và Satisfaction Score, phân biệt theo Employment Status
plt.figure(figsize=(9, 6))
sns.scatterplot(data=df, x='Annual Salary', y='Satisfaction Score', 
                hue='Employment Status', alpha=0.7, palette='Set1')
plt.title('Tương quan giữa Lương và Điểm hài lòng')
plt.tight_layout()
plt.show()



# 4. Scatter plot giữa Satisfaction Score và Performance Rating, phân biệt theo Employment Status
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=df, x='Satisfaction Score', y='Performance Rating', 
                hue='Employment Status', alpha=0.7, palette='Set1', ax=ax)
ax.set_title(f'Tương quan giữa Điểm hài lòng và Điểm hiệu suất', fontsize=14, pad=15)
ax.set_xlabel('Điểm hài lòng (Satisfaction Score)', fontsize=12)
ax.set_ylabel('Điểm hiệu suất (Performance Rating)', fontsize=12)
plt.tight_layout()
plt.show() 



# 5. Biểu đồ cột và đường kết hợp: Số lượng nhân viên nghỉ việc và Điểm hài lòng trung bình theo Thâm niên
# 5.1. xử lý ngày tháng
df['Hire Date'] = pd.to_datetime(df['Hire Date'])
# dữ liệu ở thời điểm 2026-05-23
current_date = pd.to_datetime('2026-05-23')
# 5.2. Tính số năm làm việc (Thâm niên) = Làm tròn xuống của (Ngày hiện tại - Ngày vào làm) / 365.25
df['Tenure_Years'] = np.floor((current_date - df['Hire Date']).dt.days / 365.25)
df = df[df['Tenure_Years'] >= 0] 
# 5.3. Tính toán số liệu 
# Đếm số người nghỉ việc theo từng năm
turnover_by_tenure = df[df['Employment Status'] == 'Resigned'].groupby('Tenure_Years').size() 
# Tính trung bình điểm hài lòng theo từng năm
satisfaction_by_tenure = df.groupby('Tenure_Years')['Satisfaction Score'].mean() 
# 5.4. Vẽ biểu đồ
fig, axes = plt.subplots(1, 2, figsize=(16, 6)) 
# Cột: Số người nghỉ việc
sns.barplot(x=turnover_by_tenure.index.astype(int), y=turnover_by_tenure.values, ax=axes[0], palette='flare')
axes[0].set_title('Số lượng nhân viên Nghỉ việc theo Thâm niên')
axes[0].set_xlabel('Thâm niên (Năm)')
# Đường: Điểm hài lòng
sns.lineplot(x=satisfaction_by_tenure.index.astype(int), y=satisfaction_by_tenure.values, 
             ax=axes[1], marker='o', color='dodgerblue', linewidth=2.5)
axes[1].set_title('Điểm hài lòng trung bình theo Thâm niên')
axes[1].set_xlabel('Thâm niên (Năm)')
plt.tight_layout()
plt.show() 



# 6. Tương quan Điểm hài lòng và tỷ lệ nghỉ việc theo từng Phòng ban
# 6.1. Tính điểm hài lòng trung bình theo phòng ban
satisfaction = df.groupby('Department')['Satisfaction Score'].mean().sort_values(ascending=False)
# 6.2. Tính tỷ lệ tự nghỉ việc (Resigned)
df['Is_Resigned'] = (df['Employment Status'] == 'Resigned').astype(int)
turnover = (df.groupby('Department')['Is_Resigned'].mean() * 100).sort_values(ascending=False)
# setup biểu đồ
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
# Biểu đồ 1
sns.barplot(x=satisfaction.values, y=satisfaction.index, ax=axes[0], palette='coolwarm_r')
axes[0].set_title('Điểm hài lòng trung bình theo Phòng ban', fontsize=14)
axes[0].set_xlabel('Điểm hài lòng (1-10)')
# Biểu đồ 2
sns.barplot(x=turnover.values, y=turnover.index, ax=axes[1], palette='Reds_r')
axes[1].set_title('Tỷ lệ nhân viên tự nghỉ việc (%)', fontsize=14)
axes[1].set_xlabel('Tỷ lệ (%)')
plt.tight_layout()
plt.show()  