data = document.createElement('div');
function addTo(parent, tag, html) {
    var n = document.createElement(tag);
    n.innerHTML = html;
    parent.appendChild(n);
}
company = document.querySelector('#AccountGeneralInfoUserControl_AccountNameLabel').innerHTML;
addTo(data, 'p', company);
address = document.querySelector('#AccountGeneralInfoUserControl_AddressPanel').innerHTML
addTo(data, 'p', address);
phone = document.querySelector('#AccountGeneralInfoUserControl_PhoneNumberLabel').innerHTML
addTo(data, 'p', phone);
primary_name = document.querySelector('#AccountGeneralInfoUserControl_PrimaryContactValue').innerHTML
primary_email = document.querySelector('#AccountGeneralInfoUserControl_PrimaryContactValue').href.replace('mailto:', '')
contacts = {};
contacts[primary_name + primary_email] = [primary_name, primary_email];
emails = document.querySelectorAll('#FeedContainer > div > div');
[].forEach.call(emails, function(e) {
    try {
        var name = e.querySelector('.ResourceName > a.FeedControl').innerHTML;
        var email = e.querySelector('.ResourceName + a').href.replace('mailto:', '');
        contacts[name + email] = [name, email]
    } catch(err) {}
})

cnode = document.createElement('ol');
Object.getOwnPropertyNames(contacts).forEach(function(c) {
    addTo(cnode, 'li', contacts[c][0] + ' : ' + contacts[c][1]);
})
data.appendChild(cnode);
document.body.innerHTML = '';
document.body.appendChild(data);
