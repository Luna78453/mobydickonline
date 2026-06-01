const chaptersContainer = document.getElementById("noveltext");
const buttonsContainer = document.getElementById("buttons");
const chapterElements = document.getElementsByClassName("chapter");
const chapterButtons = document.getElementsByClassName("chapterButton");
const tutorialText = document.getElementById("tutorialtext");

//tutorialText.remove();
//tutorialText = null;
/*let chapterIds = []
//console.log(chapterElements);

for(let chapter of chapterElements){
    //console.log(chapter.id);
    chapterIds.push(chapter.id);
}

//console.log(chapterIds);

for(let i = 0; i < 137; i++){
    chapterButtons[i].setAttribute("id", `${chapterIds[i]}`);
}*/

/*Esta parte del documento se escribió para hacer la transferencia de IDs de los divs
de cada capitulo a los botones de cada capitulo para poder realizar la funcion.

El documento "hfgjfghjkfghjk.htm" es el resultado de usar ese script al iniciar la página.

El resutlado lo guardé de mi buscador y lo cambiado hice copy paste al html principal.*/

function enableChapter(id){
    const chapterElement = chaptersContainer.querySelector(`#${id}`);
    const buttonElement = buttonsContainer.querySelector(`#${id}`);
    let aux = chapterElement.getAttribute("style");

    if(aux == "display: none;"){
        chapterElement.setAttribute("style", "display: block;");
        buttonElement.setAttribute("style", "color: purple;");
    }
    else if(aux == "display: block;"){
        chapterElement.setAttribute("style", "display: none;");
        buttonElement.setAttribute("style", "color: blue;");
    }

    if(document.body.contains(tutorialText)){
        tutorialText.remove();
    }
}
    

function displayAllChapters(){
    for(let i = 0; i < 137; i++){
        if(chapterElements[i].getAttribute("style") == "display: none;"){
            chapterElements[i].setAttribute("style", "display: block;");
            chapterButtons[i].setAttribute("style", "color: purple;");
        }
    }

    if(document.body.contains(tutorialText)){
        tutorialText.remove();
    }
}

function hideAllChapters(){
    for(let i = 0; i < 137; i++){
        if(chapterElements[i].getAttribute("style") == "display: block;"){
            chapterElements[i].setAttribute("style", "display: none;");
            chapterButtons[i].setAttribute("style", "color: blue;");
        }
    }
}