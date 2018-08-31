$(document).ready(function () {
    /*$(document).on('change keyup', 'select#function', function(e) {
        var currentSelectVal = $(this).val();
        alert(currentSelectVal);
    })*/ 
    /* automatically assigns event handlers to elements that are specified by the selector (i.e select)*/
    
    // clear text fields onfocus
    $("input[type='text']").on("focus", function(){
        $( this ).val('');
    });        
    
    //shows and hides fields depending on $Select
    function show_hide_input($Select) {
        if ($Select == "AtomicWeight" || $Select == "ElementDensity") {
            $("div.xlib").hide();
            $("#int_z").show();
        } else if ($Select == "FF_Rayl" || $Select == "SF_Compt") {
            $("div.xlib").hide();
            $("#int_z, #float_q").show();
        } else if ($Select == "LineEnergy" || $Select == "RadRate"){
            $("div.xlib").hide();
            $("#int_z, #transition").show();
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
            $("#int_z, #transition, #energy").show();
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
    
    //shows and hides code examples depending on $Select
    function show_hide_code ($Select) {
        if ($Select == 'cpp-objdump') {
            $(".code-examples, .support-examples").hide();
            $(".cpp-objdump").show();
        } else if ($Select == 'fortran') {
            $(".code-examples, .support-examples").hide();
            $(".fortran").show();
        } else if ($Select == 'perl') {
            $(".code-examples, .support-examples").hide();
            $(".perl").show();
        } else if ($Select == 'idl') {
            $(".code-examples, .support-examples").hide();
            $(".idl").show();
        } else if ($Select == 'python') {
            $(".code-examples, .support-examples").hide();
            $(".python").show();
        } else if ($Select == 'java') {
            $(".code-examples, .support-examples").hide();
            $(".java").show();
        } else if ($Select == 'csharp') {
            $(".code-examples, .support-examples").hide();
            $(".csharp").show();
        } else if ($Select == 'lua') {
            $(".code-examples, .support-examples").hide();
            $(".lua").show();
        } else if ($Select == 'ruby') {
            $(".code-examples, .support-examples").hide();
            $(".ruby").show();
        } else if ($Select == 'php') {
            $(".code-examples, .support-examples").hide();
            $(".php").show();
        };
        
    };
    
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
    
    function validate_form($Select){
        if ($Select == "AtomicWeight" || $Select == "ElementDensity") {
            if (! $("input#int_z[value]").val()){
            return false;
            alert('not valid')
            } else {
            alert($("input#int_z[value]").val())
            };            
        };
    };
      
    // on page refresh or load (POST)
    var $SelectOnLoad = $("select#function").val();
    show_hide_input($SelectOnLoad);
    
    // hides/shows as form changes
    $("select#function").change(function(e) {
        var $SelectVal = $(this).val();        
        show_hide_input($SelectVal);
    });
   
    // shows select form for transition on change
    $("input[type='radio']").change(function(e) {
        var $RadioVal = $(this).val();
        show_hide_trans($RadioVal);
    });  
    
    // shows select form for transition on load
    var $RadioOnLoad = $("input[checked]").val();
    show_hide_trans($RadioOnLoad)
       
    // hides/shows examples as form changes 
    $("select#examples").change(function(e) {
        var $SelectEx = $(this).val();                
        show_hide_code($SelectEx);
    });    
        
    //on page refresh or load (POST) hides/shows examples
    var $Output = $("p#output").text();
    var $TableOutput = $("div#output").text();
    var $SuppEx = $("div.support-examples").text();
    
    if ($Output || $TableOutput && $SuppEx ) {
        $("div#examples").show();
        var $ExampleOnLoad = $("select#examples").val();
        show_hide_code($ExampleOnLoad);
    } else {
        $("div#examples, .support-examples, .code-examples").hide();
    }; 
      
    //if input empty on submission: block submission and display error next to empty field
    //need similar if function to show/hide? or is there a way to only need visible elements
    $("form").submit(function(event) {
          var $SelectedVal = $("select#function option[selected]").val();          
          alert( $SelectedVal );
          validate_form($SelectedVal);
    });
    //if energy = 0 display error: block submission  
});
