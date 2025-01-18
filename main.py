import pandas as pd
import flask
from flask import Flask, request, jsonify, send_file
import io
import time
import re
import matplotlib
matplotlib.use('Agg')  # Ensure using 'Agg' backend for matplotlib
import matplotlib.pyplot as plt

# Data source: https://www.kaggle.com/datasets/ionaskel/nba-2k20-player-dataset

app = Flask(__name__)

# Global variables for A/B testing
visit_count = 0
click_A = 0
click_B = 0
locked_version = None

# Global variables for rate limiting and visitors
visitors = {}

# Global variable for subscriber count
num_subscribed = 0

@app.route('/')
def home():
    global visit_count, click_A, click_B, locked_version
    with open("index.html") as f:
        html = f.read()

    if visit_count == 10:
        # After 10 visits, determine which version is better based on clicks
        if click_A >= click_B:
            locked_version = 'A'
        else:
            locked_version = 'B'

    if visit_count < 10:
        if visit_count % 2 == 1:
            # Version A
            html = html.replace("VERSION_COLOR", "red").replace("VERSION_NAME", "A")
        else:
            # Version B
            html = html.replace("VERSION_COLOR", "purple").replace("VERSION_NAME", "B")
    else:
        # After 10 visits, show the locked version
        if locked_version == 'A':
            html = html.replace("VERSION_COLOR", "red").replace("VERSION_NAME", "A")
        else:
            html = html.replace("VERSION_COLOR", "purple").replace("VERSION_NAME", "B")
    visit_count += 1

    return html

@app.route('/browse.html')
def browse_handler():
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv("main.csv")
    # Convert the DataFrame to an HTML table
    html_table = df.to_html(float_format="{:.10f}".format)
    # Create the HTML content
    html_content = "<html><body><h1>Browse Data</h1>{}</body></html>".format(html_table)
    return html_content

@app.route('/browse.json')
def browse_json():
    client_ip = request.remote_addr
    current_time = time.time()

    if client_ip in visitors:
        last_visit_time = visitors[client_ip]
        if current_time - last_visit_time < 60:
            # Return 429 error code with Retry-After header
            retry_after = 60 - int(current_time - last_visit_time)
            return flask.Response(
                "Too many requests. Please try again later.",
                status=429,
                headers={"Retry-After": retry_after}
            )

    # Update the last visit time for the client IP
    visitors[client_ip] = current_time

    df = pd.read_csv("main.csv")
    data = df.to_dict(orient='records')

    return jsonify(data)

@app.route('/visitors.json')
def visitors_json():
    # Return the list of visitor IPs who have accessed browse.json
    return jsonify(list(visitors.keys()))

@app.route('/donate.html')
def donate():
    global click_A, click_B
    from_version = request.args.get('from')
    if from_version == 'A':
        click_A += 1
    elif from_version == 'B':
        click_B += 1

    with open('donate.html') as f:
        html = f.read()
    return html

@app.route('/email', methods=["POST"])
def email():
    global num_subscribed
    email_address = str(request.data, "utf-8")
    # Validate email format: abc@xyz.lmn where lmn is exactly 3 letters
    if len(re.findall(r"^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.([a-zA-Z]{3})$", email_address)) > 0:
        with open("emails.txt", "a") as f:
            f.write(email_address + "\n")
        num_subscribed += 1
        return jsonify(f"thanks, your subscriber number is {num_subscribed}!")
    # Sternly warn the user for invalid email
    return jsonify("Invalid Email Address. Please enter a valid email.")

# Dashboard routes

@app.route('/plot1.svg')
def plot1():
        df = pd.read_csv('main.csv')
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
        df = df.dropna(subset=['rating'])

        bins = request.args.get('bins', default=10, type=int)

        fig, ax = plt.subplots()
        ax.hist(df['rating'], bins=bins)
        ax.set_xlabel('Player Rating')
        ax.set_ylabel('Frequency')
        ax.set_title(f'Histogram of Player Ratings with {bins} bins')

        img = io.BytesIO()
        fig.savefig(img, format='svg')
        img.seek(0)
        plt.close(fig)
        filename = "dashboard1-query.svg" if"bins" in request.args else "dashboard1.svg"
        return flask.Response(img.getvalue(), content_type='image/svg+xml')

@app.route('/plot2.svg')
def plot2():
        df = pd.read_csv('main.csv')
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
        df['draft_year'] = pd.to_numeric(df['draft_year'], errors='coerce')
        df = df.dropna(subset=['rating', 'draft_year'])

        fig, ax = plt.subplots()
        ax.scatter(df['draft_year'], df['rating'])
        ax.set_xlabel('Draft Year')
        ax.set_ylabel('Player Rating')
        ax.set_title('Player Rating vs Draft Year')

        img = io.BytesIO()
        fig.savefig(img, format='svg')
        img.seek(0)
        plt.close(fig)
        filename = "dashboard2.svg" 
        return flask.Response(img.getvalue(), content_type='image/svg+xml')

# Save the plots locally for grading

def save_dashboard_plots():
    try:
        df = pd.read_csv('main.csv')
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
        df['draft_year'] = pd.to_numeric(df['draft_year'], errors='coerce')
        df = df.dropna(subset=['rating', 'draft_year'])

        # Generate dashboard1.svg with bins=10
        fig, ax = plt.subplots()
        ax.hist(df['rating'], bins=10)
        ax.set_xlabel('Player Rating')
        ax.set_ylabel('Frequency')
        ax.set_title('Histogram of Player Ratings with 10 bins')
        fig.savefig('dashboard1.svg')
        plt.close(fig)
        print("Saved dashboard1.svg")

        # Generate dashboard1-query.svg with bins=100
        fig, ax = plt.subplots()
        ax.hist(df['rating'], bins=100)
        ax.set_xlabel('Player Rating')
        ax.set_ylabel('Frequency')
        ax.set_title('Histogram of Player Ratings with 100 bins')
        fig.savefig('dashboard1-query.svg')
        plt.close(fig)
        print("Saved dashboard1-query.svg")

        # Generate dashboard2.svg
        fig, ax = plt.subplots()
        ax.scatter(df['draft_year'], df['rating'])
        ax.set_xlabel('Draft Year')
        ax.set_ylabel('Player Rating')
        ax.set_title('Player Rating vs Draft Year')
        fig.savefig('dashboard2.svg')
        plt.close(fig)
        print("Saved dashboard2.svg")

    except Exception as e:
        print("Error in save_dashboard_plots:", e)

if __name__ == '__main__':
    save_dashboard_plots()
    app.run(host="0.0.0.0", debug=True, threaded=False)  # Don't change this line!
