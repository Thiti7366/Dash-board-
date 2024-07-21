import dash
from dash import dcc, html, Input, Output
import pandas as pd
import requests
import plotly.express as px

app = dash.Dash(__name__)

url = 'https://gpa.obec.go.th/reportdata/pp3-4_2566_province.json'
response = requests.get(url)
data = response.json()

df = pd.DataFrame(data)

df['totalmale'] = pd.to_numeric(df['totalmale'], errors='coerce')
df['totalfemale'] = pd.to_numeric(df['totalfemale'], errors='coerce')
df['totalstd'] = pd.to_numeric(df['totalstd'], errors='coerce')

province_data = {
    'province': [
        'กระบี่', 'กรุงเทพมหานคร', 'กาญจนบุรี', 'กาฬสินธุ์', 'กำแพงเพชร', 'ขอนแก่น', 'จันทบุรี', 'ฉะเชิงเทรา',
        'ชลบุรี', 'ชัยนาท', 'ชัยภูมิ', 'ชุมพร', 'ตรัง', 'ตราด', 'ตาก', 'นครนายก', 'นครปฐม', 'นครพนม', 'นครราชสีมา',
        'นครศรีธรรมราช', 'นครสวรรค์', 'นนทบุรี', 'นราธิวาส', 'น่าน', 'บึงกาฬ', 'บุรีรัมย์', 'ปทุมธานี', 'ประจวบคีรีขันธ์',
        'ปราจีนบุรี', 'ปัตตานี', 'พระนครศรีอยุธยา', 'พะเยา', 'พังงา', 'พัทลุง', 'พิจิตร', 'พิษณุโลก', 'ภูเก็ต', 'มหาสารคาม',
        'มุกดาหาร', 'ยะลา', 'ยโสธร', 'ระนอง', 'ระยอง', 'ราชบุรี', 'ร้อยเอ็ด', 'ลพบุรี', 'ลำปาง', 'ลำพูน', 'ศรีสะเกษ',
        'สกลนคร', 'สงขลา', 'สตูล', 'สมุทรปราการ', 'สมุทรสงคราม', 'สมุทรสาคร', 'สระบุรี', 'สระแก้ว', 'สิงห์บุรี',
        'สุพรรณบุรี', 'สุราษฎร์ธานี', 'สุรินทร์', 'สุโขทัย', 'หนองคาย', 'หนองบัวลำภู', 'อำนาจเจริญ', 'อุดรธานี',
        'อุตรดิตถ์', 'อุทัยธานี', 'อุบลราชธานี', 'อ่างทอง', 'เชียงราย', 'เชียงใหม่', 'เพชรบุรี', 'เพชรบูรณ์', 'เลย',
        'แพร่', 'แม่ฮ่องสอน'
    ],
    'latitude': [
        8.05917, 13.72917, 14.01944, 16.43417, 16.48111, 16.43889, 12.60861, 13.69028, 13.36222, 15.18722,
        15.80556, 10.49389, 7.5575, 12.3025, 16.89667, 14.1224, 13.81556, 17.40694, 14.975, 8.43636,
        15.71333, 13.85083, 6.42639, 18.78333, 18.2204, 14.99417, 14.05, 11.81667, 14.05667, 6.86778,
        14.35361, 19.16528, 8.46444, 7.61667, 16.44306, 16.81583, 7.88, 16.17722, 16.54306, 6.5425,
        15.79722, 10.03917, 12.67417, 13.53556, 16.05306, 14.8, 18.28611, 18.58639, 15.11444, 17.15639,
        7.20611, 6.61472, 13.59556, 13.41972, 13.54861, 14.52861, 13.8222, 14.89111, 14.4675, 9.13972,
        14.88, 17.00583, 17.87444, 17.20417, 15.85, 17.53917, 17.62306, 15.2999, 15.22806, 14.5925,
        19.90944, 18.79028, 13.11194, 16.42417, 17.48528, 18.14528, 19.30111
    ],
    'longitude': [
        98.91889, 100.52389, 99.53111, 103.50917, 99.52222, 102.82861, 102.10389, 101.07028, 100.98333, 100.12833,
        102.03111, 99.18, 99.61028, 102.5125, 99.01333, 101.0712, 100.03722, 104.78083, 102.1, 99.96306,
        100.13528, 100.52222, 101.81528, 100.78333, 103.6363, 103.10222, 100.48333, 99.8, 101.37389, 101.25,
        100.56917, 99.90361, 98.53167, 100.083333, 100.34667, 100.26361, 98.3925, 103.30083, 104.72278, 101.28306,
        104.14306, 98.6125, 101.27889, 99.81333, 103.65111, 100.62694, 99.51306, 99.01194, 104.32028, 104.14556,
        100.59667, 100.06806, 100.60722, 100.00167, 100.2775, 100.91139, 102.066, 100.40306, 100.11694, 99.33056,
        103.49, 99.82639, 102.73833, 102.44444, 104.63333, 102.78444, 100.09583, 99.4562, 104.85944, 100.45722,
        99.8275, 98.96056, 99.94583, 101.15472, 101.73028, 100.14794, 97.97
    ]
}

