const cards = document.querySelectorAll('.movie_card');

const onDragStart = (event) => {
    event.dataTransfer.setData('id', event.target.id);

    setTimeout(() => {
        event.target.style.visibility = 'hidden';
    }, 50)
}

const onDragEnd = (event) => {
    event.target.style.visibility = 'visible';
}

cards.forEach((card) => {
    card.ondragstart = onDragStart;
    card.ondragend = onDragEnd;
})