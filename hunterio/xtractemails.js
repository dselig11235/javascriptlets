emails = [].map.call(document.querySelectorAll('.email'), function(e) { return e.textContent });

function onlyUnique(value, index, self) { 
    return self.indexOf(value) === index;
}
sources = [].map.call(document.querySelectorAll('.sources_list'), function(s) { 
  return [].map.call(s.querySelectorAll('a'), function(a) { 
    return a.href; 
  }); 
}).reduce(function(x, y) { return x.concat(y); }, []).filter(onlyUnique)


document.body.innerHTML = '';
[emails, sources].forEach(function(data) {
    var p = document.createElement('p');
    data.forEach(function(e) {
      var div = document.createElement('div');
      div.innerHTML = e;
      p.appendChild(div);
    })
    document.body.appendChild(p);
});

