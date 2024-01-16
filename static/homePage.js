function flipCard1() {
    var frontCard = document.getElementById("card1-front");
    var backCard = document.getElementById("card1-back");

    if (frontCard.style.transform === 'rotateY(180deg)') {
        frontCard.style.transform = 'rotateY(0deg)';
        backCard.style.transform = "rotateY(180deg)";
    }
    
    else {
        frontCard.style.transform = 'rotateY(180deg)';
        backCard.style.transform = "rotateY(0deg)";
    }

}

function flipCard2() {
    var frontCard = document.getElementById("card2-front");
    var backCard = document.getElementById("card2-back");

    if (frontCard.style.transform === 'rotateY(180deg)') {
        frontCard.style.transform = 'rotateY(0deg)';
        backCard.style.transform = "rotateY(180deg)";
    }
    
    else {
        frontCard.style.transform = 'rotateY(180deg)';
        backCard.style.transform = "rotateY(0deg)";
    }
}