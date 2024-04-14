# import os
from config import DATABASE, DATABASE_2
import psycopg2
# from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for

# load_dotenv()
app = Flask(__name__)
# DB = os.getenv("DATABASE")
# print(DB)


connection = psycopg2.connect(dbname=DATABASE["dbname"], host=DATABASE["host"], user=DATABASE["user"],
                              password=DATABASE["password"], port=DATABASE["port"])

connection_rainbow = psycopg2.connect(dbname=DATABASE_2["dbname"], host=DATABASE_2["host"], user=DATABASE_2["user"],
                              password=DATABASE_2["password"], port=DATABASE_2["port"])


INSERT_PROD = "INSERT INTO products (name, type_product) VALUES ('carrot', 'Veg');"
connection.autocommit = True

psql = "CREATE DATABASE clients;"

with connection.cursor() as cursor:
    # cursor.execute(psql)
    print("psql was create")
    # cursor.execute("SELECT * FROM products;")
    # cursor.execute(INSERT_PROD)
    # print(cursor.fetchall())

with connection_rainbow.cursor() as cursor:
    cursor.execute("SELECT * FROM students;")
    # print(cursor.fetchone())
    # print(cursor.fetchone())

@app.route("/succes")
def get_database():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM clients;")
        database_list = cursor.fetchall()
    return render_template("data.html", data=database_list)


CREATE_CLIENTS_TABLE = "CREATE TABLE IF NOT EXISTS clients(id SERIAL PRIMARY KEY,name VARCHAR(50),email TEXT);"
INSERT_CLIENTS_TABLE = "INSERT INTO clients (name, email) VALUES (%s, %s);"

@app.route("/create", methods=['POST','GET'])
def create_client():
    if request.method == 'POST':
        name = request.form["nm"]
        email = request.form["email"]
        print(name,email)
        with connection.cursor() as cursor:
            cursor.execute(CREATE_CLIENTS_TABLE)
            cursor.execute(INSERT_CLIENTS_TABLE, (name,email, ))
            print("Success")
            return redirect(url_for('get_database'))
    else:
        print("not all")

    return render_template("create.html")



