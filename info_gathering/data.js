names = [].map.call(document.querySelectorAll('.td-name'), function(n) {return n.innerText; })
document.body.innerHTML='';
names.forEach(function(e) {
    var div = document.createElement('div');
    div.innerHTML = e;
    document.body.appendChild(div);
});


