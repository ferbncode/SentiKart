var buttons = require('sdk/ui/button/action');
var tabs = require("sdk/tabs");

var button = buttons.ActionButton({
  id: "mozilla-link",
  label: "Visit Sentikart",
  icon: {
    "16": "./icon-16.png",
    "32": "./icon-32.png",
    "64": "./icon-64.png"
  },
  onClick: handleClick
});

function handleClick(state) {
var myurl = tabs.activeTab.url
var mypro = myurl.split("/")
var product = mypro[3]
tabs.open("127.0.0.1:8080/" + product)

}
