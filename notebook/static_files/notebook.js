// Javascript for notebook
//
// Copyright 2008 Juha Autero <jautero@gmail.com>
//
//
var count=0;

function add(title,text,editit) {
  var content=document.getElementById("content");
  var id="note"+count;
  var node=document.getElementById('notetemplate').cloneNode(true);
  count=count+1;
  node.id=id;
  for (var i = node.childNodes.length - 1; i >= 0; i--){
  	var element=node.childNodes[i];
	if (element.getAttribute("class")=="title") {
		element.setAttribute("id",id+"t");
		element.innerHTML=title;
	}
	if (element.getAttribute("class")=="content") {
		element.setAttribute("id",id+"c");
		element.innerHTML=text;
	}
  };
  content.appendChild(node);
  if (editit) {
    edit(node);
  }
}

function editAll() {
  var content=document.getElementById("content");

  for (index=0; index<content.childNodes.length;index++) {
    var element=content.childNodes[index];
    if (element.nodeName=="DIV") {
       edit(element);
    }
  }  
  return true;
}
function replace_node_with_edit_fragment(node,title,content) {
	var editnode=document.getElementById('edittemplate').cloneNode(true);
	editnode.id=node.id
	var titlename= node.id +'t';
	var contentname = node.id + 'c';
}

function edit(node) {
  var divs=node.getElementsByTagName('div');
  var quote="'";
  var title=divs[0].innerHTML;
  var content=divs[2].innerHTML;
  
}

function getValueOfNamedChild(node,name)
{
  for (index=0; index<node.childNodes.length;index++) {
    var child=node.childNodes[index];
    if (child.name == name) {
      return child.value;
    }
  }
}

function done(node) {
  var title=getValueOfNamedChild(node,node.id+"t");
  var content=getValueOfNamedChild(node,node.id+"c");
  node.innerHTML='<div class="menu" onclick="edit(this.parentNode);">Edit</div><div class="title">'+title+
                 '</div><div class="content">'+content+'</div>';

}


