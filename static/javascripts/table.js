function altRows(id){

    if(document.getElementsByTagName){  
        
        var table = document.getElementById(id);
        if (table != null){
            var rows = table.getElementsByTagName("tr"); 
         
            for(i = 1; i < rows.length; i++){          
                if(i % 2 == 0){
                    rows[i].className = "evenrowcolor";
                }else{
                    rows[i].className = "oddrowcolor";
                }      
            }
        }
    }
}