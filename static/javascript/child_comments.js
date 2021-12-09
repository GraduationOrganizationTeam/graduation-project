var showableElements = document.getElementsByClassName("hidden-form");

function myFunc(element)
{
    pos = element.id.slice(5,);

    if(showableElements[pos].style.display=="none"){
        for (let i = 0; i < showableElements.length; i++){
            showableElements[i].style.display = "none";
        } 
        showableElements[pos].style.display = "flex";
    }

    else if(showableElements[pos].style.display=="flex"){
        showableElements[pos].style.display = "none";
    }
    
}