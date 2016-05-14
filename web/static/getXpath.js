var btn = document.getElementById('urlBtn');
btn.onclick = function(){
  var url = document.getElementById('urlInput').value;
  document.getElementById("iframePage").src = url;
}

var iframePage = document.getElementById('iframePage');
iframePage.onload = function(){
  var xpath = document.getElementById('xpath');
  xpath.innerHTML = 'Xpath is shown in here';
  var contents = $("#iframePage").contents();
  var elements = contents[0].all;
  for(var i = 0; i < elements.length; i++){
    elements[i].onclick = function(event){
      event.preventDefault();// 取消事件的默认行为
      event.stopPropagation(); // 阻止事件的传播
      xpath.innerHTML = getXPath(this);
    }
  }
}

function getXPath( element ){
  var xpath = '';
  for ( ; element && element.nodeType == 1; element = element.parentNode ){
    var id = $(element.parentNode).children(element.tagName).index(element) + 1;
      id > 1 ? (id = '[' + id + ']') : (id = '');
      xpath = '/' + element.tagName.toLowerCase() + id + xpath;
  }
  return xpath;
}
