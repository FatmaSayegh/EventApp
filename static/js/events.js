function manageEvent(slug, id){

    const url = MANAGE_URL + "/" + slug + "/" + id;
    let http = new XMLHttpRequest();
    http.open("GET", url);
    http.send();
    
    http.onreadystatechange = function(e){
        if(this.readyState==4 && this.status == 200){
            manageResponse(slug, id, this.responseText)
        }
    }
}
    

function manageResponse(slug, id, text){
    console.log("respone: " + text)
    if (!text.includes("success"))
        return;
    

    let element_parts = document.getElementsByClassName(slug +"_parts")
    
    if (id < 3 && (!element_parts || element_parts.length == 0)){
        return;
    }
    
    if (id < 3){
        let splt = text.split(":")
        if (splt.length == 2){
            counts = document.getElementsByClassName(slug +"_count")
            for (let i = 0; i<counts.length; i++){
                counts[i].innerHTML = splt[1] + " participating"
            }
        }
        for (let i = 0; i<element_parts.length; i++){
            let e = element_parts[i]
            if (id == 0){
                e.innerHTML ='<p onclick="manageEvent(\'' + slug + '\',2)">You are not participating (click to undo)</p>'
            }else if (id == 1){
                e.innerHTML = '<p onclick="manageEvent(\'' + slug + '\',2)">You are participating (click to undo)</p>'
            }else if (id == 2){
                e.innerHTML = "<li onclick=\"manageEvent('" + slug + "', 1)\">Participating</li><li  onclick=\"manageEvent('" + slug + "', 0)\">Not this time</li>"
            }
        }
    }else{
        element_parts = document.getElementsByClassName(slug +"_container");
        console.log(element_parts)
         for (let i = 0; i<element_parts.length; i++){
            let e = element_parts[i]
             console.log("removing " + e)
            e.remove()
            
         }
    }   
}