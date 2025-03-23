from flask import Flask, request, jsonify, redirect, render_template
import sqlite3
import hashlib

# Initialize Flask
app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('url_shortener.db')
    c = conn.cursor()
    
    # Create a table to store URLs
    c.execute('''CREATE TABLE IF NOT EXISTS urls
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  long_url TEXT NOT NULL,
                  short_url TEXT NOT NULL UNIQUE)''')
    conn.commit()
    conn.close()

init_db()

#Long to Short url generation
def generate_short_url(long_url):
    hash_object = hashlib.md5(long_url.encode())
    return hash_object.hexdigest()[:8]  # Use first 8 characters of the hash

# Endpoint to shorten URL
@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.json.get('long_url')
    if not long_url:
        return jsonify({'error': 'Missing long_url'}), 400

    short_url = generate_short_url(long_url)

    # Save to database
    conn = sqlite3.connect('url_shortener.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO urls (long_url, short_url) VALUES (?, ?)', (long_url, short_url))
        conn.commit()
    except sqlite3.IntegrityError:
        # If short_url already exists, fetch the existing one
        c.execute('SELECT short_url FROM urls WHERE long_url = ?', (long_url,))
        result = c.fetchone()
        short_url = result[0] if result else short_url
    conn.close()
    #Return the short URL
    return jsonify({'short_url': f'http://localhost:5000/{short_url}'})

# Endpoint to redirect to original URL
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
        return jsonify({'error': 'URL not found'}), 404

# Serve the frontend
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)   #run flask in debug mode
