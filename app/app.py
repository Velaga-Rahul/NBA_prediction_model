import mysql.connector as mc
import json
import pandas as pd
from datetime import datetime, timedelta
from flask import Flask, render_template

def sqlTodf(query:str, creds:dict) -> pd.DataFrame:

    with mc.connect(**creds) as conn:
        cur = conn.cursor()

        cur.execute(query)
        column_names = [column[0] for column in cur.description]
        rows = cur.fetchall()
        
    data = pd.DataFrame(rows, columns=column_names)
    
    return data

today = datetime.now()
todayDate = today.strftime('%Y-%m-%d')
year = today.year + 1
with open('creds.json') as file:
    creds = json.load(file)

query = '''
select home_id, home, visitor_id, visitor from games where date = '{}'
'''.format(todayDate)

data = sqlTodf(query, creds).astype(str)

app = Flask(__name__)

@app.route('/')
def today():
    return render_template('index.html', columns = data.columns, df=data)


@app.route('/game/<home_id>/<visitor_id>')
def game(home_id, visitor_id):

    logoQuery = '''
    select * from abbrev where id in ({}, {})
    '''.format(home_id, visitor_id)

    logos = sqlTodf(logoQuery, creds)

    teamQuery = '''
    select * from conference_standings where team_id in ({}, {}) and year={}
    '''.format(home_id, visitor_id, year)

    team = sqlTodf(teamQuery, creds)

    home_team, visitor_team = logos[logos['ID'] == int(home_id)]['Team'].iloc[0], logos[logos['ID'] == int(visitor_id)]['Team'].iloc[0]

    return render_template('game.html', home_id = home_id, visitor_id = visitor_id, home_team=home_team, visitor_team=visitor_team, team=team)

if __name__ == "__main__":
    app.run(debug=True)