names = [].map.call(document.querySelector('#initial_browse_result').children[0].children[0].children[0].querySelectorAll('._gll'), function(n) { return n.innerText; });
document.body.innerHTML='';
names.forEach(function(e) {
    var div = document.createElement('div');
    div.innerHTML = e;
    document.body.appendChild(div);
});

