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

$("#int_z").show();

$(document).ready(function(){
        $("#atmw, #dens").click(function(){
                $("div.xlib").hide();
                $("#int_z").show();
                                });
        $("#rff").click(function(){
                $("div.xlib").hide();
                $("#int_z").show();
                $("#float_q").show();
                });        
        $("#lineenergy, #radrate").click(function(){
                $("div.xlib").hide();
                $("#int_z").show();
                $("#linetype").show();
                });
        $("#absedge, #jumprat, #flyield, #augyield, #alw, #econfig").click(function(){
                $("div.xlib").hide();
                $("#int_z").show();
                $("#shell").show();
                }); 
        $("#cs_pp").click(function(){
                $("div.xlib").hide();
                $("#int_z").show();
                $("#shell").show();
                $("#energy").show();
                });
        $("#cs_tot, #cs_ph, #cs_rayl, #cs_compt, #csb_tot, #csb_ph, #csb_rayl, #csb_compt,").click(function(){
                $("div.xlib").hide();
                $("#energy").show();
                $("#int_z_or_comp").show();
                });         
                
});


//add units! maybe better to add to forms as part of field?
  
/*$( "select" ).change(function() {
    $( "select option:selected" ).each(function() {
        var $selectedForm = $(this).val;
        if ($selectedForm == "AtomicWeight") {
            $("div.form-group").hide();
            $(".element").show();}
        else if ($selectedForm. == "Rayl_FF") {
            $("div.form-group").hide();
            $(".element, .momentumtransfer").show();
            })
            .trigger("change")  
            
so bugged it breaks the window :(
*/  
window.onload = function(){
    if (window.jQuery) {  
        // jQuery is loaded  
        alert("Static works");
    } else {
        // jQuery is not loaded
        alert("Doesn't Work");
    }
} 

