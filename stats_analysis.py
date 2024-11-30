import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt

#Loading the data
data_file = "ms_data_insurance.csv"
data = pd.read_csv(data_file, sep=',')

#1. Analyze walking speed:
model = smf.mixedlm("walking_speed ~ age + education_level", data, groups=data["patient_id"])
results = model.fit()

#Regression summary for walking speed
print("\nMultiple Regression for Walking Speed with Education and Age:")
print(results.summary())

#Test for significant trends: 
data['visit_date'] = pd.to_datetime(data['visit_date'])
data = data.sort_values(by=['patient_id', 'visit_date'])
data['days_since_first_visit'] = data.groupby('patient_id')['visit_date'].transform('min')
data['days_since_first_visit'] = (data['visit_date'] - data['days_since_first_visit']).dt.days
print(data.head())

data['days_since_first_visit'] = (data['visit_date'] - data['visit_date'].min()).dt.days
trend_model = smf.mixedlm("walking_speed ~ days_since_first_visit + age + education_level", data, groups=data["patient_id"])
trend_results = trend_model.fit()

print("\nRegression for Walking Speed Trend over Time:")
print(trend_results.summary())

#2. Analyze Cost
#ANOVA to compare visit costs across different insurance types
anova_results = stats.f_oneway(data[data['insurance_type'] == 'Basic']['visit_cost'],
                               data[data['insurance_type'] == 'Premium']['visit_cost'],
                               data[data['insurance_type'] == 'Platinum']['visit_cost'])
print("\nANOVA Results for Insurance Type and Visit Costs:")
print(f"F-statistic: {anova_results.statistic}, p-value: {anova_results.pvalue}")

#Box Plots and Basic Statistics for Costs by Insurance Type
sns.boxplot(x="insurance_type", y="visit_cost", data=data)
plt.title("Visit Costs by Insurance Type")
plt.show()

#Summary statistics for visit costs by insurance type
print("\nSummary Statistics for Visit Costs by Insurance Type:")
print(data.groupby('insurance_type')['visit_cost'].describe())

#Calculate Effect Sizes: Cohen's d for Basic vs Premium insurance
group1 = data[data['insurance_type'] == 'Basic']['visit_cost']
group2 = data[data['insurance_type'] == 'Premium']['visit_cost']

t_stat, p_value = stats.ttest_ind(group1, group2)
cohen_d = (group1.mean() - group2.mean()) / np.sqrt((group1.std() ** 2 + group2.std() ** 2) / 2)

print(f"\nCohen's d for Basic vs Premium: {cohen_d}, p-value: {p_value}")

#3. Advanced Analysis
#Mixed-effects model for walking speed with interaction between age and education
interaction_model = smf.mixedlm("walking_speed ~ age * education_level", data, groups=data["patient_id"])
interaction_results = interaction_model.fit()

#Print the regression summary for interaction effects
print("\nRegression for Interaction Effects between Education and Age on Walking Speed:")
print(interaction_results.summary())

#Control for Relevant Confounders: Add additional covariates like insurance type
full_model = smf.mixedlm("walking_speed ~ age * education_level + insurance_type", data, groups=data["patient_id"])
full_results = full_model.fit()

#Print the regression summary controlling for confounders
print("\nRegression with Education, Age, and Insurance Type as Covariates:")
print(full_results.summary())

#Report Key Statistics and P-values
print("\nConfidence Intervals for Regression Coefficients (Interaction Model):")
print(interaction_results.conf_int())