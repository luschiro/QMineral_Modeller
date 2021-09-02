import base64
import io
import os
import pandas as pd
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from web_app import about, table, plot, informations
import plotly.express as px


def encode_image(image_file):
    encoded = base64.b64encode(open(image_file, 'rb').read())
    return 'data:image/jpg;base64,{}'.format(encoded.decode())


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#To run Localhost
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, prevent_initial_callbacks=True)

#to run on Server
# app = dash.Dash(
#     __name__,
#     url_base_pathname='/qmin/',
#     external_stylesheets=external_stylesheets,
#     prevent_initial_callbacks=True
# )

server = app.server
app.title = 'Qmin'


def upload_card():
    """
    :return: A Div for upload data.
    """
    return html.Div([
        html.Div([
            html.Div(html.A('Template Data', href='assets/template.xls')),

            html.H4("Upload Files",
                    style={'text-align': 'center'}),
            html.B(),
            html.Div(className='row',
                     children=[html.P("  Column Separator:",
                                      className='four columns'),
                               dcc.Input(id='columns-separator',
                                         size='1', placeholder=',',
                                         className='two columns')]),
            html.Div(className='row',
                     children=[html.P("  Header Skip:",
                                      className='four columns'),
                               dcc.Input(id='header-skip',
                                         size='1',
                                         placeholder=0,
                                         className='two columns')]),
            html.Div(className='row',
                     children=[html.P("  Footer Skip:",
                                      className='four columns'),
                               dcc.Input(id='footer-skip',
                                         size='1',
                                         placeholder=0,
                                         className='two columns')])
        ]),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ], style={'text-align': 'center',
                      'right': '30%'}),
            style={
                'width': '50%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'display': 'block',
                'margin-left': 'auto',
                'margin-right': 'auto',
                'margin-top': '20px',
                'margin-bottom': '20px'},
            # Allow multiple files to be uploaded
            multiple=True
        ),
        html.Div(id='checkChange'),
        dcc.Checklist(
            id='checkDataProcedings',
            options=[
                {'label': 'I accept to agreggate my data in the training database of Qmin', 'value': 'true'},
            ],
            value=['true'],
            labelStyle={'display': 'inline-block'},
            style={'textAlign': 'center',
                   'display': 'block',
                   'margin-left': 'auto',
                   'margin-right': 'auto'}
        ),
        html.Div(
            id="remove_2",
            className="block",
            children=[]
        ),
        html.Div(id='download-name'),
        html.Div(id='remove'),

    ], className='item-a')


