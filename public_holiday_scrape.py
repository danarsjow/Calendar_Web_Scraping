# %%
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import requests



# %%
# Fetches the current year to apply to the URL
now = datetime.now()
current_year = now.year


url = f"https://publicholidays.co.id/id/{current_year}-dates/"

page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')






# %%
# Scrapes the 'Hari Libur Nasional Tahun 2024' table
table = soup.find('table', class_ = 'publicholidays phgtable')


# %%
world_titles = table.find_all('th')


# %%
world_table_titles = [title.text.strip() for title in world_titles]


# %%
df = pd.DataFrame(columns = world_table_titles)
df

# %%
world_data= table.find_all('td')



# %%
# Original code to strip whitespace from text elements
data = [data.text.strip() for data in world_data]

# Remove empty strings from the list
data = [item for item in data if item]


# %%
data_reshaped = [data[i:i+3] for i in range(0, len(data), 3)]



df = pd.DataFrame(data_reshaped, columns=['Tanggal', 'Hari', 'Hari Libur'])
df = df.drop(columns=['Hari'])
df['Tanggal'] = df['Tanggal'].str.replace(' to', ',')
df['Tanggal'] = df['Tanggal'].str.findall(r'\d{1,2} \w+')
df = df.explode('Tanggal').reset_index(drop=True)
df['Tanggal'] = df['Tanggal'] + f" {current_year}"
df = df.dropna()


# %%
df2 = df
month_mapping = {
    'Januari': 'January',
    'Februari': 'February',
    'Maret': 'March',
    'April': 'April',
    'Mei': 'May',
    'Juni': 'June',
    'Juli': 'July',
    'Agustus': 'August',
    'September': 'September',
    'Oktober': 'October',
    'November': 'November',
    'Desember': 'December'
}
def convert_date(date_str):
    day, month_id, year = date_str.split()
    month_name = month_mapping[month_id]
    return datetime.strptime(f"{day} {month_name} {year}", "%d %B %Y")

# Apply the function and create a new column with the correct date format
df2['Tanggal'] = df2['Tanggal'].apply(convert_date)

# Convert to 'yy-mm-dd' format
df2['Tanggal'] = df2['Tanggal'].dt.strftime('%Y-%m-%d')



# %%
'''MODIFIES ROWS WITH DATES ORIGINALLY EXPRESSED AS 'DATE TO DATE' '''

df2['Tanggal'] = pd.to_datetime(df['Tanggal'], format='%Y-%m-%d')

# Function to generate date range and fill missing dates
def fill_dates(group):
    min_date = group['Tanggal'].min()
    max_date = group['Tanggal'].max()
    
    all_dates = pd.date_range(start=min_date, end=max_date)
    
    # Create a DataFrame with all dates and the holiday name
    filled_dates_df = pd.DataFrame({
        'Tanggal': all_dates,
        'Hari Libur': group['Hari Libur'].iloc[0]
    })
    return filled_dates_df

# Group by 'Hari Libur' and apply the fill_dates function
cleaned_df = df2.groupby('Hari Libur').apply(fill_dates).reset_index(drop=True)

# Convert 'Tanggal' back to 'yy-mm-dd' format
cleaned_df['Tanggal'] = cleaned_df['Tanggal'].dt.strftime('%Y-%m-%d')




# %%
