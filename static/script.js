document.getElementById('urlForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const longUrl = document.getElementById('longUrl').value;

    const response = await fetch('/shorten', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ long_url: longUrl }),
    });

    const data = await response.json();
    if (data.short_url) {
        document.getElementById('result').innerHTML = `
            <p>Short URL: <a href="${data.short_url}" target="_blank">${data.short_url}</a></p>
        `;
    } else {
        document.getElementById('result').innerHTML = `<p>Error: ${data.error}</p>`;
    }
});