app.layout = html.Div(
    html.Div([
        html.Div(id='banner',
                 style={'width': '100%',
                        'background': "#262B3D",
                        'color': "#E2EFFA"},
                 children=[
                     html.A(id="dashbio-logo",
                            className='one columns',
                            children=[html.Img(src='assets/Qmin_logo.png',
                                               height='60',
                                               width='70',
                                               style={'top': '10',
                                                      'margin': '10px'})]),
                     html.H2('Mineral Chemistry Virtual Assistant',
                             className='five columns',
                             style={'font-size': '45px',
                                    'float': 'left'}),
                     html.A([
                         html.Img(src="assets/cprm_logo.png",
                                  height='70',
                                  width='152',
                                  style={'float': 'right'})
                     ], href='https://www.cprm.gov.br'),

                     html.A([
                         html.Img(src="assets/GitHub-Mark-Light-64px.png",
                                  style={'float': 'right'})
                     ],
                         href='https://github.com/gferrsilva/QMineral_Modeller')

                 ],
                 className='row'),

        html.Div(children=[
            html.Div(className='row',  # Define the row element
                     children=[
                         # Define the right element
                         html.Div(className='four columns div-user-controls',
                                  children=[upload_card(),
                                            html.Div(children=[
                                                html.H4('Video Tutorial of QMin'),
                                                html.Iframe(
                                                    src="https://www.youtube.com/embed/ege7MC3NQfM",
                                                    title="YouTube video player",

                                                )], className='item-a'),
                                            html.Div([
                                                html.Div(children=[html.H4("Contact"),
                                                                   html.P("Name:"),
                                                                   dcc.Input(id='nameEmail')
                                                                   ]),
                                                html.Div(children=[html.P("E-mail:"),
                                                                   dcc.Input(id='endEmail',
                                                                             type='email')
                                                                   ]),
                                                html.Div(children=[html.P("Issues:"),
                                                                   dcc.Textarea(
                                                                       id='textarea-state-email',
                                                                       value='',
                                                                       style={'width': '100%', 'height': 200},
                                                                   ),
                                                                   html.Button('Submit',
                                                                               id='textarea-state-example-button',
                                                                               n_clicks=0),
                                                                   html.Div(id='textarea-state-example-output',
                                                                            style={'whiteSpace': 'pre-line'})
                                                                   ])], className='item-a'),
                                            informations.about_card(),


                                            ]),


                         # Define the left element
                         html.Div(id='right_container',
                                  className='eight columns div-for-charts bg-grey',
                                  children=[html.Div([

                                      dcc.Tabs(
                                          id="tabs-with-classes",
                                          value='tab-table',
                                          parent_className='custom-tabs',
                                          className='custom-tabs-container',
                                          children=[
                                              dcc.Tab(id='General_tab',
                                                      label='Dataset',
                                                      value='tab-table',
                                                      className='custom-tab',
                                                      children=[
                                                          html.Div(id='output-data-upload',
                                                                   children=[
                                                                       html.H3('Upload your dataset',
                                                                               style={'text-align': 'center',
                                                                                      'padding': '320px'})
                                                                   ]),
                                                          html.Div(
                                                              id="download-area",
                                                              className="block",
                                                              children=[html.Form(
                                                                  action='',
                                                                  method="get",
                                                                  id='form-download',
                                                                  children=[
                                                                      html.Button(
                                                                          className="button",
                                                                          type="submit",
                                                                          children=["download"]
                                                                      )
                                                                  ])
                                                              ])
                                                      ]),

                                              dcc.Tab(id='graphic_tab',
                                                      label='Graphics',
                                                      value='graphic-table',
                                                      className='custom-tab',
                                                      children=[
                                                          html.Div(id='General_graphic',
                                                                   children=[
                                                                       html.H3('Upload your dataset',
                                                                               style={'text-align': 'center',
                                                                                      'padding': '320px'})
                                                                   ]),
                                                          html.Div(id='biplot_dropdown'),
                                                          html.Div(id='biplot-graphic'),
                                                          html.Div(id='triplot-dropdown'),
                                                          html.Div(id='triplot-graphic')
                                                      ]),

                                          ])],
                                      className='item-a'),
                                      informations.status_area(),

                                  ])
                     ])  # Define the right element
        ])
    ]))


def write_excel(df, dic_formula):
    import uuid
    import pandas as pd
   # from formula import append_df_to_excel

    filename = f"{uuid.uuid1()}.xlsx"
    relative_filename = os.path.join(
        'downloads',
        filename
    )
    if os.path.exists(relative_filename):
        os.remove(relative_filename)

    absolute_filename = os.path.join(os.getcwd(), relative_filename)
    writer = pd.ExcelWriter(absolute_filename, engine='xlsxwriter')
    df.to_excel(writer, sheet_name = 'QMIN')

    for key in dic_formula.keys():
        if len(dic_formula[key]) > 0:
            #append_df_to_excel(absolute_filename, dic_formula[key], sheet_name=key + '_formula')
            dic_formula[key].to_excel(writer, sheet_name = key + '_formula')

    writer.save()
    writer.close()

    return relative_filename


def parse_contents(contents, filename, date, write=False, sep=',',
                   decimalsep='.', headerskip=0, footerkip=0):
    import qmin
    sep = ','
    content_type, content_string = contents.split(sep)
    decoded = base64.b64decode(content_string)
    df = None
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file is CPRM style (evandro)
            df, dic_formulas = qmin.load_data_ms_web(io.StringIO(decoded.decode('ISO-8859-1')),
                                                     separator_diferent=sep, ftype='csv')
            # filename_output = write_excel(df)

        elif 'xls' in filename or 'xlsx' in filename:
            # Assume that the user uploaded an excel file
            # This excel is format of Microssonda!!!!
           # sep = ','
            content_type, content_string = contents.split(sep)
            decoded = base64.b64decode(content_string)

            df, dic_formulas = qmin.load_data_ms_web(io.BytesIO(decoded), ftype='xls')

        filename_output = write_excel(df, dic_formulas)

        # if write:
        #     filename_output = write_excel(df)
    except Exception as e:
        print(e)
        return html.Div([
            html.H5('There was an error processing this file.')
        ])

    return html.Div([
        html.H5('File loaded: ' + filename),
        # html.H4('Last modification in file: '+str(datetime.datetime.fromtimestamp(date))),

        dash_table.DataTable(
            id='table',
            style_table={
                'maxHeight': '500px',
                'overflowY': 'auto',
                'overflowX': 'scroll',
                'minWidth': '100%'
            },

            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            fixed_columns={'headers': True, 'data': 2},
            filter_action="native",
            sort_action="native",
            sort_mode='multi',
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                },
                {
                    'if': {'column_id': 'PREDICTED GROUP'},
                    'backgroundColor': '#4C5EA1',
                    'color': 'white'
                },
                {
                    'if': {'column_id': 'QC GROUP'},
                    'backgroundColor': '#4C5EA1',
                    'color': 'white'
                }

            ],

            style_header=
            {
                'backgroundColor': '#262B3D',
                'fontWeight': 'bold',
                'color': 'white'
            },
            style_cell=
            {
                'overflow': 'hidden',
                'textAlign': 'center',
                'textOverflow': 'ellipsis',
                'width': 'auto'
            }
        ),

        html.Hr(),
    ]), filename_output


