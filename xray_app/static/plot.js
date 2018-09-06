$(document).ready(function () {    
    // Clear text fields onfocus
    $("input[type='text']").on("focus", function () {
        $( this ).val('');
    });
    
    // Hides All option for transition until implemented
    $("div#transition li:last-child").hide();
       
    // Shows and hides fields depending on $Select
    function hideInputFields ($Select) {
        if ($Select == "CS_Photo_Partial"){
            $("div.xlib").hide();
            $("#int_z, #shell").show();
        } else if ($Select == "CS_Total" 
                || $Select == "CS_Photo" 
                || $Select == "CS_Rayl" 
                || $Select == "CS_Compt" 
                || $Select == "CS_Energy" 
                || $Select == "CS_Photo_Total") {
            $("div.xlib").hide();
            $("#int_z_or_comp").show();
        } else if ($Select.includes("CS_FluorLine")) {
            $("div.xlib").hide();
            $("#int_z, #transition").show();
        };    
    };

    // Hides impossible iupac transitions
    function hideIUPAC ($select) {
        var shellsArray = ['K', 'L1', 'L2', 'L3', 'M1', 'M2', 'M3', 'M4', 'M5', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'O1', 'O2', 'O3', 'O4', 'O5', 'O6', 'O7', 'P1', 'P2', 'P3', 'P4', 'P5', 'Q1', 'Q2', 'Q3']
        
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
    
    // Shows and hides transition select forms depending on $Radio
    function hideTransSelects ($Radio) {
        if ($Radio == "IUPAC") {
            $("span#arrow, #transition-iupac1, #transition-iupac2").show();
=======
    // clear text fields onfocus
    $("input[type='text']").on("focus", function(){
        $( this ).val('');
    });
    
    // shows and hides transition select forms depending on $Radio
    function show_hide_trans ($Radio) {
    if ($Radio == "IUPAC") {
            $("#transition-iupac").show();
>>>>>>> 4751a09f2d96f772fb5dc83ad701ea069eda6856
            $("#transition-siegbahn").hide();
        } else if ($Radio == "Siegbahn") {
            $("#transition-siegbahn").show();
            $("span#arrow, #transition-iupac1, #transition-iupac2").hide();
        } else if ($Radio == "All") {
            $("span#arrow, #transition-siegbahn, #transition-iupac1, #transition-iupac2").hide();
        };
    }; 
    
    // Hides/shows as form changes
    $("select#transition-iupac1").change(function (e) {
        var $selectTrans = $(this).val();
        hideIUPAC($selectTrans);
    });
    
    // On page refresh or load (post form)
    var $SelectOnLoad = $("select#function").val();
    hideInputFields($SelectOnLoad);
    
    // Hides/shows as form changes 
    $("select#function").change(function (e) {
        var $SelectVal = $(this).val();
        hideInputFields($SelectVal);
    });
    
    // Shows select form for transition on change
    $("input[type='radio']").change(function (e) {
        var $RadioVal = $(this).val();
        hideTransSelects($RadioVal);        
    });
    
    // Shows select form for transition on load
    var $RadioOnLoad = $("div#transition input[checked]").val();
    hideTransSelects($RadioOnLoad);
    
    // Client side validation 
    $("form").submit(function (e) {
        var $Selected = $("select#function").val();
        if ($Selected == "CS_Photo_Partial"){
            if (!$("input#int_z[value]").val() 
                    || !$("input#range_start[value]").val()) {
                $(".empty-alert").show();
                return false;
            };
        } else if ($Selected == "CS_Total" 
                || $Selected == "CS_Photo" 
                || $Selected == "CS_Rayl" 
                || $Selected == "CS_Compt" 
                || $Selected == "CS_Energy" 
                || $Selected == "CS_Photo_Total") { 
            if (!$("input#int_z_or_comp[value]").val() || !$("input#range_start[value]").val() || !$("input#range_end[value]").val()) {
            $(".empty-alert").show();
            return false;
            };     
        } else if ($Selected.includes("CS_FluorLine")) { 
            if (!$("input#int_z[value]").val() 
                    || !$("input#range_start[value]").val() 
                    || !$("input#range_end[value]").val()) {
                $(".empty-alert").show();
                return false;
                };   
        };      
    });       
});

