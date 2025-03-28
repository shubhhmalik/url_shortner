from flask import Flask, request, redirect, render_template
import sqlite3
import hashlib

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('url_shortener.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS urls
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  long_url TEXT NOT NULL,
                  short_url TEXT NOT NULL UNIQUE)''')
    conn.commit()
    conn.close()

def generate_short_url(long_url):
    hash_object = hashlib.md5(long_url.encode())
    return hash_object.hexdigest()[:8] 
    
init_db()


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():

    long_url = request.form.get('long_url')                      #Get the long URL
    if not long_url:
        return render_template('index.html', error='Missing long URL')

    short_url = generate_short_url(long_url)

    conn = sqlite3.connect('url_shortener.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO urls (long_url, short_url) VALUES (?, ?)', (long_url, short_url))
        conn.commit()
    except sqlite3.IntegrityError:

        c.execute('SELECT short_url FROM urls WHERE long_url = ?', (long_url,))
        result = c.fetchone()
        short_url = result[0] if result else short_url
    conn.close()

    return render_template('index.html', short_url=f'http://localhost:5000/{short_url}')


@app.route('/<short_url>', methods=['GET'])
def redirect_to_long_url(short_url):

    conn = sqlite3.connect('url_shortener.db')
    c = conn.cursor()
    c.execute('SELECT long_url FROM urls WHERE short_url = ?', (short_url,))
    result = c.fetchone()
    conn.close()

    if result:
        return redirect(result[0])
    else:
        return render_template('index.html', error='URL not found')


if __name__ == '__main__':
    app.run(debug=True) 


    

#QUICK NOTES for recruiters
#Line 5 : Initialization of Flask
#Line 7-9 : Database connection setup
#Line 11-14 : Creates a table to store URLs
#Line 18-20 : Long to Short url generation
#Line 25-27 : Homepage route
#Line 29-50 : Shorten URL endpoint
#Line 53-65 : Redirection
#Line 68,69 : Runs Flask in debug mode
