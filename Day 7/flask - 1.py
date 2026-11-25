from flask import Flask, request, jsonify
import pandas as pd
import sqlite3
import openai

app = Flask(_name_)

# Load datasets
ad_sales_df = pd.read_csv("datasets/ad_sales.csv")
total_sales_df = pd.read_csv("datasets/total_sales.csv")
eligibility_df = pd.read_csv("datasets/eligibility.csv")

# Create SQLite DB
conn = sqlite3.connect("ecommerce.db", check_same_thread=False)
ad_sales_df.to_sql("ad_sales", conn, if_exists="replace", index=False)
total_sales_df.to_sql("total_sales", conn, if_exists="replace", index=False)
eligibility_df.to_sql("eligibility", conn, if_exists="replace", index=False)

# Configure your OpenAI key
openai.api_key = "your_openai_api_key_here"

# Helper to query OpenAI for SQL generation
def generate_sql(query):
    prompt = f"""
    You are a data analyst. Write a SQL query for this question:
    '{query}'
    The database has these tables:
    1. ad_sales(ad_id, product_id, impressions, clicks, spend, date)
    2. total_sales(product_id, units_sold, revenue, date)
    3. eligibility(product_id, is_active, is_eligible, category)
    Use SQLite dialect.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]

# Route to receive questions and return answers
@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("question", "")
    try:
        sql_query = generate_sql(user_input)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        data = [dict(zip(columns, row)) for row in result]
        return jsonify({"query": sql_query, "result": data})
    except Exception as e:
        return jsonify({"error": str(e)})

# Health check endpoint
@app.route("/")
def home():
    return "E-commerce AI Agent is running!"

if _name_ == "_main_":
    app.run(debug=True)