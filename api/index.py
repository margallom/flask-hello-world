from flask import Flask,render_template
import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Fetch variables
CONNECTION = os.getenv("connection")

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

@app.route('/sensor')
def sensor():
    # Connect to the database
    try:
        connection = psycopg2.connect(
            CONNECTION
        )
        print("Connection successful!")
        
        # Create a cursor to execute SQL queries
        cursor = connection.cursor()
        
        # Example query
        cursor.execute("SELECT NOW();")
        result = cursor.fetchone()
        print("Current Time:", result)
    
        # Close the cursor and connection
        cursor.close()
        connection.close()
        print("Connection closed.")
        return (f"Current Time: , {result}")
    except Exception as e:
        return(f"Failed to connect: {e}")
@app.route('/pagina')
def pagina():
    return render_template("pagina.html")
    
@app.route("/sensor/<int:sensor_id>")
def get_sensor(sensor_id):
    try:
        conn = psycopg2.connect(
            CONNECTION
        )
        cur = conn.cursor()

        # Get the latest 10 values
        cur.execute("""
            SELECT valor, created_at
            FROM sensor1
            WHERE sensor_id = %s
            ORDER BY created_at DESC
            LIMIT 10;
        """, (sensor_id,))
        rows = cur.fetchall()

        # Convert to lists for graph
        values = [r[0] for r in rows][::-1]        # reverse for chronological order
        timestamps = [r[1].strftime('%Y-%m-%d %H:%M:%S') for r in rows][::-1]
        
        return render_template("sensor.html", sensor_id=sensor_id, values=values, timestamps=timestamps, rows=rows)

    except Exception as e:
        return f"<h3>Error: {e}</h3>"

    finally:
        if 'conn' in locals():
            conn.close()


