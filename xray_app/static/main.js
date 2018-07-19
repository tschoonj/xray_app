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
        $("option[value='FF_Rayl']").click(function(){
                $("div.xlib").hide();
                $("#int_z").show();
                $("#float_q").show();
                });
                                
        $("option[value='AtomicWeight'], option[value='ElementDensity']").click(function(){
                $("div.xlib").hide();
                $("#int_z").show();
                                });
       
        $("option[value='LineEnergy'], option[value='RadRate']").click(function(){
                $("div.xlib").hide();
                $("#int_z").show();
                $("#linetype").show();
                });
        $("option[value='EdgeEnergy'], option[value='JumpFactor'], option[value='FluorYield'], option[value='AugerYield'], option[value='AtomicLevelWidth'], option[value='ElectronConfig']").click(function(){
                $("div.xlib").hide();
                $("#int_z").show();
                $("#shell").show();
                }); 
        $("option[value='CS_Photo_Partial']").click(function(){
                $("div.xlib").hide();
                $("#int_z").show();
                $("#shell").show();
                $("#energy").show();
                });
        $("option[value='CS_Total'], option[value='CS_Photo'], option[value='CS_Rayl'], option[value='CS_Compt'], option[value='CSb_Total'], option[value='CSb_Photo'], option[value='CS_Rayl'], option[value='CS_Compt']").click(function(){
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


