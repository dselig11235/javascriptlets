var ips=[];
var t = document.querySelector('#mainTable > tbody');
[].forEach.call(t.querySelectorAll('tr'), function(r) {
  var ip=r.children[2].textContent;
  if(ip.startsWith('192.168') && ips.indexOf(ip) < 0) {
    r.querySelector('input').checked=true;
  }
})


