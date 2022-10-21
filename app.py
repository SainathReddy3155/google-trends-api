

from flask import Flask, make_response,render_template,request, session,url_for,jsonify
from flask.helpers import url_for
from flask_mysqldb import MySQL
from werkzeug.utils import redirect
import pandas as pd
import sys
import json
import requests
import pandas as pd
import sys
import simplejson as json
from pytrends.request import TrendReq

app=Flask(__name__)
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'report_logs_data_damo'

mysql = MySQL(app)



@app.route('/',methods=["POST","GET"])
def index():
    if request.method=="POST":
        keyword=request.form.get("keyword")
        pytrend = TrendReq()
        pytrend.build_payload(kw_list=[keyword],geo="IN")
        df = pytrend.interest_by_region()
        statewise=df.to_json()
        related_queries = pytrend.related_queries()
        queries = related_queries.values()
        queries=list(queries)
        dataframe=pd.DataFrame(queries)
        interestovertime=pytrend.interest_over_time()
        interestovertime = interestovertime.reset_index() 
        datewise=interestovertime.to_json(orient='records', date_format='iso', date_unit='s')
        keywords=dataframe.to_json()
        finaljson='[{"statewise":'+statewise+'},{"keywords":'+keywords+'},{"datewise":'+datewise+'}]' 
    return finaljson

# @app.route('/keywordwise',methods=["POST"])
# def keywordwise():
#     if request.method=="POST":
#         keywordwise=request.form.get("keywordwise")
#         print(keywordwise)
#         pytrend = TrendReq()
#         related_queries = pytrend.related_queries()
#         keywordwisedata=related_queries.values()
#         pri
#     return "hello"







if __name__=='__main__':
    app.run(debug=True,port=9000)