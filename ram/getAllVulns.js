function testLoaded(resolve, reject) {
    if(document.querySelectorAll('.loadingGif').length === 0) {
        resolve();
    } else {
        setTimeout(function() {testLoaded(resolve, reject);}, 500);
    }
}

function openTb(tb) {
    tb.querySelector('.toggleMark').click();
    return new Promise(testLoaded);
}

var ipRegex = /(.*)\s*\((\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\)/;
function dataGetter(tb) {
    return function() {
        var name = tb.querySelector('.fp_vuln_title').innerText;
        var severity = tb.querySelector('.colSeverity').innerText;
        var nodes = [].slice.call(tb.querySelectorAll('.DataTable>tbody'));
        nodes.forEach(function(n) {
            var row = n.children[0];
            var asset = row.children[0].innerText;
            var match = ipRegex.exec(asset);
            var host, ip;
            if(match) {
                host = match[1];
                ip = match[2];
            } else {
                host = '';
                ip = asset;
            }
            var network = row.children[1].innerText;
            var port = row.children[2].innerText;
            var os = row.children[3].querySelector('span').innerText;
            var type = row.children[4].querySelector('span').innerText;
            var crit = row.children[5].querySelector('span').innerText;
            vulns.push([name, severity, host, ip, network, port, os, type, crit]);
        });
        
        // Try to keep CSO from eating up 1GB+ of RAM 
        // Neither option really works - it looks like the page keeps refs to
        // all the detached trees :(
        //tb.querySelector('.toggleMark').click();
        tb.remove();
        return Promise.resolve();
    }
}

var vulnLinks = [].slice.call(document.querySelectorAll('.DataTable>tbody'));
var vulns = [];
function getNext() {
    if (vulnLinks.length != 0) {
        tb = vulnLinks[0];
        vulnLinks.splice(0, 1);
        openTb(tb).then(dataGetter(tb)).then(getNext);
    } else {
        document.body.innerHTML='';
        var a = document.createElement('a');
        a.innerHTML = "Download json";
        a.href = "data:," + encodeURIComponent(JSON.stringify(vulns));
        a.setAttribute('download', 'vulnerabilities.json');
        document.body.appendChild(a);
    }
}
getNext();
