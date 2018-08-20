$(document).ready(function () {    
    function show_hide($Select) {
        if ($Select == "CS_Photo_Partial"){
            $("div.xlib").hide();
            $("#int_z, #shell").show();
        } else if ($Select == "CS_Total" || $Select == "CS_Photo"|| $Select == "CS_Rayl" || $Select == "CS_Compt"|| $Select == "CS_Energy") {
            $("div.xlib").hide();
            $("#int_z_or_comp").show();
        } else if ($Select.includes("CS_FluorLine")) {
            $("div.xlib").hide();
            $("#int_z, #linetype").show();
            $("#linetype-trans_iupac, #linetype-trans_siegbahn").hide();
        };    
    };
    
    /* on page refresh or load (post form) */
    var $SelectOnLoad = $("select#function").val();
    show_hide($SelectOnLoad);
    
    /* hides/shows as form changes  */ 
    $("select#function").change(function(e) {
        var $SelectVal = $(this).val();
        show_hide($SelectVal)
    });
    
    
    /* hides All option for linetype until implemented */
    $("div#linetype li:last-child").hide();
    
    /*shows appropriate select form for linetype*/
    $("input[type='radio']").change(function(e) {
        var $RadioVal = $(this).val();
        if ($RadioVal == "IUPAC") {
            $("#linetype-trans_iupac").show();
            $("#linetype-trans_siegbahn").hide();
        } else if ($RadioVal == "Siegbahn") {
            $("#linetype-trans_siegbahn").show();
            $("#linetype-trans_iupac").hide();
        }
    });    
});
