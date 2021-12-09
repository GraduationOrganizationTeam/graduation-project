// var inputBox = document.getElementById("inputBox");
// var hideableElements = document.getElementsByClassName("hideable");
// var expandeableElement = document.getElementById("expandeable");
// var contractedWidth = expandeableElement.offsetWidth;
// var speed = 1.25;

// // A CORRIGIR: 
// // Se clicar rápido fora e dentro da barra de pesquisa, não funciona mais como o esperado

// function expandBar(element){
//     var currentWidth = element.offsetWidth;

//     function increase()
//     {
//         currentWidth += speed * 15;

//         if (currentWidth >= 600)
//         {
//             element.style.maxWidth = 600 + "px";
//             return true
//         }

//         element.style.maxWidth = currentWidth + "px";
//         requestAnimationFrame(increase);
//     }

//     increase();
// }

// function contractBar(element){
//     var currentWidth = element.offsetWidth;

//     function decrease()
//     {
//         currentWidth -= speed * 15;

//         if (currentWidth <= contractedWidth)
//         {
//             element.style.maxWidth = contractedWidth + "px";
//             return fadeIn(hideableElements, hideableElements.length-1)
//         }

//         element.style.maxWidth = currentWidth + "px";
//         requestAnimationFrame(decrease);
//     }

//     decrease();
// }

// function fadeOut(elements, i){
//     var op = 1; // largura inicial

//     function decrease()
//     {   
//         op -= speed * 0.1;

//         if(op <= 0)
//         {
//             elements[i].style.opacity = 0;
//             elements[i].style.display = "none";
//             i += 1
//             if(i == elements.length){return expandBar(expandeableElement);}
//             else{return fadeOut(elements, i)}
//         }
        
//         elements[i].style.opacity = op;
//         requestAnimationFrame(decrease);
//     }
//     decrease();
// }

// function fadeIn(elements, i){
//     elements[i].style.display = "block";
//     var op = 0; // largura inicial

//     function increase()
//     {   
//         op += speed * 0.1;

//         if(op >= 1)
//         {
//             elements[i].style.opacity = 1;
//             i -= 1
//             if(i== -1){return true}
//             else{return fadeIn(elements, i)}
//         }
        
//         elements[i].style.opacity = op;
//         requestAnimationFrame(increase);
//     }
//     increase();
// }


// function show()
// {
//     for(let i = 0; i < hideableElements.length; i++)
//     {
//         hideableElements[i].style.opacity = 0;
//         hideableElements[i].style.display = 'none';
//     }
//     expandeableElement.style.maxWidth = 600 + "px";
//     contractBar(expandeableElement);
// }

// function hide()
// {

//     fadeOut(hideableElements, 0);
// }

// if (screen.width <= 600)
// {
//     expandeableElement.style.maxWidth = expandeableElement.offsetWidth  + "px";
    
//     inputBox.addEventListener("focus", hide);
    
//     inputBox.addEventListener("focusout", show);
// }