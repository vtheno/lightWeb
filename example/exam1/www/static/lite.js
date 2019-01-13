// print is console.log
function print( obj ){
    console.log(obj)
}
function quote ( s ){
    return s.replace(/[<>&" ]/g,function(c){ // \s
	return {'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;', " ":"&nbsp;"}[c]
    })
}
function unquote ( s ){
    return s.replace(/&(lt|gt|amp|quot);/ig,function(all,t){// |nbsp
	return {'lt':'<','gt':'>','amp':'&','quot':'"'}[t] // 'nbsp':' ',
    })
}
function getElementById( id ){
    return function() { return document.getElementById( id ) }
}
function Task ( ms ) {
    let _ret = {
	_ms: typeof ms == 'number' ? ms : 10,
	tasks: [],
    }
    function addTask( handler ){
	if (typeof handler == 'function' && handler.length == 0){
	    _ret.tasks.push( handler )
	    return _ret.tasks.length - 1
	}else{
	    throw "addTask: (unit -> unit) -> int; handler: unit -> unit"
	}
    }
    function removeTask( id ) {
	if (typeof id == 'number') {
	    _ret.tasks.splice(id, 1)
	    return null
	}else{
	    throw 'removeTask: int -> unit'
	}
    }
    _ret.add = addTask
    _ret.remove = removeTask
    function mainThread() {
	for( var i in _ret.tasks ){
	    _ret.tasks[i]()
	}
    }
    let main = setInterval( mainThread, ms )
    function stop (){
	clearInterval(main)
    }
    _ret.stop = stop
    return _ret 
}
function Element( data ){
    let _self = null
    let _data = null
    switch(typeof data){
    case 'object':{
	if ( !data.id ){
	    throw "data.id is: " + data.id
	}
	_data = data
	delete data
	_self = getElementById ( _data.id )
	let value = _self()
	value.id = _data.id
	break
    }
    default:
	throw "$(" + data + ")" + ": input argument need object type"
    }
    let _ret = {
	data: _data,
	// self: _self,
    }
    delete _data
    function then (handler){
	if( _self() == null ){
	    throw "$(\"" + _ret.data.id + "\")" + ": is undefine, plz try again"
	}
	if( typeof handler == "function" && handler.length == 1){
	    handler(_self())
	    return _ret
	}
	else{
	    throw "$(\"" + _ret.data.id + "\")" + ": Element .then(handler) typeof handler function: unit -> unit"
	}
    }
    _ret.then = then
    function hidden( flag ){
	if ( typeof flag == 'boolean'){
	    _ret.then( function(it) {
		if(flag){
		    if( !it.classList.contains("hidden") ){
			it.classList.add("hidden")
		    }
		}else{
		    it.classList.remove("hidden")
		}
	    } )
	}else{
	    throw "$(\"" + _ret.data.id + "\")" + ": Element .show(flag) typeof flag: boolean"
	}
    }
    _ret.hidden = hidden
    return _ret
}
function $(obj){
    return new Element(obj)
}
function $$( obj , handler ){
    return obj.then( handler )
}
// nodeType == 3  is text
// nodeType == 1  is node
function containsName (attrs, obj) {
    let i = attrs.length
    while (i--) {
        if (attrs[i].nodeName === obj) {
            return [i, false]
        }
    }
    return [-1, true]
}
function UI_loadInit( node ){
    let attrs = Array.from(node.attributes)
    let tmp = containsName(attrs,'container')
    var idx = tmp[0], err = tmp[1]
    let flex = "flex"
    if ( !err ){ 
	var value = attrs[idx].nodeValue
	if ( value == flex ) { 	// || value == grid 
	    node.classList.add(value)
	    for( var i in attrs ){
		if (attrs[i].name.substring(0,5) == value+":"){
		    let name = attrs[i].name.replace(value+":","")
		    // print( name )
		    node.attributes.removeNamedItem(attrs[i].name)
		    switch ( name ){
		    case "scale":{
			node.classList.add( "flex-scale-" + attrs[i].value )
			break
		    }
		    case "item":{
			node.classList.add( "flex-item-" + attrs[i].value )
			break
		    }
		    case "axis":{
			node.classList.add( "flex-axis-" + attrs[i].value )
			break
		    }
		    case "main":{
			node.classList.add( "flex-axis-main-" + attrs[i].value )
			break
		    }
		    case "cross":{
			node.classList.add( "flex-axis-cross-" + attrs[i].value )
			break
		    }
		    default: break
		    }
		}
	    }
	}
    }
    for( var idx=0;idx<node.childNodes.length;idx++){
	if( node.childNodes[idx].nodeType == 1 ){
	    UI_loadInit( node.childNodes[idx] )
	}
    }
}
function is_mobile () {
    return document.getElementsByTagName("body")[0].clientWidth < 678
}
window.onload = function (){
    UI_loadInit( document.getElementsByTagName("body")[0] )
}
