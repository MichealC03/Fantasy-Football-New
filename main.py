from flask import Flask, render_template, jsonify
import pandas as pd
from espn import df
from bigPlays import bigPlaysDf
from espnPosRk import merged_qbs_df
from espnPosRk import merged_rbs_df
from espnPosRk import merged_wrs_df
from espnPosRk import merged_tes_df

app = Flask(__name__)

@app.route('/')
def index():
    table1_html = df.to_html(classes='table table-striped table-bordered', index=False)
    #table2_html = bigPlaysDf.to_html(classes='table table-striped table-bordered', index=False)
    return render_template('index.html', table1=table1_html)

@app.route('/update_table/<table_name>')
def update_table(table_name):
    if table_name == 'qbs':
        table_html = merged_qbs_df.to_html(classes='table table-striped table-bordered', index=False)
    elif table_name == 'rbs':
        table_html = merged_rbs_df.to_html(classes='table table-striped table-bordered', index=False)
    elif table_name == 'wrs':
        table_html = merged_wrs_df.to_html(classes='table table-striped table-bordered', index=False)
    elif table_name == 'tes':
        table_html = merged_tes_df.to_html(classes='table table-striped table-bordered', index=False)
    else:
        table_html = bigPlaysDf.to_html(classes='table table-striped table-bordered', index=False)

    return jsonify({'table_html': table_html})

if __name__ == '__main__':
    app.run(debug=True)