def build_download_button(uri):
    """Generates a download button for the resource"""
    button = html.Form(
        action=uri,
        method="get",
        id='form-download',
        children=[
            html.Button(
                className="button",
                type="submit",
                children=[
                    "download"
                ]
            )
        ]
    )
    return button


def select_axis(df, feature, axis):
    return dict(
        args=[{axis: [df[feature]],
               'name': feature}],
        label=feature,
        method="update")


def makeAxis(title, tickangle):
    return {
        'title': title,
        'titlefont': {'size': 20},
        'tickangle': tickangle,
        'tickfont': {'size': 12},
        'tickcolor': 'rgba(0,0,0,0)',
        'ticklen': 5,
        'showline': True,
        'showgrid': True
    }


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('columns-separator', 'value'),
               State('upload-data', 'filename'),
               State('upload-data', 'last_modified'),
               State('header-skip', 'value'),
               State('footer-skip', 'value')
               ])
def update_output(list_of_contents, csep=',',  list_of_names='',
                  list_of_dates='', hs=2, fs=9):

    if csep == None:
        csep = ','
    if hs == None:
        hs = 0
    if fs == None:
        fs = 0

    print('separator', csep, type(csep))
    print('header-skip', hs)
    print('footer-skip', fs)
    if list_of_contents is not None:
        results = [
            parse_contents(c, n, d, sep=csep, headerskip=hs,
                           footerkip=fs) for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)]
        # results = [parse_contents(list_of_contents[0], list_of_names, list_of_dates,
        #                           sep=csep, decimalsep='.', headerskip=3, footerkip=6)]
        #print(results, len(results))
        if len(results) == 1:
            return results[0]
        children = [results[0][0]]


        return children
    else:
        return html.Div([html.H3('Upload your dataset', style={'text-align': 'center',
                                                               'padding': '320px'})])

@app.callback(
    Output("form-download", "action"),
    [Input('upload-data', 'contents'),
     Input('checkDataProcedings', 'value')],
    [State('columns-separator', 'value'),
     State('upload-data', 'filename'),
     State('upload-data', 'last_modified'),
     State('header-skip', 'value'),
     State('footer-skip', 'value')
     ])
def show_download_button(list_of_contents, teste='true', csep=',',
                         list_of_names='', list_of_dates='', hs=2, fs=9):

    if csep == None:
        csep = ','
    if hs == None:
        hs = 0
    if fs == None:
        fs = 0


    print('2separator', csep)

    if list_of_contents is not None:
        results = [
            parse_contents(c, n, d, sep=csep, headerskip=hs,
                           footerkip=fs) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        # results = [
        #     parse_contents(c, n, d, sep=csep) for c, n, d in
        #     zip(list_of_contents, list_of_names, list_of_dates)]
        # try:
        filename = results[0][1]
        # except:
        #     print('Error: Button filename Download')
        #     return ''
        test = 'true'
       # sendDataEmail(test, filename)
        return filename

    else:
        return None


@app.callback(Output('biplot_dropdown', 'children'),
            [Input('graphic_tab', 'value'),
             Input('form-download', 'action')],
            [State('upload-data', 'contents')])
def update_biplot_dropdown(tab, nameform, content):
    import numpy as np

    if content == None:
        return

    relative_filename = nameform

    try:
        df = pd.read_excel(relative_filename)
    except Exception:
        df = pd.read_excel(relative_filename, engine="openpyxl")


    features = df.columns.to_list()
    clean_features = []

    for name in features:
        if df[name].dtypes == np.float or df[name].dtypes == np.int64:
            clean_features.append(name)
    if tab == 'graphic-table':

        return html.Div([
        html.Div([
            dcc.Dropdown(
                id='bdropdown1',
                options=[{'label': i, 'value': i} for i in clean_features],
                value=clean_features[2]
            )], style={'width': '33%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                id='bdropdown2',
                options=[{'label': i, 'value': i} for i in clean_features],
                value=clean_features[3]
            )], style={'width': '33%', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                    id='bdropdown3',
                    options=[{'label': 'PREDICTED MINERAL', 'value': 'PREDICTED MINERAL'},
                             {'label': 'PREDICTED GROUP', 'value': 'PREDICTED GROUP'}],
                    value='PREDICTED MINERAL'
                )], style={'width': '24%', 'display': 'inline-block'}),
            html.Div(id='dd-output-container'),
        ], style={'passing': 10})
    else:
        return None


