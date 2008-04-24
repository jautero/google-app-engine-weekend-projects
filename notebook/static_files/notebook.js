// Javascript for notebook
//
// Copyright 2008 Juha Autero <jautero@gmail.com>
//
//
var count=0;

function add(title,text,editit) {
  var content=document.getElementById("content");
  var id="note"+count;
  var node=document.createElement("div");
  count=count+1;
  

  node.id=id;
  node.innerHTML='<div class="menu" onclick="edit(this.parentNode);">Edit</div><div class="title">'+title+'</div><div class="content">'+text+'</div>';
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

function edit(node) {
  var divs=node.getElementsByTagName('div');
  var quote="'";
  var title=divs[1].innerHTML;
  var content=divs[2].innerHTML;
  node.innerHTML='<div class="menu" onclick="done(this.parentNode);">done</div><input type="text" name="'+node.id+'t" value="'+title+'" class="title"> <br><textarea name="'+node.id+'c" class="content" rows=5>'+content+'</textarea>'; 
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


