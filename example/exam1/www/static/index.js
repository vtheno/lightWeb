print("this is mk load")
window.onloaded = function(){
    let desktop = $({id: "desktop"})
    let mobile  = $({id: "mobile"})
    let task = new Task(50)
    task.add( function(){
	if ( is_mobile() ){
            desktop.hidden(true)
            mobile.hidden(false)
	}else{
            desktop.hidden(false)
            mobile.hidden(true)
	}
    })

}
