import pandas as pd

def prepare_data(df : pd.DataFrame) -> pd.DataFrame:
    melted_df = pd.melt(df, id_vars=['Year'], var_name='City_Country', value_name='Air Quality Index')
    
    split_data = melted_df['City_Country'].str.split(', ', expand=True)
    melted_df['City'] = split_data[0]
    melted_df['Country'] = split_data[1]
    melted_df['Country'] = melted_df['Country'].fillna('Unknown')
    melted_df.drop(columns=['City_Country'], inplace=True)
    
    air_quality_bins = [0, 9, 35.4, 55.4, 125.4, 225.4, float('inf')]
    air_quaility_labels = ['Good', 'Moderate', 'Unhealthy for Sensitive Groups', 'Unhealthy', 'Very Unhealthy', 'Hazardous']
    melted_df['Air Quality'] = pd.cut(melted_df['Air Quality Index'], bins=air_quality_bins, labels=air_quaility_labels, right=True)
    
    melted_df.rename(columns={'Air Quality Index': 'Air Quality (µg/m³)'}, inplace=True)

    return melted_df

def prepare():
    raw_df_path = 'https://raw.githubusercontent.com/plotly/Figure-Friday/main/2024/week-36/air-pollution.csv'
    prepared_df_path = 'data/air-pollution.csv'
    raw_df = pd.read_csv(raw_df_path)
    prepared_df = prepare_data(raw_df)
    prepared_df.to_csv(prepared_df_path, index=False)

if __name__ == '__main__':
    prepare()