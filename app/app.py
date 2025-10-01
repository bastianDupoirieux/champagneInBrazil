
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('index.html')

@app.route('/wine_data', methods=['POST'])
def submit_form():
    name = request.form['name']
    domain = request.form['domain']
    producer = request.form['producer']
    vintage = request.form['vintage']
    date_bought = request.form['date_bought']

    # Create a DataFrame and append it to a CSV file
    df = pd.DataFrame([[name, domain, producer, vintage, date_bought]],
                      columns=['Name', 'Domaine', 'Producer', 'Vintage', 'Date Bought'])
    df.to_csv('wine_data.csv', mode='a', header=not pd.io.common.file_exists('wine_data.csv'), index=False)

    return redirect(url_for('form'))


if __name__ == '__main__':
    app.run(debug = True)
