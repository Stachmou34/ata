function decode_html(encoded) {
    const replacements = [
        ['&amp;gt;', '>'],
        ['&amp;lt;', '<'],
        ['\\\'', '\''],
        // ... other replacements
    ];
    return replacements.reduce((str, [find, replace]) => 
        str.replace(new RegExp(find, 'g'), replace), encoded);
}

function replaceAll(find, replace, str) {
    return str.replace(new RegExp(find, 'g'), replace);
}

function hoverbutton_pluginAppObj_45() {
    
        var container_btn = $('#pluginAppObj_45_container');
        var button = $('#pluginAppObj_45 .pluginAppObj_45-button');
    
    x5engine.boot.push(function(){
  
        var isMobile = x5engine.responsive.isMobileDevice !== 'undefined' && typeof x5engine.responsive.isMobileDevice === "function";
        if(isMobile && navigator.userAgent.toLowerCase().indexOf("android") > -1){
            $(container_btn).addClass("rem-highlight");
        }

        var eff = "sweep-top";
        switch(eff) {
            case "fade":
                fade();
                break;
            case "sweep-top":
            case "sweep-bottom":
            case "sweep-right":
            case "sweep-left":
                sweep();
                break;
            case "shutter-out-vertical":
            case "shutter-out-horizontal":
            case "shutter-radial-out":
                shutter();
                break;
            case "rotate-over":
                rotate_over();
                break;
            case "rotate-under":
                rotate_under();
                break;
        }  
    });
    
    function fade(){
        
        var timeout = 0;
        container_btn.on('mouseenter', function() {
            clearTimeout(timeout);
            var overElem = $('#pluginAppObj_45 .button-wrapper-over');
            if (overElem.length == 0) overElem = button.clone().addClass('button-wrapper-over fade').removeAttr('id').attr('id','pluginAppObj_45_overElem'). appendTo(container_btn);
            setTimeout(function() {
                overElem.addClass('animated');
            }, 10);
        }).on('mouseleave', function() {
            var overElem = $('#pluginAppObj_45 .button-wrapper-over');
            overElem.removeClass('animated');
            timeout = setTimeout(function() {
                overElem.remove();
            }, 300);
        });   
    }    
    
    function sweep(){
        
        var timeout = 0;
        container_btn.on('mouseenter', function() {
            clearTimeout(timeout);
            var overElem = container_btn.children('.sweeper');
            if (overElem.length == 0) overElem = button.clone().removeAttr('id').attr('id','pluginAppObj_45_overElem').appendTo(container_btn).wrap('<div class="sweeper"></div>').addClass('button-wrapper-over sweep').removeAttr('id').attr('id','pluginAppObj_45_overElemWrapper').css('width',button.css('width')).parent(); 
            setTimeout(function() {
                overElem.addClass('animated');
            }, 10);
        }).on('mouseleave', function() {
            var overElem = container_btn.children('.sweeper');
            overElem.removeClass('animated');
            timeout = setTimeout(function() {
                overElem.remove();
            }, 300);
        });
    }

    function shutter(){
        
        var timeout = 0;
        container_btn.on('mouseenter', function() {
            clearTimeout(timeout);
            var overElem = container_btn.children('.shutter');
            var cloneButton = button.clone();
            cloneButton.css('width', container_btn.css('width'));
            
            if (overElem.length == 0) overElem = cloneButton.clone().removeAttr('id').attr('id','pluginAppObj_45_overElem').appendTo(container_btn).wrap('<div class="shutter"></div>').addClass('button-wrapper-over').removeAttr('id').attr('id','pluginAppObj_45_overElemWrapper').parent();
            setTimeout(function() {
                overElem.addClass('animated');
            }, 10);
        }).on('mouseleave', function() {
            var overElem = container_btn.children('.shutter');
            overElem.removeClass('animated');
            timeout = setTimeout(function() {
                overElem.remove();
            }, 300);
        });
    }

    function rotate_under(){ 
        
        var timeout = 0;
        button.addClass('rotate-u');
        container_btn.on('mouseenter', function() {
            clearTimeout(timeout);  
            var overElem = container_btn.children('.rotate-under');
            if (overElem.length == 0) button.clone().addClass('button-wrapper-over rotate-under').removeAttr('id').attr('id','pluginAppObj_45_overElem').appendTo(container_btn);
            setTimeout(function() {
                button.addClass('animated');
            }, 10);
        }).on('mouseleave', function() {
            var overElem = container_btn.children('.rotate-under');
            button.removeClass('animated');
            timeout = setTimeout(function() {
                overElem.remove();
            }, 300);
        });
    }

    function rotate_over(){  

        var timeout = 0;
        container_btn.on('mouseenter', function() {
            clearTimeout(timeout);
            var overElem = container_btn.children('.rotate-over');
            if (overElem.length == 0) button.clone().addClass('button-wrapper-over rotate-over').removeAttr('id').attr('id','pluginAppObj_45_overElem').appendTo(container_btn);
            setTimeout(function() {
                container_btn.children('.rotate-over').addClass('animated');
            }, 10);
        }).on('mouseleave', function() {
            var overElem = container_btn.children('.rotate-over');
            overElem.removeClass('animated');
            timeout = setTimeout(function() {
                overElem.remove();
            }, 300);
        });   
    }
}