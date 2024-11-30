import pandas as pd
import numpy as np

#read the processed CSV file
data_file = "ms_data.csv"
data = pd.read_csv(data_file, sep=',')

#convert visit_date to datetime
data['visit_date'] = pd.to_datetime(data['visit_date'])

#sort by patient_id and visit_date
data = data.sort_values(by=['patient_id', 'visit_date'])

#display the first few records to verify
print(data.head())

#read insurance types from insurance.lst
insurance_types = pd.read_csv("insurance.lst")
insurance_types_list = insurance_types['insurance_type'].tolist()

#randomly assign insurance types
np.random.seed(42)
patient_ids = data['patient_id'].unique()
patient_insurance = {pid: np.random.choice(insurance_types_list) for pid in patient_ids}
data['insurance_type'] = data['patient_id'].map(patient_insurance)

#generate visit costs based on insurance type
base_cost = {'Basic': 50, 'Premium': 100, 'Platinum': 200}
variation = np.random.uniform(-10, 10, size=len(data)) 
data['visit_cost'] = data['insurance_type'].map(base_cost) + variation

#mean walking speed by education level
mean_walking_speed = data.groupby('education_level')['walking_speed'].mean()
print("\nMean Walking Speed by Education Level:")
print(mean_walking_speed)

#mean costs by insurance type
mean_costs = data.groupby('insurance_type')['visit_cost'].mean()
print("\nMean Costs by Insurance Type:")
print(mean_costs)

#age effects on walking speed
age_bins = pd.cut(data['age'], bins=[20, 30, 40, 50, 60, 70, 80])
age_speed = data.groupby(age_bins)['walking_speed'].mean()
print("\nWalking Speed by Age Group:")
print(age_speed)