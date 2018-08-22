$(document).ready(function () {
    /*$(document).on('change keyup', 'select#function', function(e) {
        var currentSelectVal = $(this).val();
        alert(currentSelectVal);
    })*/ /* automatically assigns event handlers to elements that are specified by the selector (i.e select)*/
    
    function show_hide_input($Select) {
        if ($Select == "AtomicWeight" || $Select == "ElementDensity") {
            $("div.xlib").hide();
            $("#int_z").show();
        } else if ($Select == "FF_Rayl" || $Select == "SF_Compt") {
            $("div.xlib").hide();
            $("#int_z, #float_q").show();
        } else if ($Select == "LineEnergy" || $Select == "RadRate"){
            $("div.xlib, select#linetype-trans_iupac, select#linetype-trans_siegbahn").hide();
            $("#int_z, #linetype").show();
        } else if ($Select == "EdgeEnergy" || $Select == "JumpFactor" || $Select == "FluorYield" || $Select == "AugerYield" || $Select == "AtomicLevelWidth" || $Select == "ElectronConfig") {
            $("div.xlib").hide();
            $("#int_z, #shell").show();
        } else if ($Select == "CS_Photo_Partial"){
            $("div.xlib").hide();
            $("#int_z, #shell, #energy").show();
        } else if ($Select == "CS_KN"){
            $("div.xlib").hide();
            $("#energy").show();
        } else if ($Select == "CS_Total" || $Select == "CS_Photo"|| $Select == "CS_Rayl" || $Select == "CS_Compt"|| $Select == "CS_Energy"){
            $("div.xlib").hide();
            $("#int_z_or_comp, #energy").show();
        } else if ($Select.includes("CS_FluorLine")){
            $("div.xlib").hide();
            $("#int_z, #linetype, #energy").show();
        } else if ($Select == "DCS_KN" || $Select == "ComptonEnergy"){
            $("div.xlib").hide();
            $("#energy, #theta").show();
        } else if ($Select == "DCS_Thoms"){
            $("div.xlib").hide();
            $("#theta").show();
        } else if ($Select == "DCS_Rayl" || $Select == "DCS_Compt"){
            $("div.xlib").hide();
            $("#int_z_or_comp, #energy, #theta").show();
        } else if ($Select == "DCSP_KN"){
            $("div.xlib").hide();
            $("#energy, #theta, #phi").show();
        } else if ($Select == "DCSP_Thoms"){
            $("div.xlib").hide();
            $("#theta, #phi").show();
        } else if ($Select == "DCSP_Rayl" || $Select == "DCSP_Compt"){
            $("div.xlib").hide();
            $("#int_z_or_comp, #energy, #theta, #phi").show();
        } else if ($Select.includes("Fi")) {
            $("div.xlib").hide();
            $("#int_z, #energy").show();
        } else if ($Select == "CosKronTransProb"){
            $("div.xlib").hide();
            $("#int_z, #cktrans").show();
        } else if ($Select == "ComptonProfile"){
            $("div.xlib").hide();
            $("#int_z, #pz").show();
        } else if ($Select == "ComptonProfile_Partial"){
            $("div.xlib").hide();
            $("#int_z, #pz, #shell").show();
        } else if ($Select == "MomentTransf"){
            $("div.xlib").hide();
            $("#energy, #theta").show();
        } else if ($Select == "Refractive_Index"){
            $("div.xlib").hide();
            $("#int_z_or_comp, #energy, #density").show();
        } else if ($Select == "CompoundParser"){
            $("div.xlib").hide();
            $("#comp").show();
        } else if ($Select == "GetRadioNuclideDataList"){
            $("div.xlib").hide();
        } else if ($Select == "GetRadioNuclideDataByIndex"){
            $("div.xlib").hide();
            $("#rad_nuc").show();
        } else if ($Select == "GetCompoundDataNISTList"){
            $("div.xlib").hide();
        } else if ($Select == "GetCompoundDataNISTByIndex"){
            $("div.xlib").hide();
            $("#nistcomp").show();
        };       
    };        
    
    function show_hide_code ($Select) {
        if ($Select == 'cpp-objdump') {
            $(".code-examples").hide();
            $(".cpp-objdump").show();
            $("#C/C++/Objective-C").show();
        } else if ($Select == 'fortran') {
            $(".code-examples").hide();
            $(".fortran").show();
        } else if ($Select == 'perl') {
            $(".code-examples").hide();
            $(".perl").show();
        } else if ($Select == 'idl') {
            $(".code-examples").hide();
            $(".idl").show();
        } else if ($Select == 'python') {
            $(".code-examples").hide();
            $(".python").show();
        } else if ($Select == 'java') {
            $(".code-examples").hide();
            $(".java").show();
        } else if ($Select == 'antlr-csharp') {
            $(".code-examples").hide();
            $(".antlr-csharp").show();
        } else if ($Select == 'lua') {
            $(".code-examples").hide();
            $(".lua").show();
        } else if ($Select == 'ruby') {
            $(".code-examples").hide();
            $(".ruby").show();
        } else if ($Select == 'php') {
            $(".code-examples").hide();
            $(".php").show();
        };
        
    };
   
    /*$("select#example").ready(function () {
        var $SelectExOnLoad = $("select#example").val();
        show_hide_code($SelectExOnLoad);
    }*/
    
    /* hides/shows examples as form changes */    
    $("select#examples").change(function(e) {
        var $SelectEx = $(this).val();                
        show_hide_code($SelectEx);
    });
    
    /* on page refresh or load (post form) */
    var $SelectOnLoad = $("select#function").val();
    show_hide_input($SelectOnLoad);
    
    /* hides/shows as form changes */
    $("select#function").change(function(e) {
        var $SelectVal = $(this).val();        
        show_hide_input($SelectVal);
    });
    
    /*shows appropriate select form for linetype*/
    $("input[type='radio']").change(function(e) {
        var $RadioVal = $(this).val();
        if ($RadioVal == "IUPAC") {
            $("#linetype-trans_iupac").show();
            $("#linetype-trans_siegbahn").hide();
        } else if ($RadioVal == "Siegbahn") {
            $("#linetype-trans_siegbahn").show();
            $("#linetype-trans_iupac").hide();
        } else if ($RadioVal == "All") {
            $("#linetype-trans_siegbahn, #linetype-trans_iupac").hide();
        };
    });    
});
