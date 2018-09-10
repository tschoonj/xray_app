// Extends jQuery methods with custom method
// Filters Select element using text input
// $("selectElement").filterSelect($("textInputElement"))
jQuery.fn.filterSelect = function (textinput) {
    return this.each(function () {
        var select = this;
        var options = [];
        $(select).find('option').each(function () {
            options.push({
                value: $(this).val(),
                text: $(this).text()
            });
        });
    
        $(select).data('options', options);

        $(textinput).on('change keyup', function () {
            var options = $(select).empty().data('options');
            var filter = $.trim($(this).val());
            var regex = new RegExp(filter, "gi");

            $.each(options, function (i) {
                var option = options[i];
                if (option.text.match(regex) !== null) {
                    $(select).append(
                    $('<option>').text(option.text).val(option.value)
                    );
                };
            });
        });
    });
};

$(document).ready(function () {
    // $ indicates a jQuery object
    
    // Clears text fields onfocus
    $(".xlib input[type='text']").on("focus", function () {
        $( this ).val('');
    });        
    
    // Filters function select element on keyup
    $("select#function").filterSelect($("input#function"));
    // Filters NIST compounds select element on keyup
    $("select#nistcomp").filterSelect($("input#nistcomp"))
    
    // Shows and hides fields depending on $select
    function hideInputFields ($select) {
        if ($select == "AtomicWeight" || $select == "ElementDensity") {
            $("div.xlib").hide();
            $("#int_z").show();
        } else if ($select == "FF_Rayl" || $select == "SF_Compt") {
            $("div.xlib").hide();
            $("#int_z, #float_q").show();
        } else if ($select == "LineEnergy" || $select == "RadRate"){
            $("div.xlib").hide();
            $("#int_z, #transition").show();
        } else if ($select == "AugerRate"){
            $("div.xlib").hide();
            $("#int_z, #augtrans").show();
        } else if ($select == "EdgeEnergy" 
                || $select == "JumpFactor" 
                || $select == "FluorYield" 
                || $select == "AugerYield" 
                || $select == "AtomicLevelWidth" 
                || $select == "ElectronConfig") {
            $("div.xlib").hide();
            $("#int_z, #shell").show();
        } else if ($select == "CS_Photo_Partial"){
            $("div.xlib").hide();
            $("#int_z, #shell, #energy").show();
        } else if ($select == "CS_KN"){
            $("div.xlib").hide();
            $("#energy").show();

        } else if ($select == "CS_Total" 
                || $select == "CS_Photo" 
                || $select == "CS_Rayl" 
                || $select == "CS_Compt" 
                || $select == "CS_Energy"){
            $("div.xlib").hide();
            $("#int_z_or_comp, #energy").show();
        } else if ($select.includes("CS_FluorLine")){
            $("div.xlib").hide();
            $("#int_z, #transition, #energy").show();
        } else if ($select == "DCS_KN" || $select == "ComptonEnergy"){
            $("div.xlib").hide();
            $("#energy, #theta").show();
        } else if ($select == "DCS_Thoms"){
            $("div.xlib").hide();
            $("#theta").show();
        } else if ($select == "DCS_Rayl" || $select == "DCS_Compt"){
            $("div.xlib").hide();
            $("#int_z_or_comp, #energy, #theta").show();
        } else if ($select == "DCSP_KN"){
            $("div.xlib").hide();
            $("#energy, #theta, #phi").show();
        } else if ($select == "DCSP_Thoms"){
            $("div.xlib").hide();
            $("#theta, #phi").show();
        } else if ($select == "DCSP_Rayl" || $select == "DCSP_Compt"){
            $("div.xlib").hide();
            $("#int_z_or_comp, #energy, #theta, #phi").show();
        } else if ($select.includes("Fi")) {
            $("div.xlib").hide();
            $("#int_z, #energy").show();
        } else if ($select == "CosKronTransProb"){
            $("div.xlib").hide();
            $("#int_z, #cktrans").show();
        } else if ($select == "ComptonProfile"){
            $("div.xlib").hide();
            $("#int_z, #pz").show();
        } else if ($select == "ComptonProfile_Partial"){
            $("div.xlib").hide();
            $("#int_z, #pz, #shell").show();
        } else if ($select == "MomentTransf"){
            $("div.xlib").hide();
            $("#energy, #theta").show();
        } else if ($select == "Refractive_Index"){
            $("div.xlib").hide();
            $("#int_z_or_comp, #energy, #density").show();
        } else if ($select == "CompoundParser"){
            $("div.xlib").hide();
            $("#comp").show();
        } else if ($select == "GetRadioNuclideDataList"){
            $("div.xlib").hide();
        } else if ($select == "GetRadioNuclideDataByIndex"){
            $("div.xlib").hide();
            $("#rad_nuc").show();
        } else if ($select == "GetCompoundDataNISTList"){
            $("div.xlib").hide();
        } else if ($select == "GetCompoundDataNISTByIndex"){
            $("div.xlib").hide();
            $("#nistcomp").show();
        };       
    };        
    
    // Shows and hides code examples depending on $select
    function hideCode ($select) {
        if ($select == 'cpp-objdump') {
            $(".code-examples, .support-examples").hide();
            $(".cpp-objdump").show();
        } else if ($select == 'fortran') {
            $(".code-examples, .support-examples").hide();
            $(".fortran").show();
        } else if ($select == 'perl') {
            $(".code-examples, .support-examples").hide();
            $(".perl").show();
        } else if ($select == 'idl') {
            $(".code-examples, .support-examples").hide();
            $(".idl").show();
        } else if ($select == 'python') {
            $(".code-examples, .support-examples").hide();
            $(".python").show();
        } else if ($select == 'java') {
            $(".code-examples, .support-examples").hide();
            $(".java").show();
        } else if ($select == 'csharp') {
            $(".code-examples, .support-examples").hide();
            $(".csharp").show();
        } else if ($select == 'lua') {
            $(".code-examples, .support-examples").hide();
            $(".lua").show();
        } else if ($select == 'ruby') {
            $(".code-examples, .support-examples").hide();
            $(".ruby").show();
        } else if ($select == 'php') {
            $(".code-examples, .support-examples").hide();
            $(".php").show();
        };
        
    };
    
    // Shows and hides transition select forms depending on $Radio
    function hideTransSelects ($Radio) {
        if ($Radio == "IUPAC") {
            $("span#arrow, #transition-iupac1, #transition-iupac2").show();
            $("#transition-siegbahn").hide();
        } else if ($Radio == "Siegbahn") {
            $("#transition-siegbahn").show();            
            $("span#arrow, #transition-iupac1, #transition-iupac2").hide();
        } else if ($Radio == "All") {
            $("span#arrow, #transition-siegbahn, #transition-iupac1, #transition-iupac2").hide();
        };
    };   
    

    // Hides impossible IUPAC transitions
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
    
    // Hides impossible auger transitions
    function hideAuger1 ($select) {
        var shellsArray = ['K', 'L1', 'L2', 'L3', 'M1', 'M2', 'M3', 'M4', 'M5', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'O1', 'O2', 'O3', 'O4', 'O5', 'O6', 'O7', 'P1', 'P2', 'P3', 'P4', 'P5', 'Q1', 'Q2', 'Q3']
        var transShell = document.getElementById("augtrans-trans_shell");
        var transSelected = trans_shell.options[trans_shell.selectedIndex].value;
    
        $selectIndex = shellsArray.indexOf($select);
        $(transShell).empty();
    
        var match = false;
        for (var i = $selectIndex+1 ; i < 9 ; i++) {
            transShell.options.add(new Option(shellsArray[i], shellsArray[i]));
            if (shellsArray[i] == transSelected) {
                transShell.options[i-$selectIndex-1].selected = true;
                match = true;
            };
        };
        if (match == false) {
        transShell.options[0].selected = true;
        };    
    };
    
    function hideAuger2 ($select) {
        var shellsArray = ['K', 'L1', 'L2', 'L3', 'M1', 'M2', 'M3', 'M4', 'M5', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'O1', 'O2', 'O3', 'O4', 'O5', 'O6', 'O7', 'P1', 'P2', 'P3', 'P4', 'P5', 'Q1', 'Q2', 'Q3']
        var augShell = document.getElementById("augtrans-aug_shell");
        var augSelected = aug_shell.options[aug_shell.selectedIndex].value;
    
        $selectIndex = shellsArray.indexOf($select);
        $(augShell).empty();
    
        var match = false;
        for (var i = $selectIndex+1 ; i < shellsArray.length ; i++) {
    	    augShell.options.add(new Option(shellsArray[i], shellsArray[i]));
    	    if (shellsArray[i] == augSelected) {
    	        augShell.options[i-$selectIndex-1].selected = true;
    	        match = true;
    	    };
        };
        if (match == false) {
            augShell.options[0].selected = true;
        };    
    };      
    
    
    $("select#augtrans-ex_shell").change(function (e) {
        var $selectAug = $(this).val();
        hideAuger1($selectAug);
    });
    
    $("select#augtrans-trans_shell").change(function (e) {
        var $selectAug = $(this).val();
        hideAuger2($selectAug);
    });
    
    // Hides/shows as form changes
    $("select#transition-iupac1").change(function (e) {
        var $selectTrans = $(this).val();
        hideIUPAC($selectTrans);
    });
       
    // On page refresh or load (POST)
    var $selectOnLoad = $("select#function").val();
    hideInputFields($selectOnLoad);
    
    // Hides/shows as form changes
    $("select#function").change(function (e) {
        var $selectVal = $(this).val();        
        hideInputFields($selectVal);
    });
   
    // Hides/shows on key up of search
    $("input#function").keyup(function (e) {
        $("select#function").change();
    });
    
    // Shows select form for transition on change
    $("input[type='radio']").change(function (e) {
        var $RadioVal = $(this).val();
        hideTransSelects($RadioVal);
    });  
    
    // Shows select form for transition on load
    var $RadioOnLoad = $("input[checked]").val();
    hideTransSelects($RadioOnLoad);
       
    // Hides/shows examples as form changes 
    $("select#examples").change(function (e) {
        var $selectEx = $(this).val();                
        hideCode($selectEx);
    });    
        
    // On page refresh or load (POST) hides/shows examples
    // Only shows if output or table output
    var $output = $("p#output").text();
    var $tableOutput = $("div#output").text();
    var $suppEx = $("div.support-examples").text();
    
    if ($output == 'Error') {
        $("div#examples, .support-examples, .code-examples").hide();
    } else if ($output || $tableOutput && $suppEx ) {
        $("div#examples").show();
        var $exampleOnLoad = $("select#examples").val();
        hideCode($exampleOnLoad);
    } else {
        $("div#examples, .support-examples, .code-examples").hide();
    }; 
          
    // Client side validation 
    $("form").submit(function (e) {
        var $selected = $("select#function").val();        
        // If energy = 0 display error: block submission
        if ($("input#energy[value]").val() == 0) {
            $(".energy-alert").show();
            return false;
        };
        // If input empty on submission: block submission and display empty field error
        if ($selected == "AtomicWeight" 
                || $selected == "ElementDensity" 
                || $selected == "LineEnergy" 
                || $selected == "RadRate" 
                || $selected == "EdgeEnergy" 
                || $selected == "JumpFactor" 
                || $selected == "FluorYield" 
                || $selected == "AugerYield" 
                || $selected == "AtomicLevelWidth" 
                || $selected == "ElectronConfig" 
                || $selected == "CosKronTransProb" 
                || $selected == "AugerRate") {
            if (!$("input#int_z[value]").val()) {
                $(".empty-alert").show();
                return false;
            };
        } else if ($selected == "FF_Rayl" || $selected == "SF_Compt") {
            if (!$("input#int_z[value]").val() 
                    || !$("input#float_q[value]").val()) {
                $(".empty-alert").show();
                return false;
            };
        } else if ($selected == "CS_Photo_Partial" 
                || $selected.includes("CS_FluorLine") 
                || $selected.includes("Fi")) {
            if (!$("input#int_z[value]").val() || !$("input#energy[value]").val()) {
                $(".empty-alert").show();
                return false;
            };
        } else if ($selected == "CS_Total" 
                || $selected == "CS_Photo" 
                || $selected == "CS_Rayl" 
                || $selected == "CS_Compt" 
                || $selected == "CS_Energy"){
            if (!$("input#int_z_or_comp[value]").val() 
                    || !$("input#energy[value]").val()) {
                $(".empty-alert").show();
                return false;
            };               
        } else if ($selected == "DCS_KN" 
                || $selected == "ComptonEnergy" 
                || $selected == "MomentTransf"){
            if (!$("input#energy[value]").val() 
                    || !$("input#theta[value]").val()) {
                $(".empty-alert").show();
                return false;
            };
        } else if ($selected == "DCS_Thoms"){
            if (!$("input#theta[value]").val()) {
                $(".empty-alert").show();
                return false;
            };
        } else if ($selected == "DCS_Rayl" || $selected == "DCS_Compt") {
            if (!$("input#int_z_or_comp[value]").val() 
                    || !$("input#energy[value]").val() 
                    || !$("input#theta[value]").val()) {
                $(".empty-alert").show();
                return false;
            };
        } else if ($selected == "DCSP_KN") {
            if (!$("input#phi[value]").val() 
                    || !$("input#energy[value]").val() 
                    || !$("input#theta[value]").val()) {
                $(".empty-alert").show();
                return false;
            };
        } else if ($selected == "DCSP_Thoms") {
            if (!$("input#phi[value]").val() 
                    || !$("input#theta[value]").val()) {
                $(".empty-alert").show();
                return false;
            };
        } else if ($selected == "DCSP_Rayl" || $selected == "DCSP_Compt") {
            if (!$("input#int_z_or_comp[value]").val()
                    || !$("input#energy[value]").val()
                    || !$("input#theta[value]").val() 
                    || !$("input#phi[value]").val()) {
                $(".empty-alert").show();
                return false;
            };
        } else if ($selected == "ComptonProfile" || $selected == "ComptonProfile_Partial") {
            if (!$("input#int_z[value]").val() 
                    || !$("input#pz[value]").val()) {
                $(".empty-alert").show();
                return false;
            };
        } else if ($selected == "Refractive_Index") {
            if (!$("input#int_z_or_comp[value]").val() 
                    || !$("input#energy[value]").val() 
                    || !$("input#density[value]").val()) {
                $(".empty-alert").show();
                return false;
            };
        } else if ($selected == "CompoundParser") {
            if (!$("input#comp[value]").val()) {
                $(".empty-alert").show();
                return false;
            };     
        };    
    });           
});

