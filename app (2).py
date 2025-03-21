from flask import Flask, request, render_template
import mysql.connector as con

app = Flask(__name__)

# Database connection
connection = con.connect(
    host="localhost",
    user="root",
    password="jillabala",
    database="magazine_db"
)

# Create table for magazine_db database if not exists
mycursor = connection.cursor(dictionary=True)
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS month_06_2024 (
        event_id INT AUTO_INCREMENT PRIMARY KEY,
        event_name VARCHAR(255) NOT NULL,
        event_description TEXT NOT NULL,
        event_date DATE NOT NULL,
        event_image TEXT
    );
""")

# Insert a sample record
mycursor.execute("""
    INSERT INTO month_06_2024 (
        event_name,
        event_description,
        event_date,
        event_image
    ) VALUES (
        'nature',
        'Nature is all the animals, plants, and other things in the world that are not made by people, and all the events and processes that are not caused by people. The most amazing thing about nature is its infinite variety.',
        '2024-05-01',  
        'nature.jpg'
    )
""")
connection.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        month = request.form['month']
        year, month_num = month.split('-')
        table_name = f"month_{month_num}_{year}"
        print(table_name)  

        mycursor.execute(f"SELECT * FROM {table_name}")
        result = mycursor.fetchall()
        print(result)
        
        return render_template('result.html', result=result)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
