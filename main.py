from flask import Flask, jsonify, render_template
import os
import json
import psycopg2
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
connection = psycopg2.connect(                                                  
    user = os.getenv("PGUSER"),                                      
    password = os.getenv("PGPASSWORD"),                                  
    host = os.getenv("PGHOST"),                                            
    port = os.getenv("PGPORT"),                                          
    database = os.getenv("PGDATABASE")                                 
)          
# url = os.getenv("DATABASE_URL")

# connection = psycopg2.connect(url)

@app.route('/')
def index():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('Select * from cars;')
            data = cursor.fetchall()
    return render_template('index.html', data=data)

@app.route("/api/car/<int:n>", methods=['GET'])
def get_info_taxi(n):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('Select taxi_name, tarif_name, price from taxi, choice, cars where cars.car_id = {0} AND taxi.taxi_id = choice.tarif_id AND Cars.car_id = choice.car_id;'.format(n))
            data = cursor.fetchall()
    

    return render_template('data.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