@app.callback(Output('biplot-graphic', 'children'),
              [Input('graphic_tab', 'value'),
               Input('bdropdown1', 'value'),
               Input('bdropdown2', 'value'),
               Input('bdropdown3', 'value'),
               Input('form-download', 'action')],
              [State('upload-data', 'contents')])
def update_biplot(tabs, dp1, dp2, dp3, nameform, contents):
    import plotly.express as px
    if tabs == 'graphic-table':

        if contents == None:
            return

        relative_filename = nameform

        args = {}
        if relative_filename.lower().endswith("xlsx"):
            args["engine"] = "openpyxl"

        df = pd.read_excel(relative_filename, **args)


        fig = px.scatter(df, x=df[dp1], y=df[dp2], color=df[dp3],
                         hover_data=['PREDICTED GROUP', 'PREDICTED MINERAL'])
        return html.Div([
            dcc.Graph(figure=fig)
        ])
    return None



@app.callback(Output('triplot-dropdown', 'children'),
            [Input('graphic_tab', 'value'),
             Input('form-download', 'action')],
            [State('upload-data', 'contents')])
def update_dropdown(tab, nameform, content):
    import numpy as np

    if content == None:
        return

    relative_filename = nameform

    try:
        df = pd.read_excel(relative_filename)
    except Exception:
        df = pd.read_excel(relative_filename, engine="openpyxl")

    features = df.columns.to_list()
    clean_features = []

    for name in features:
        if df[name].dtypes == np.float or df[name].dtypes == np.int64:
            clean_features.append(name)
    if tab == 'graphic-table':

        return html.Div([
        html.Div([
            dcc.Dropdown(
                id='dropdown1',
                options=[{'label': i, 'value': i} for i in clean_features],
                value=clean_features[2]
            )], style={'width': '24%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                id='dropdown2',
                options=[{'label': i, 'value': i} for i in clean_features],
                value=clean_features[3]
            )], style={'width': '24%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                id='dropdown3',
                options=[{'label': i, 'value': i} for i in clean_features],
                value=clean_features[4]
            )], style={'width': '24%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                id='dropdown4',
                options=[{'label': 'PREDICTED MINERAL', 'value': 'PREDICTED MINERAL'},
                         {'label': 'PREDICTED GROUP', 'value': 'PREDICTED GROUP'}],
                value='PREDICTED MINERAL'
            )], style={'width': '24%', 'display': 'inline-block'}),
            html.Div(id='dd-output-container'),
        ], style={'passing': 10})
    else:
        return None


@app.callback(Output('General_graphic', 'children'),
              [Input('graphic_tab', 'value'),
               Input('form-download', 'action')],
              [State('upload-data', 'contents')])
def update_graphic(tab, nameform, contents):
    # Callback for the first donut graphic in the graphic table

    if tab == 'graphic-table':

        if contents is not None:

            relative_filename = nameform
            try:
                df = pd.read_excel(relative_filename)
            except Exception:
                df = pd.read_excel(relative_filename, engine="openpyxl")
            fig = px.sunburst(df, path=['PREDICTED GROUP', 'PREDICTED MINERAL'])

            return html.Div([
                dcc.Graph(figure=fig)
            ])
        else:
            return html.Div([
                html.H3('Upload your dataset', style={'text-align': 'center', 'padding': '320px'})
            ])

    else:
        return html.Div([
            html.H3('Upload your dataset', style={'text-align': 'center', 'padding': '320px'})
        ])


