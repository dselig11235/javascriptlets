function addICMP(ips) {
    /*
     * This takes the targets from the "IPs scanned" list on the summaries
     * page.  From what I understand, we don't put all the targets in - just
     * the ones that have open ports
    var list = document.querySelector('#tabContent > form > fieldset:nth-child(8) > table:nth-child(3) > tbody:nth-child(1) > tr > td:nth-child(2) > div > ul');
    var ips = [].map.call(list.children, function(l) { return l.innerText; });
   */
    var t = document.querySelector('#tabContent > form > fieldset:nth-child(8) > table:nth-child(7) > tbody:nth-child(1) > tr > td:nth-child(2) > table > tbody:nth-child(2)');
    var existing = [].map.call(t.children, function(r) { 
        return r.querySelector('input[name="eptOSAssetIPs"]').value
    });
    ips.forEach(function(ip) {
        if(existing.indexOf(ip) < 0) {
            document.querySelector('#tabContent > form > fieldset:nth-child(8) > table:nth-child(7) > tbody:nth-child(1) > tr > td:nth-child(2) > table > tbody:nth-child(3) > tr > td > a').click();
            t.children[t.children.length - 1].querySelector('input[name="eptOSAssetIPs"]').value=ip;
            t.children[t.children.length - 1].querySelector('input[name="icmpNetmasks"]').value='No Response';
        }
    });
}
