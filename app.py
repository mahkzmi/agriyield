import dash
from dash import dcc, html
import plotly.graph_objects as go
from dash.dependencies import Input, Output

# ایجاد اپ Dash
app = dash.Dash(__name__, external_stylesheets=['assets/styles.css'])

# طراحی رابط کاربری
app.layout = html.Div(className="container", children=[
    html.H1("پیش‌بینی عملکرد محصول"),
    html.Div(className="card", children=[
        html.Label("دمای روزانه (سانتی‌گراد):"),
        dcc.Input(id='temperature', type='number', value=25, step=0.1),

        html.Label("بارش (میلی‌متر):"),
        dcc.Input(id='rainfall', type='number', value=50, step=1),

        html.Label("نوع خاک:"),
        dcc.Dropdown(
            id='soil-type',
            options=[
                {'label': 'شنی', 'value': 'sandy'},
                {'label': 'لومی', 'value': 'loamy'},
                {'label': 'رسوبی', 'value': 'clay'}
            ],
            value='loamy'
        ),

        html.Label("میزان آبیاری (لیتر/هکتار):"),
        dcc.Input(id='irrigation', type='number', value=100, step=10),

        html.Div(id='result-output'),

        html.Button('دانلود خروجی', id='download-btn', n_clicks=0),
    ])
])

# تابع پیش‌بینی
def predict_yield(temperature, rainfall, soil_type, irrigation):
    base_yield = 100  # مقدار پایه عملکرد (مثلاً 100 کیلوگرم در هکتار)

    yield_adjustment_by_temp = -0.5 * (temperature - 25)
    yield_adjustment_by_rainfall = 0.2 * rainfall

    if soil_type == 'sandy':
        soil_factor = 0.8
    elif soil_type == 'loamy':
        soil_factor = 1.0
    else:
        soil_factor = 1.2

    yield_adjustment_by_irrigation = 0.3 * irrigation

    total_yield = base_yield + yield_adjustment_by_temp + yield_adjustment_by_rainfall
    total_yield *= soil_factor
    total_yield += yield_adjustment_by_irrigation
    
    return total_yield

# به‌روزرسانی خروجی
@app.callback(
    Output('result-output', 'children'),
    Input('temperature', 'value'),
    Input('rainfall', 'value'),
    Input('soil-type', 'value'),
    Input('irrigation', 'value')
)
def update_output(temperature, rainfall, soil_type, irrigation):
    yield_prediction = predict_yield(temperature, rainfall, soil_type, irrigation)
    return f"عملکرد تخمینی: {yield_prediction:.2f} کیلوگرم در هکتار"

if __name__ == '__main__':
    app.run_server(debug=True)