@app.callback(
    Output('textarea-state-example-output', 'children'),
    [Input('textarea-state-example-button', 'n_clicks')],
    [State('textarea-state-email', 'value'),
     State('nameEmail', 'value'),
     State('endEmail', 'value')])
def update_output(n_clicks, value, name, endemail):
    if n_clicks > 0:
        sendEmail(value, name, endemail)
        return 'E-mail send!:'


def sendEmail(text, name = '', from_email=''):

    import smtplib
    from email.mime.text import MIMEText

    text = name + '\n\n' + from_email + '\n\n' + text
    msg = MIMEText(text)

    # Create a text/plain message

    msg['Subject'] = "USER COMUNICATION from QMIN"
    msg['From'] = "qmin.mineral@gmail.com"
    msg['To'] = "qmin.mineral@gmail.com"


    try:
        s = smtplib.SMTP_SSL('smtp.gmail.com')
        # s.login('postmaster@sandboxab11a79dd2474185afd6e9c69a4ac7ea.mailgun.org',
        #     'acbc4e8bdfa843cb4c66d3e2eddd579b-f7d0b107-2a58389a')
        s.login('qmin.mineral@gmail.com', 'iqlwncjdlwltfljo')
        s.sendmail(From, To, msg.as_string())
        s.quit()
    except:
        print("Erro desconhecido [app.py:730]: ({}) {}".format(e.__class__.__name__, e))

    return None


def sendDataEmail(teste, file_data):

    import smtplib
    from email.mime.application import MIMEApplication
    from email.mime.multipart import MIMEMultipart

    if teste == 'true':
     #   From = "postmaster@sandboxab11a79dd2474185afd6e9c69a4ac7ea.mailgun.org"
        From = 'qmin.mineral@gmail.com'
        To = "qmin.mineral@gmail.com"
        # Create a text/plain message
        msg = MIMEMultipart()

        msg['Subject'] = "Data from QMIN"
        msg['From'] = "qmin.mineral@gmail.com"
        msg['To'] = "qmin.mineral@gmail.com"

        filename = file_data
        fp = open(filename, 'rb')
        att = MIMEApplication(fp.read(), _subtype="xls")
        fp.close()
        att.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(att)

        s = smtplib.SMTP_SSL('smtp.gmail.com')

        # s.login('postmaster@sandboxab11a79dd2474185afd6e9c69a4ac7ea.mailgun.org',
        #     'acbc4e8bdfa843cb4c66d3e2eddd579b-f7d0b107-2a58389a')
        s.login('qmin.mineral@gmail.com','iqlwncjdlwltfljo')
        s.sendmail(From, To, msg.as_string())
        s.quit()

    return None


@app.callback(Output('triplot-graphic', 'children'),
               [Input('graphic_tab', 'value'),
                Input('dropdown1', 'value'),
                Input('dropdown2', 'value'),
                Input('dropdown3', 'value'),
                Input('dropdown4', 'value')],
              [State('form-download', 'action'),
               State('upload-data', 'contents')])
def update_triplot(tabs, dp1, dp2, dp3, dp4, nameform, contents):
    import plotly.express as px

    if tabs == 'graphic-table':

        if contents == None:
            return

        relative_filename = nameform

        args = {}
        if relative_filename.lower().endswith("xlsx"):
            args["engine"] = "openpyxl"

        try:
            df = pd.read_excel(relative_filename)
        except Exception:
            df = pd.read_excel(relative_filename, engine="openpyxl")

        if 'Total' in df.columns:
            fig = px.scatter_ternary(df,
                                     a=df[dp1], b=df[dp2],
                                     c=df[dp3], size_max=15,
                                     color=dp4, hover_name=df['PREDICTED MINERAL'],
                                     size=df['Total'])
        else:
            fig = px.scatter_ternary(df,
                                 a=df[dp1], b=df[dp2],
                                 c=df[dp3], size_max=15,
                                 color=dp4, hover_name=df['PREDICTED MINERAL'])
        return html.Div([
                dcc.Graph(figure=fig)
            ])
    else:
        return None


@app.server.route('/downloads/<path:path>')
def serve_static(path):
    import flask
    root_dir = os.getcwd()
    return flask.send_from_directory(
        os.path.join(root_dir, 'downloads'), path
    )


if __name__ == '__main__':
    app.server.run(port=8000, host='127.0.0.1', debug=True)
    #app.run_server(debug=True)
