document.getElementById('urlForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    //Get the long URL from user
    const longUrl = document.getElementById('longUrl').value;

    //POST request to shorten the URL
    const response = await fetch('/shorten', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ long_url: longUrl }),
    });

    const data = await response.json();
    if (data.short_url) {
        //Display the short URL
        document.getElementById('result').innerHTML = `
            <p>Short URL: <a href="${data.short_url}" target="_blank">${data.short_url}</a></p>
        `;
    } else {
        // for an error, show this error message
        document.getElementById('result').innerHTML = `<p>Error: ${data.error}</p>`;
    }
});
