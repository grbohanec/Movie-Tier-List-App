const rows = document.querySelectorAll('.row');

const movies_window = document.getElementById("movies_window");

const onDragOver = (event) => {
    event.preventDefault();
}

const onDrop = (event) => {
    event.preventDefault();
    const draggedCardId = event.dataTransfer.getData('id');
    const draggedCard = document.getElementById(draggedCardId);
    console.log(event.target.id);

    event.target.appendChild(draggedCard);
    console.log('dropped');
    updateMovieTier(draggedCardId, event.target.id);
}


rows.forEach((row) => {
    row.ondragover = onDragOver;
    row.ondrop = onDrop;
});

movies_window.ondragover = onDragOver;
movies_window.ondrop = onDrop;

function updateMovieTier(movieId, newTier) {
    fetch('', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            movieId: movieId,
            newTier: newTier
        })
    })
    .then(response => response.json())
    .then(data => console.log('Success', data))
    .catch((error) => {
        console.error('Error:', error);
    });    
}

function getCookie(name) {
    let cookieVal = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieVal = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieVal;
}