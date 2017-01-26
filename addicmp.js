function addIPs(ips) {
    var t = document.querySelector('#tabContent > form > fieldset:nth-child(8) > table:nth-child(7) > tbody:nth-child(1) > tr > td:nth-child(2) > table > tbody:nth-child(2)');
    var existing = [].map.call(t.children, function(r) { 
        return r.querySelector('input[name="eptOSAssetIPs"]').value
    });
    ips.forEach(function(ip) {
        if(existing.indexOf(ip) < 0) {
            document.querySelector('#tabContent > form > fieldset:nth-child(8) > table:nth-child(7) > tbody:nth-child(1) > tr > td:nth-child(2) > table > tbody:nth-child(3) > tr > td > a').click();
            t.children[t.children.length - 1].querySelector('input[name="eptOSAssetIPs"]').value=ip;
        }
    });
}
