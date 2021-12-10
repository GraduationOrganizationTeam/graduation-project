var lis = document.getElementById('filter-form').getElementsByClassName('form-control');

function filterRedirect(){
    let order_by = lis[0].value;
    let dept = lis[1].value;
    let cred_aula = lis[2].value;
    let cred_trab = lis[3].value;

    const re = /\&(.*)/;
    let current = window.location.href.replace(re,"")
    window.location.href=current+"&o="+order_by+"&d="+dept+"&ca="+cred_aula+"&ct="+cred_trab;
}