geo_df = pd.DataFrame(province_data)

df = df.merge(geo_df, left_on='schools_province', right_on='province')

total_male = df['totalmale'].sum()
total_female = df['totalfemale'].sum()
total_std = df['totalstd'].sum()

dropdown_options = [{'label': province, 'value': province} for province in df['province'].unique()]

app.layout = html.Div([
   
    html.Div([
        html.H1(
            'จำนวนนักเรียนระดับมัธยมศึกษาปีที่ 6 ในปีการศึกษา 2566 แยกตามจังหวัด',
            style={'textAlign': 'center', 'margin': '20px'}
        )
    ], style={'display': 'flex', 'justifyContent': 'center'}),

    html.Div([
        html.Div([
            dcc.Graph(
                id='pie-chart',
                figure={
                    'data': [
                        {
                            'labels': ['เพศชาย', 'เพศหญิง'],
                            'values': [total_male, total_female],
                            'type': 'pie',
                            'name': 'จำนวนนักเรียน'
                        }
                    ],
                    'layout': {
                        'title': 'จำนวนนักเรียนแยกตามเพศในทุกจังหวัด',
                        'title_x': 0.5,
                        'title_font': {'size': 24}
                    }
                }
            ),
            html.Div(f'จำนวนนักเรียนทั้งหมดในทุกจังหวัด: {total_std} คน')
        ], style={'flex': '1', 'padding': '10px', 'border': '1px solid black', 'margin': '10px'}),

        html.Div([
            dcc.Graph(id='map-graph'),
        ], style={'flex': '1', 'padding': '10px', 'border': '1px solid black', 'margin': '10px'})
    ], style={'display': 'flex'}),

    html.Div([
        html.H2(id='total-students-header'),
        dcc.Dropdown(
            id='province-dropdown',
            options=dropdown_options,
            value='นครศรีธรรมราช' 
        ),
        dcc.Graph(id='example-graph'),
        html.Div(id='total-students')
    ], style={'border': '1px solid black', 'padding': '10px', 'margin': '10px'})
])


@app.callback(
    Output('example-graph', 'figure'),
    [Input('province-dropdown', 'value')]
)
def update_bar_graph(selected_province):
    filtered_df = df[df['schools_province'] == selected_province]
    
    bar_fig = {
        'data': [
            {'x': ['เพศชาย', 'เพศหญิง'], 
             'y': [filtered_df['totalmale'].iloc[0], filtered_df['totalfemale'].iloc[0]], 
             'type': 'bar', 
             'name': 'จำนวนนักเรียน',
             'marker': {'color': ['orange', 'blue']}  # Set color for male and female
            },
        ],
        'layout': {
            'title': f'จำนวนนักเรียนแยกตามเพศในจังหวัด {selected_province}',
            'xaxis': {'title': 'เพศ'},
            'yaxis': {'title': 'จำนวนนักเรียน'},
            'title_x': 0.5,
            'title_font': {'size': 24}
        }
    }
    return bar_fig

@app.callback(
    Output('map-graph', 'figure'),
    [Input('province-dropdown', 'value')]
)
def update_map(selected_province):
    map_fig = px.scatter_geo(
        df,
        lat='latitude',
        lon='longitude',
        size='totalstd',
        hover_name='province',
        color='totalstd',
        title='แผนที่จำนวนนักเรียนในแต่ละจังหวัด',
        template='plotly_dark'
    )
    map_fig.update_layout(title_x=0.5, title_font={'size': 18})
    return map_fig

@app.callback(
    Output('total-students', 'children'),
    [Input('province-dropdown', 'value')]
)
def update_total_students(selected_province):
    filtered_df = df[df['schools_province'] == selected_province]
    
    total_students = filtered_df['totalstd'].iloc[0]
    total_male = filtered_df['totalmale'].iloc[0]
    total_female = filtered_df['totalfemale'].iloc[0]
    
    return (
        f'จำนวนนักเรียนทั้งหมดในจังหวัด {selected_province}: {total_students} คน\n'
        f'จำนวนนักเรียนชาย: {total_male} คน\n'
        f'จำนวนนักเรียนหญิง: {total_female} คน'
    )

@app.callback(
    Output('total-students-header', 'children'),
    [Input('province-dropdown', 'value')]
)
def update_total_students_header(selected_province):
    return f'จำนวนนักเรียนทั้งหมดในจังหวัด {selected_province}'

if __name__ == '__main__':
    app.run_server(debug=True)
