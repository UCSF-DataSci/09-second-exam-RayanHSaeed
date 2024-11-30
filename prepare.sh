#generating ms_dirty_data.csv 
python3 generate_dirty_data.py

#input and output file names
input_file="ms_data_dirty.csv"
output_file="ms_data.csv"

#remove comment lines, empty lines, extra commas, and extract essential columns (patient_id, visit_date, age, education_level, walking_speed)
grep -v "^#" "$input_file" | sed '/^$/d' | sed 's/,,*/,/g' | cut -d ',' -f 1,2,4,5,6 > "$output_file"

#create insurance.lst file with a header
echo -e "insurance_type\nBasic\nPremium\nPlatinum" > insurance.lst

#total number of visits (excluding the header)
total_visits=$(tail -n +2 "$output_file" | wc -l)  
echo "Total number of visits: $total_visits"

#display the first few records
echo "First few records:"
head -n 5 "$output_file"