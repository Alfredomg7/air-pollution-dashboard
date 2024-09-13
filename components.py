from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import polars as pl

PRIMARY_COLOR = '#E63462'
BACKGROUND_COLOR = '#333745'
ALTERNATIVE_COLOR = '#59656F'
PRIMARY_COLOR_RGBA = 'rgba(230, 52, 98, 0.8)'

def create_dropdown(id : str, options : list, placeholder : str) -> dcc.Dropdown:
    dropdown = dcc.Dropdown(
        id=id,
        options=options,
        value=options[0]['value'],
        clearable=True,
        searchable=True,
        placeholder=placeholder
    )   
    return dropdown

def create_line_chart(df : pl.DataFrame, x : str, y : str, title : str, color : str, treshold_colors : dict) -> px.line:
    lines_colors = [PRIMARY_COLOR, '#00A7E1', '#70F8BA', '#8075FF', '#F49CBB', '#FFD131', '#CBF3F0']
    if len(df[color].unique()) > 1:
        fig = px.line(df, x=x, y=y, title=title, color=color, color_discrete_sequence=lines_colors)
    else:
        fig = px.line(df, x=x, y=y, title=title, color=color, color_discrete_sequence=[PRIMARY_COLOR])

    max_value = df[y].max() * 1.3
 
    air_quality_levels = {
        'Good': 0,
        'Moderate': 9,
        'Unhealthy for Sensitive Groups': 35.4,
        'Unhealthy': 55.4,
        'Very Unhealthy': 125.4,
        'Hazardous': 225.4
    }
    for category, level in air_quality_levels.items():
        if level <= max_value:
            fig.add_hline(y=level, line_dash="dash", line_color=treshold_colors.get(category, '#fff'))
            fig.add_annotation(
                xref="paper",
                yref="y",
                y=level,
                text=category,
                showarrow=False,
                font=dict(
                    color=treshold_colors.get(category, '#fff'),
                ),
                align="center",
                xanchor="center",
                yanchor="bottom",
                yshift=10
            )

    fig.update_layout(
        plot_bgcolor=BACKGROUND_COLOR, 
        paper_bgcolor=BACKGROUND_COLOR,
        title=dict(
            font=dict(size=20, color='#fff', weight=600),
            x=0.5
        ),
        xaxis=dict(
            showgrid=False,
            linecolor='#fff',
            title=dict(
                text=x,
                font=dict(size=16, color='#fff', weight=500)
            ),
            tickfont=dict(size=14, color='#fff')
        ),
        yaxis=dict(
            showgrid=False,
            linecolor='#fff',
            title=dict(
                text=y,
                font=dict(size=16, color='#fff', weight=500)
            ),
            tickfont=dict(size=14, color='#fff')
        ),
        legend=dict(
            title=dict(
                text=color,
                font=dict(size=16, color='#fff', weight=500)
            ),
            font=dict(size=14, color='#fff')
        )
    )
    return fig

def create_tree_map(df : pd.DataFrame, category : list, values : str, title : str, custom_colors : dict) -> px.treemap:
    fig = px.treemap(df, 
                     path=[category], 
                     values=values, 
                     title=title,
                     color=category,
                     color_discrete_map=custom_colors
                    )
    
    fig.update_layout(
        plot_bgcolor=BACKGROUND_COLOR, 
        paper_bgcolor=BACKGROUND_COLOR,
        title=dict(
            font=dict(size=20, color='#fff', weight=600),
            x=0.5
        ),
    )
    return fig

def create_table(df : pd.DataFrame) -> dash_table.DataTable:
    table = dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{'name': col, 'id': col} for col in df.columns],
                style_header={
                    'backgroundColor': PRIMARY_COLOR,
                    'color': '#FFF',
                    'fontWeight': 'bold',
                    'borderBottom': '2px solid #FFF',
                    'textAlign': 'center',
                    'padding': '10px'
                },
                style_cell={
                    'backgroundColor': ALTERNATIVE_COLOR,
                    'color': '#FFF',
                    'border': '1px solid #ddd',
                    'textAlign': 'left',
                    'padding': '10px',
                    'whiteSpace': 'normal'
                },
                style_table={
                    'overflowX': 'auto',
                    'border': '1px solid #ccc',
                    'boxShadow': '0px 2px 8px rgba(0, 0, 0, 0.1)'
                },
                style_data_conditional=[
                    {
                        'if': {'state': 'active'},
                        'backgroundColor': PRIMARY_COLOR,
                        'border': 'none'
                    }
                ],
                style_data={
                    'border': '1px solid #ccc',
                },

                page_size=10,
                style_as_list_view=True,
            )
    return table
    
def create_footer() -> html.Footer:
    link_style = {
    'color': PRIMARY_COLOR,
    'font-weight': 'bold',
    'font-size': '16px',
    'text-decoration': 'none'
    }
    footer = html.Footer(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.A(
                            "Source Code",
                            href="https://github.com/Alfredomg7/air-pollution-dashboard",
                            target="_blank",
                            style=link_style
                        ),
                        className='text-center'
                    ),
                    dbc.Col(
                        html.A(
                            "Data Source",
                            href="https://github.com/plotly/Figure-Friday/tree/main/2024/week-36",
                            target="_blank",
                            style=link_style
                        ),
                        className='text-center'
                    ),
                ],
                className='justify-content-center',
            )
        ],
        className='py-3',
        style={
            'background-color': BACKGROUND_COLOR,
            'position': 'fixed',
            'bottom': '0',
            'width': '100%',
            'box-shadow': f"0px 0px 8px {PRIMARY_COLOR_RGBA}",
            'z-index': '1000'
        }
    )
    return footer
                  