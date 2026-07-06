import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Đọc dữ liệu
df = pd.read_csv('employee_hr_records.csv')

# Thiết lập style để biểu đồ đẹp hơn
sns.set_theme(style="whitegrid")

# ---------------------------------------------------------
# 1. BAR CHART: Số lượng nhân viên theo phòng ban
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6))
counts = df['Department'].value_counts() 
sns.barplot(x=counts.values, y=counts.index, ax=ax, palette='viridis')
ax.set_title('Số lượng nhân viên theo phòng ban', fontsize=14, pad=15)
ax.set_xlabel('Số lượng nhân viên')
ax.set_ylabel('Phòng ban')
plt.tight_layout()
plt.show()

# ---------------------------------------------------------
# 2. PIE CHART: Tỷ lệ trạng thái làm việc
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 8))
counts = df['Employment Status'].value_counts()
ax.pie(counts, labels=counts.index, autopct='%1.1f%%', 
       startangle=90, colors=sns.color_palette('pastel'))
ax.set_title('Tỷ lệ Trạng thái làm việc của nhân viên', fontsize=14, pad=15)
plt.tight_layout()
plt.show()

# ---------------------------------------------------------
# 3. HISTOGRAM: Phân phối Mức lương
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(df['Annual Salary'].dropna(), bins=30, kde=True, color='skyblue', ax=ax)
ax.set_title('Phân phối Mức lương (Annual Salary)', fontsize=14, pad=15)
ax.set_xlabel('Mức lương')
ax.set_ylabel('Tần suất (Số người)')
plt.tight_layout()
plt.show()

# ---------------------------------------------------------
# 4. BOXPLOT: Điểm số hiệu suất và Hài lòng
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=df[['Performance Rating', 'Satisfaction Score']], ax=ax, palette='Set2')
ax.set_title('Boxplot: Phát hiện ngoại lai ở các cột Điểm số', fontsize=14, pad=15)
ax.set_ylabel('Giá trị điểm')
plt.tight_layout()
plt.show()