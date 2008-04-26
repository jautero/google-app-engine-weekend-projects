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
	if (element.getAttribute && element.getAttribute("class")=="title") {
		element.setAttribute("id",id+"t");
		element.innerHTML=title;
	}
	if (element.getAttribute && element.getAttribute("class")=="content") {
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
	editnode.id=node.id
	var titlename= node.id +'t';
	var contentname = node.id + 'c';
}

function get_node_by_class(node,aclass) {
	for (var i=0; i < node.childNodes.length; i++) {
		var child=node.childNodes[i];
		if (child.getAttribute && child.getAttribute("class")==aclass) {
			return child;
		};
	};
	return null;
}
function edit(node) {
  var titlediv=get_node_by_class(node,"title");
  var contentdiv=get_node_by_class(node,"content");
  var editnode=document.getElementById('edittemplate').cloneNode(true);
  var titleelement=get_node_by_class(editnode,"title");
	var contentelement=get_node_by_class(editnode,"content");
	
  editnode.id=node.id;
	titleelement.name=node.id+"t";
	contentelement.name=node.id+"c";
	
	titleelement.value=titlediv.innerHTML;
	contentelement.value=contentdiv.innerHTML;
	node.parentNode.replaceChild(editnode,node);
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
  var noteelement=document.getElementById('notetemplate').cloneNode(true);
	var newtitle=get_node_by_class(noteelement,"title");
	var newcontent=get_node_by_class(noteelement,"content");
	
	noteelement.id=node.id;
	newtitle.setAttribute("id",node.id);
	newtitle.innerHTML=title;
	newcontent.setAttribute("id",node.id);
	newcontent.innerHTML=content;
	
	node.parentNode.replaceChild(noteelement,node);
}


function toggle_content(node) {
	var contentnode=get_node_by_class(node,"content");
	if (contentnode.style.display == 'none') {
		contentnode.style.display = 'block';
	} else {
		contentnode.style.display = 'none';
	}
}