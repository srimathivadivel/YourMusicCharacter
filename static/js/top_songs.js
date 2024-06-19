// The code listens for the DOMContentLoaded event, which fires when the initial HTML document has been completely loaded and parsed
document.addEventListener('DOMContentLoaded', () => {
    // Fetches data from the '/top-songs' endpoint using the Fetch API
    fetch('/top-songs')
        // If the fetch request is successful, the response is parsed as JSON
        .then(response => {
            console.log('Fetch response:', response);
            // If the response is not OK (status code not in the 200-299 range), an error is thrown
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        // If the JSON parsing is successful, the data is processed
        .then(data => {
            console.log('Data fetched:', data);
            // Get a reference to the DOM element with the id 'tracks'
            const tracksDiv = document.getElementById('tracks');
            // If the fetched data contains an 'error' property, display the error message
            if (data.error) {
                tracksDiv.innerHTML = `<p class="text-red-500">Error: ${data.error}</p>`;
            } else {
                // Otherwise, iterate over the fetched data (assumed to be an array of track objects)
                data.forEach(track => {
                    // Create a new div element for each track
                    const trackDiv = document.createElement('div');
                    trackDiv.className = 'track p-4 bg-white rounded shadow';
                    // Set the innerHTML of the div to display the track details and an audio player
                    trackDiv.innerHTML = `<h2 class="text-2xl font-semibold">${track.name}</h2>
                                          <p class="text-lg">Artist: ${track.artist}</p>
                                          <p class="text-lg">Album: ${track.album}</p>
                                          <p class="text-lg">Release Date: ${track.release_date}</p>
                                          <audio controls class="mt-2 w-full">
                                            <source src="${track.preview_url}" type="audio/mpeg">
                                            Your browser does not support the audio element.
                                          </audio>`;
                    // Append the track div to the 'tracks' div
                    tracksDiv.appendChild(trackDiv);
                });
            }
        })
        // If any error occurs during the fetch or data processing, catch the error
        .catch(error => {
            console.error('Error fetching top songs:', error);
            const tracksDiv = document.getElementById('tracks');
            // Display the error message in the 'tracks' div
            tracksDiv.innerHTML = `<p class="text-red-500">Error fetching top songs: ${error.message}</p>`;
        });
});
