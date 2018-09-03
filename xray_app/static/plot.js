$(document).ready(function () {    
    // clear text fields onfocus
    $("input[type='text']").on("focus", function(){
        $( this ).val('');
    });
    
    /* hides All option for transition until implemented */
    $("div#transition li:last-child").hide();
    
    
    //shows and hides fields depending on $Select
    function hideInputFields($Select) {
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
    
    //hides impossible iupac transitions
    function hideIUPAC ($select) {
        var shellsArray = new Array('K', 'L1', 'L2', 'L3', 'M1', 'M2', 'M3', 'M4', 'M5', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'O1', 'O2', 'O3', 'O4', 'O5', 'O6', 'O7', 'P1', 'P2', 'P3', 'P4', 'P5', 'Q1', 'Q2', 'Q3')
        
        var iupac2 = document.getElementById("transition-iupac2");
        var iupac2Selected = iupac2.options[iupac2.selectedIndex].value;
        
        $selectIndex = shellsArray.indexOf($select);
        $(iupac2).empty();
        
        var match = false;
        for (var i = $selectIndex+1 ; i < shellsArray.length ; i++) {
    	    iupac2.options.add(new Option(shellsArray[i], shellsArray[i]));
    	    if (shellsArray[i] == iupac2Selected) {
    	        iupac2.options[i-$selectIndex-1].selected = true;
    	        match = true;
    	    };
        };
        if (match == false) {
            iupac2.options[0].selected = true;
        };
    };
    
    // shows and hides transition select forms depending on $Radio
    function hideTransSelects ($Radio) {
        if ($Radio == "IUPAC") {
            $("#transition-iupac1, #transition-iupac2").show();
            $("#transition-siegbahn").hide();
        } else if ($Radio == "Siegbahn") {
            $("#transition-siegbahn").show();
            $("#transition-iupac1, #transition-iupac2").hide();
        } else if ($Radio == "All") {
            $("#transition-siegbahn, #transition-iupac1, #transition-iupac2").hide();
        };
    }; 
    
    // hides/shows as form changes
    $("select#transition-iupac1").change(function(e) {
        var $selectTrans = $(this).val();
        hideIUPAC($selectTrans);
    });
    
    // on page refresh or load (post form)
    var $SelectOnLoad = $("select#function").val();
    hideInputFields($SelectOnLoad);
    
    // hides/shows as form changes 
    $("select#function").change(function(e) {
        var $SelectVal = $(this).val();
        hideInputFields($SelectVal);
    });
    
    // shows select form for transition on change
    $("input[type='radio']").change(function(e) {
        var $RadioVal = $(this).val();
        hideTransSelects($RadioVal);        
    });
    
    // shows select form for transition on load
    var $RadioOnLoad = $("div#transition input[checked]").val();
    hideTransSelects($RadioOnLoad);
    
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
