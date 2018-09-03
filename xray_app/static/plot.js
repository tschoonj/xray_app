$(document).ready(function () {    
    //shows and hides fields depending on $Select
    function show_hide($Select) {
        if ($Select == "CS_Photo_Partial"){
            $("div.xlib").hide();
            $("#int_z, #shell").show();
        } else if ($Select == "CS_Total" || $Select == "CS_Photo" || $Select == "CS_Rayl" || $Select == "CS_Compt"|| $Select == "CS_Energy" || $Select == "CS_Photo_Total") {
            $("div.xlib").hide();
            $("#int_z_or_comp").show();
        } else if ($Select.includes("CS_FluorLine")) {
            $("div.xlib").hide();
            $("#int_z, #transition").show();
        };    
    };
    
    // clear text fields onfocus
    $("input[type='text']").on("focus", function(){
        $( this ).val('');
    });
    
    // shows and hides transition select forms depending on $Radio
    function show_hide_trans ($Radio) {
    if ($Radio == "IUPAC") {
            $("#transition-iupac").show();
            $("#transition-siegbahn").hide();
        } else if ($Radio == "Siegbahn") {
            $("#transition-siegbahn").show();
            $("#transition-iupac").hide();
        } else if ($Radio == "All") {
            $("#transition-siegbahn, #transition-iupac").hide();
        };
    };
    
    // on page refresh or load (post form)
    var $SelectOnLoad = $("select#function").val();
    show_hide($SelectOnLoad);
    
    // hides/shows as form changes 
    $("select#function").change(function(e) {
        var $SelectVal = $(this).val();
        show_hide($SelectVal);
    });
        
    /* hides All option for transition until implemented */
    $("div#transition li:last-child").hide();
    
    // shows select form for transition on change
    $("input[type='radio']").change(function(e) {
        var $RadioVal = $(this).val();
        show_hide_trans($RadioVal);        
    });
    
    // shows select form for transition on load
    var $RadioOnLoad = $("div#transition input[checked]").val();
    show_hide_trans($RadioOnLoad);
    
    //client side validation 
    $("form").submit(function(event) {
        var $Selected = $("select#function").val();
        if ($Selected == "CS_Photo_Partial"){
            if (!$("input#int_z[value]").val() || !$("input#range_start[value]").val()) {
            $(".empty-alert").show();
            return false;
            };
        } else if ($Selected == "CS_Total" || $Selected == "CS_Photo" || $Selected == "CS_Rayl" || $Selected == "CS_Compt"|| $Selected == "CS_Energy" || $Selected == "CS_Photo_Total") { 
            if (!$("input#int_z_or_comp[value]").val() || !$("input#range_start[value]").val() || !$("input#range_end[value]").val()) {
            $(".empty-alert").show();
            return false;
            };     
        } else if ($Selected.includes("CS_FluorLine")) { 
            if (!$("input#int_z[value]").val() || !$("input#range_start[value]").val() || !$("input#range_end[value]").val()) {
            $(".empty-alert").show();
            return false;
            };   
        };      
    });
       
});
