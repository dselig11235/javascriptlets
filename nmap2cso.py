#!/usr/bin/python


from nmaptools import NmapResults
from sys import argv
from json import dumps

results = NmapResults()
results.open(argv[1:])
dataStr = dumps(results.data)
funcStr = """
function addRecords(records) {
    var rows = document.querySelectorAll('.RowdiscoveredOpenPorts');    
    var discoverd = [].map.call(rows, function(r) {
        return [r.querySelector('input[name="eptOpenPortIPs"]').value, r.querySelector('input[name="eptOpenPortPorts"]').value, r.querySelector('input[name="eptOpenPortIdentifiedTypeVersions"]').value];
    });
    records.forEach(function(rec) {
        var matchPosition = discovered.findIndex(function(r) {
            return r[0] == rec[0] && r[1] == rec[1];
        });
        rows[matchPosition].querySelector('input[name="eptOpenPortIdentifiedTypeVersions"]').value = rec[3];
    });
}"""

print '{} addRecords({})'.format(funcStr, dataStr)
