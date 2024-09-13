from dash import Dash, dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import polars as pl
import plotly.express as px
import components as cmp

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Load the data
df_path = 'data/air-pollution.csv'
df = pl.read_csv(df_path)

# Generate dropdown options for country, year and air quality category
countries = sorted(df['Country'].unique().to_list())
countries_options = [{'label': country, 'value': country} for country in countries]
years = sorted(df['Year'].unique().to_list())
years_options = [{'label': year, 'value': year} for year in years]
air_qualities = sorted(df['Air Quality'].unique().to_list())
air_qualities_options = [{'label': air_quality, 'value': air_quality} for air_quality in air_qualities]

# Create Dash components
countries_dropdown = cmp.create_dropdown(id='countries-dropdown', options=countries_options, placeholder='Select a country')
line_chart_container = dcc.Graph(id='line-chart-container')
years_dropdown = cmp.create_dropdown(id='years-dropdown', options=years_options, placeholder='Select a year')
tree_map_container = dcc.Graph(id='tree-map-container')
air_qualities_dropdown = cmp.create_dropdown(id='air-qualities-dropdown', options=air_qualities_options, placeholder='Select an air quality category')
table_container = html.Div(id='table-container')
footer = cmp.create_footer()

# Custom colors for the air quality categories
custom_colors = {
        'Good': '#96F550',
        'Moderate': '#ffef00',
        'Unhealthy for Sensitive Groups': '#FF5E0E',
        'Unhealthy': '#C6011F',
        'Very Unhealthy': '#662d91',
        'Hazardous': '#635147'
    }

# Define the layout
app.layout = html.Div([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1('Air Pollution Dashboard (1850-2021)', className='text-center', style={'color': cmp.PRIMARY_COLOR})
        ], md=8, sm=12, className='my-2'),
        dbc.Col([
            html.P('Explore air pollution data from cities around the world', className='lead text-white text-center')
        ], md=4, sm=12, className='my-2')
    ], className='my-2'),

    # Main content
    dbc.Container([
        # Line chart section
        dbc.Row([
            dbc.Col([
                countries_dropdown
            ], xl=2, lg=3, md=4, sm=6, xs=12, className='my-2'),
            dbc.Col([
                line_chart_container
            ], width=12, className='my-2')
        ], className='my-4'),
 
        # Tree map and table section
        dbc.Row([
            dbc.Col([
                dbc.Col([
                    years_dropdown
                ], xl=4, lg=6, md=4, sm=6, xs=12, className='my-2'),
                dbc.Col([
                    tree_map_container
                ], width=12, className='my-2')
            ], lg=6, md=12, className='mb-4'),
            dbc.Col([
                dbc.Col([
                    air_qualities_dropdown
                ], xl=4, lg=6, md=4, sm=6, xs=12, className='my-2'),
                dbc.Col([
                    table_container
                ], width=12, className='my-2')
            ], lg=6, md=12, className='mb-4')
        ], className='my-4')
    ], 
    fluid=True, 
    className='mx-auto'),
    html.Div([html.Br()], style={'backgroundColor': cmp.BACKGROUND_COLOR}),

    # Footer
    footer
], style={'backgroundColor': cmp.BACKGROUND_COLOR})

# Callback to update the line chart based on the selected country
@app.callback(
    Output('line-chart-container', 'figure'),
    Input('countries-dropdown', 'value')
)
def update_line_chart(selected_country: str) -> px.line:
    if not selected_country:
        selected_country = countries[0]
    filtered_df = df.filter(df['Country'] == selected_country)
    fig = cmp.create_line_chart(
        df=filtered_df, 
        x='Year', 
        y='Air Quality (µg/m³)', 
        color='City', 
        title=f'Air Quality for Cities in {selected_country} Over Time',
        treshold_colors=custom_colors)
    
    return fig

# Callback to update the tree map based on the selected year
@app.callback(
    Output('tree-map-container', 'figure'),
    Input('years-dropdown', 'value')
)
def update_tree_map(selected_year: int) -> px.treemap:
    if not selected_year:
        selected_year = years[0]
    filtered_df = df.filter(df['Year'] == selected_year).to_pandas()
    grouped_df = (filtered_df.groupby('Air Quality')
                             .size()
                             .reset_index(name='Count')
                             .sort_values(by='Count', ascending=False))
    fig = cmp.create_tree_map(
        df=grouped_df, 
        category='Air Quality', 
        values='Count', 
        title=f'City Count by Air Quality Category in {selected_year}',
        custom_colors=custom_colors)
    return fig

# Callback to update the table based on the selected year and air quality category
@app.callback(
    Output('table-container', 'children'),
    Input('years-dropdown', 'value'),
    Input('air-qualities-dropdown', 'value')
)
def update_table(selected_year: int, selected_air_quality: str) -> dash_table.DataTable:
    if not selected_year:
        selected_year = years[0]
    if not selected_air_quality:
        selected_air_quality = air_qualities[0]
    filtered_df = df.filter((df['Year'] == selected_year) & (df['Air Quality'] == selected_air_quality))
    if selected_air_quality in ['Good', 'Moderate']:
        filtered_df = filtered_df.sort('Air Quality (µg/m³)')
    else:
        filtered_df = filtered_df.sort('Air Quality (µg/m³)', descending=True)
    filtered_df = filtered_df.select(['City', 'Country', 'Air Quality (µg/m³)'])
    table = cmp.create_table(filtered_df.to_pandas())
    return table


if __name__ == '__main__':
    app.run_server(debug=True)