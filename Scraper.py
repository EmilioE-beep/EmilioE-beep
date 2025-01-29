import requests
import csv
from bs4 import BeautifulSoup

# Send a GET request to the URL
url = 'https://emu.edu/faculty-staff/all-name'
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Open a CSV file to write data
    with open('faculty_data_with_emails.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write the header row
        writer.writerow(['Name', 'Department', 'Position', 'Email'])
        
        # Find all faculty entries (assume each faculty member is in a <div> with a specific style or class)
        faculty_entries = soup.find_all('div', style="width:30%;")  # Adjust based on the actual structure
        
        # Extract name, department, position, and email
        for entry in faculty_entries:
            name_tag = entry.find('h6')
            department_tag = entry.find_next('p')  # Assuming department is in the next <p> tag
            position_tag = entry.find_next('p')  # Assuming position is in the same <p> or different tag (adjust if needed)
            
            # Check if the required information is available
            if name_tag and department_tag and position_tag:
                name = name_tag.get_text(strip=True)
                department = department_tag.get_text(strip=True)
                position = position_tag.get_text(strip=True)  # This assumes the position is also in a <p> tag
                
                # Construct the email address (assuming format is firstname.lastname@emu.edu)
                name_parts = name.split()
                if len(name_parts) >= 2:
                    first_name = name_parts[0].lower()
                    last_name = name_parts[1].lower()
                    email = f"{first_name}.{last_name}@emu.edu"
                else:
                    email = f"{name.lower()}@emu.edu"  # In case there's only one name part

                # Write the data to the CSV file
                writer.writerow([name, department, position, email])

    print("Data has been written to faculty_data_with_emails.csv")
else:
    print(f"Failed to retrieve the webpage, status code: {response.status_code}")
