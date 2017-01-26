stop = undefined;
expanders = [].slice.call(document.querySelectorAll('.fp_cs_title'));
function openAll() {
    function open() {
        expanders[0].click();
        expanders.splice(0,1);
    }
    open();
    if(expanders.length > 0) {
        setTimeout(openAll, 200);
    }
}
function testLoaded(resolve, reject) {
    if(document.querySelectorAll('.loadingGif').length === 0) {
        resolve();
    } else {
        setTimeout(function() {testLoaded(resolve, reject);}, 500);
    }
}

function clicker(table) {
    return function clickAllValid() {
        console.log('starting clickAllValid');
      var buttons = [].slice.call(table.querySelectorAll('input[value="Valid"]'));
      function clickValid() {
          while(buttons.length > 0 && buttons[0].style.display == "none") {
            console.log('new length is ' + String(buttons.length));
            buttons.splice(0, 1);
          }
          if(buttons.length === 0) { 
              stop = undefined;
              return true; 
          }
          console.log('clicking');
          buttons[0].click();
          function waitForIt() {
            if(buttons[0].style.display == "none") {
              clickValid();
            } else {
              console.log('waiting...');
              var timeout = setTimeout(waitForIt, 250);
              stop = function stopWaiting() {
                  clearTimeout(timeout);
              }
            }
          }
          waitForIt();
        }
    clickValid();
    }
}

openAll();
loadPromise = new Promise(testLoaded);
clickQueue = new Promise(function(resolve,reject) { resolve(); });
function addButtons() {
    [].forEach.call(document.querySelectorAll('#ui-tabs-1 > table table'), function(t) {
      var b = document.createElement('button');
      b.addEventListener('click', function(e) {
          clickQueue = clickQueue.then(clicker(e.target.parentElement));
      });
      b.innerHTML="Mark All Valid";
      t.insertBefore(b, t.firstChild);
      [].forEach.call(t.querySelectorAll('.fp_vuln_title'), function(n) {
          if(n.textContent.toLowerCase().includes('identifies') ||
              n.textContent.toLowerCase().includes('wrapper') ||
              n.textContent.toLowerCase().includes('UDP')) 
          {
              n.parentNode.parentNode.style['background'] = 'orange';
          }
      });
    });
}
loadPromise.then(addButtons);
