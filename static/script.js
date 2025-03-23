// Step 1: Find the form
var form = document.getElementById('urlForm');

form.addEventListener('submit', function (event) {
    
    // Step 2: Stop the refreshing of page
    event.preventDefault();

    // Step 3: Get the long URL
    var longUrl = document.getElementById('longUrl').value;

    // Step 4: Send the long URL to the server to shorten it
    // (Create an object for the data to send)
    var dataToSend = {
        long_url: longUrl
    };

    // Step 5: Send the data to the server, using fetch
    fetch('/shorten', {
        method: 'POST',            //Use the POST method
        headers: {
            'Content-Type': 'application/json'   // Telling server we're sending JSON
        },
        body: JSON.stringify(dataToSend)   // Convert the data to JSON and send it
    })
    .then(function (response) {
        // Step 6: Convert it to JSON
        return response.json();
    })
    .then(function (data) {
        // Step 7: If the server returned a short URL, display it
        if (data.short_url) {
            var resultDiv = document.getElementById('result');
            resultDiv.innerHTML = '<p>Short URL: <a href="' + data.short_url + '" target="_blank">' + data.short_url + '</a></p>';
        } else {
            // Step 9: Incase of error, show the error message
            var resultDiv = document.getElementById('result');
            resultDiv.innerHTML = '<p>Error: ' + data.error + '</p>';
        }
    })
    .catch(function (error) {
        // Step 10: If fetch doesn't work, show this error
        console.error('Error:', error);
        var resultDiv = document.getElementById('result');
        resultDiv.innerHTML = '<p>Something went wrong. Please try again.</p>';
    });
});
