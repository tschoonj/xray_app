//move code from index here after fixing reroute, below tests if routes etc work
$( "select" )
  .change(function() {
    var str = "";
    $( "select option:selected" ).each(function() {
      str += "Function: " + $( this ).val() + " ";
    });
    $( "p" ).text( str );
  })
  .trigger( "change" );

$(document).ready(function(){
        $("#atmw, #dens").click(function(){
                $("div.xlib").hide();
                $("#atm_num").show();
                                });
        $("#rff").click(function(){
                $("div.xlib").hide();
                $("#atm_num").show();
                $("#momentumtransfer").show();
                });        
        $("#lineenergy, #radrate").click(function(){
                $("div.xlib").hide();
                $("#atm_num").show();
                $("#linetype").show();
                });
        $("#absedge, #jumprat, #flyield, #augyield, #alw, #econfig").click(function(){
                $("div.xlib").hide();
                $("#atm_num").show();
                $("#shell").show();
                }); 
        $("#cs_pp").click(function(){
                $("div.xlib").hide();
                $("#atm_num").show();
                $("#shell").show();
                $("#energy").show();
                });
        $("#cs_tot, #cs_ph, #cs_rayl, #cs_compt, #csb_tot, #csb_ph, #csb_rayl, #csb_compt,").click(function(){
                $("div.xlib").hide();
                $("#energy").show();
                $("#element_or_comp").show();
                });         
                
});

window.onload = function(){
    if (window.jQuery) {  
        // jQuery is loaded  
        alert("Static works");
    } else {
        // jQuery is not loaded
        alert("Doesn't Work");
    }
} 

