document.addEventListener('DOMContentLoaded', () => {
    console.log('top_songs.js loaded'); // Ensure this script is loaded
    fetch('/top-songs')
        .then(response => {
            console.log('Fetch response:', response);
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            const contentType = response.headers.get('content-type');
            if (!contentType || !contentType.includes('application/json')) {
                throw new TypeError('Expected JSON, but got ' + contentType);
            }
            return response.json();
        })
        .then(data => {
            console.log('Data fetched:', data);
            const tracksDiv = document.getElementById('tracks');
            if (data.error) {
                tracksDiv.innerHTML = `<p class="text-red-500">Error: ${data.error}</p>`;
            } else {
                data.tracks.forEach(track => {
                    console.log(`Rendering track: ${track.name}`);
                    const trackDiv = document.createElement('div');
                    trackDiv.className = 'track p-4 bg-white rounded shadow';
                    trackDiv.innerHTML = `
                        <h2 class="text-2xl font-semibold">${track.name}</h2>
                        <p class="text-lg">Artist: ${track.artist}</p>
                        <p class="text-lg">Genre: ${track.genre}</p>
                        <audio controls class="mt-2 w-full">
                            <source src="${track.preview_url}" type="audio/mpeg">
                            Your browser does not support the audio element.
                        </audio>
                    `;
                    tracksDiv.appendChild(trackDiv);
                });
            }
        })
        .catch(error => {
            console.error('Error fetching top songs:', error);
            const tracksDiv = document.getElementById('tracks');
            tracksDiv.innerHTML = `<p class="text-red-500">Error fetching top songs: ${error.message}</p>`;
        });
});