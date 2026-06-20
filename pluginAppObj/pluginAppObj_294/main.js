function logoslider_pluginAppObj_294(param) {
    
    var MIN_WIDTH_SIZE = 128;
    var resizing = false;
    var itemVisible = param.itemVisible;
    var pluginAppObj_294_resizeTo = null,
		pluginAppObj_294_width = 0;
    
    x5engine.boot.push(function(){     
        addEvents();
        init();
    
        x5engine.utils.onElementResize(document.getElementById("pluginAppObj_294"), function (rect, target) {
            if (pluginAppObj_294_width == rect.width) {
                return;
            }
            pluginAppObj_294_width = rect.width;
            if (!!pluginAppObj_294_resizeTo) {
                clearTimeout(pluginAppObj_294_resizeTo);
            }
            if ( false && (rect.width == 0 || document.hidden) ) {
                //if the window was hidden/minimized so will jump eventResize
                resizing = true;
            }
            pluginAppObj_294_resizeTo = setTimeout(function() {}, 50);   
        });
    });

    function init() {
        param.carousel.empty().append(buildHtml());
        setPathImage();
        setup();
    }

    function setPathImage() {
        if ( false ) {
            return;    
        }
            
        var imagesPath = ['pluginAppObj/pluginAppObj_294/logo-Yanassur-Assurance.png','pluginAppObj/pluginAppObj_294/logo-assuranceendirect.jpg','pluginAppObj/pluginAppObj_294/logo-elvire.jpg','pluginAppObj/pluginAppObj_294/logo_direct-temporaires.png','pluginAppObj/pluginAppObj_294/logo-global-assurances.jpg','pluginAppObj/pluginAppObj_294/logo-Car-Protection-Services.png','pluginAppObj/pluginAppObj_294/logo-assu-temporaire.png','pluginAppObj/pluginAppObj_294/logo-Arthur-assurance.png','pluginAppObj/pluginAppObj_294/logo-assur-tempo.jpg','pluginAppObj/pluginAppObj_294/logo-TAP-ASSURANCE.png'];
             
        $('#pluginAppObj_294 .logo-slide-img').each(function(i, obj) {
            var path = x5engine.settings.currentPath + imagesPath[i];
            $(this).css("background-image", 'url(' + path + ')');
            $(this).find("img").attr("src", path);
        });
    }
    
    function setup() {
        param.carousel.owlCarousel({
            items: itemVisible,
            loop: param.autoplay ? true: false,
            margin: param.margin,
            nav: false,
            autoplay: param.autoplay,
            smartSpeed: param.animationDuration,
            autoplayTimeout: param.autoplayMode == "continuousScrolling" &&  param.autoplay ? param.animationDuration : param.autoplayTimeout,
            autoplaySpeed: param.animationDuration,
            slideTransition: param.autoplayMode == "continuousScrolling" &&  param.autoplay ? 'linear' : 'cubic-bezier(0.25, 0.1, 0.25, 1)',
            autoplayHoverPause: param.autoplayHoverPause,
            dots: param.dots
        });
    }

    function addEvents() {
        param.carousel.on('refresh.owl.carousel', eventResize);   
        $("#pluginAppObj_294_container .owl-carousel .item").bind('touchstart', function(event) {
            $(this).addClass("zoom");
        });     
        $("#pluginAppObj_294_container .owl-carousel .item").bind('touchend', function(event) {
            $(this).removeClass("zoom");
        });
    }

    function eventResize() {
        if(resizing){
            return;
        }
        resizing = true;
        resize();
        resizing = false;
    }

    function resize() {
        var widthSlider = getWidthSingleSlider(); 
        if(param.preview || ((widthSlider >= MIN_WIDTH_SIZE) && (itemVisible == param.itemVisible))){
            setBackgroundSize(widthSlider);
            return;
        }
        else if((widthSlider > MIN_WIDTH_SIZE) && (itemVisible < param.itemVisible)){
            do {
                itemVisible++;
                itemVisible = Math.min(itemVisible, param.itemVisible); //security control
                widthSlider = getWidthSingleSlider(); 
            } while((widthSlider > MIN_WIDTH_SIZE) && (itemVisible < param.itemVisible));
        }
        else if(widthSlider < MIN_WIDTH_SIZE){
            if(itemVisible > 1) {
                do {
                    itemVisible--;
                    itemVisible = Math.max(itemVisible, 1); //security control
                    widthSlider = getWidthSingleSlider(); 
                } while(widthSlider < MIN_WIDTH_SIZE);
            }
        }
        //destroy and reinizialize
        param.carousel.owlCarousel('destroy'); 
        init();
        setBackgroundSize(widthSlider);
    }

    function getWidthSingleSlider() {
        return parseInt((param.container.width() / itemVisible) - (param.margin / 2))
    }

    function setBackgroundSize(widthSlider) {
        var realImageWidth = 0;
        var realImageHeight = 0;
        var maxHeight = 0;
        if(!param.preview){
            $("#pluginAppObj_294_container .owl-carousel .owl-item .logo-slide-img").css("background-size", ""); 
            $("#pluginAppObj_294_container .owl-carousel .owl-item .logo-slide-img").each(function(index,item){
                var imageWidth = $(item).data("width");
                var imageHeight = $(item).data("height");
                if(imageWidth > imageHeight){
                    realImageHeight = parseInt((imageHeight * widthSlider)/ imageWidth);
                    realImageWidth = widthSlider;
                }
                else{
                    realImageWidth = parseInt((imageWidth * widthSlider)/ imageHeight);
                    realImageHeight = widthSlider;
                }
                
                var finalImageHeight;     
                if(realImageWidth > imageWidth && realImageHeight > imageHeight) {
                    $(item).css("background-size", imageWidth + "px " + imageHeight + "px");
                    finalImageHeight = imageHeight;
                }
                else {
                    finalImageHeight = realImageHeight;
                }
                maxHeight = Math.max(finalImageHeight, maxHeight);
            });
            $("#pluginAppObj_294_container .owl-carousel .owl-stage .owl-item").css("height", maxHeight);
        }
    }

    function buildHtml() {   
        var allItems = "<div class='item link described zoom'><a href='https://yanassur.com/assurance-temporaire.php' target='_blank'><div title='DEVIS ASSURANCE TEMPORAIRE EN LIGNE' class='logo-slide-img' data-index='0' data-height='71' data-width='201' style='background-image: url(pluginAppObj/pluginAppObj_294/logo-Yanassur-Assurance.png)'><img src='pluginAppObj/pluginAppObj_294/logo-Yanassur-Assurance.png' style='visibility: hidden; max-height:71px; max-width:201px;' /></div></a></div><div class='item link described zoom'><a href='https://www.assurance-voiture-temporaire-provisoire.com/assurance-temporaire-auto-camion-poids-lourds-camping-car-remorque.html?obf' target='_blank'><div title='Choisissez le véhicule à assurer' class='logo-slide-img' data-index='1' data-height='72' data-width='222' style='background-image: url(pluginAppObj/pluginAppObj_294/logo-assuranceendirect.jpg)'><img src='pluginAppObj/pluginAppObj_294/logo-assuranceendirect.jpg' style='visibility: hidden; max-height:72px; max-width:222px;' /></div></a></div><div class='item link described zoom'><a href='https://www.elvire-broker.com/' target='_blank'><div title='L’assurance auto temporaire immédiate en ligne pour rouler protégé' class='logo-slide-img' data-index='2' data-height='102' data-width='204' style='background-image: url(pluginAppObj/pluginAppObj_294/logo-elvire.jpg)'><img src='pluginAppObj/pluginAppObj_294/logo-elvire.jpg' style='visibility: hidden; max-height:102px; max-width:204px;' /></div></a></div><div class='item link described zoom'><a href='https://direct-temporaires.fr/' target='_blank'><div title='Assurance temporaire auto en ligne et pas cher' class='logo-slide-img' data-index='3' data-height='25' data-width='186' style='background-image: url(pluginAppObj/pluginAppObj_294/logo_direct-temporaires.png)'><img src='pluginAppObj/pluginAppObj_294/logo_direct-temporaires.png' style='visibility: hidden; max-height:25px; max-width:186px;' /></div></a></div><div class='item link described zoom'><a href='https://globalassurances.re/auto-provisoire/' target='_blank'><div title='Devis et Souscription Temporaire en moins de 5 min à La Réunion' class='logo-slide-img' data-index='4' data-height='43' data-width='256' style='background-image: url(pluginAppObj/pluginAppObj_294/logo-global-assurances.jpg)'><img src='pluginAppObj/pluginAppObj_294/logo-global-assurances.jpg' style='visibility: hidden; max-height:43px; max-width:256px;' /></div></a></div><div class='item link zoom'><a href='https://carprotectionservices.com/' target='_blank'><div class='logo-slide-img' data-index='5' data-height='110' data-width='245' style='background-image: url(pluginAppObj/pluginAppObj_294/logo-Car-Protection-Services.png)'><img src='pluginAppObj/pluginAppObj_294/logo-Car-Protection-Services.png' style='visibility: hidden; max-height:110px; max-width:245px;' /></div></a></div><div class='item link described zoom'><a href='https://assutemporaire.fr/' target='_blank'><div title='Assurer son véhicule en 10 minutes avec nous, c’est possible ! ' class='logo-slide-img' data-index='6' data-height='160' data-width='250' style='background-image: url(pluginAppObj/pluginAppObj_294/logo-assu-temporaire.png)'><img src='pluginAppObj/pluginAppObj_294/logo-assu-temporaire.png' style='visibility: hidden; max-height:160px; max-width:250px;' /></div></a></div><div class='item link described zoom'><a href='https://www.arthurassurance.fr/assurance-temporaire-provisoire' target='_blank'><div title='Assurance occasionnelle de courte durée en Martinique et Guadeloupe' class='logo-slide-img' data-index='7' data-height='96' data-width='256' style='background-image: url(pluginAppObj/pluginAppObj_294/logo-Arthur-assurance.png)'><img src='pluginAppObj/pluginAppObj_294/logo-Arthur-assurance.png' style='visibility: hidden; max-height:96px; max-width:256px;' /></div></a></div><div class='item link described zoom'><a href='https://assur-tempo.com/' onclick='return x5engine.imShowBox({ media:[{type: 'iframe', url: 'https://assur-tempo.com/', width: 1920, height: 1080, description: ''}]}, 0, this);'><div title='L'assurance temporaire à Marseille c'est Assur-Tempo !' class='logo-slide-img' data-index='8' data-height='102' data-width='256' style='background-image: url(pluginAppObj/pluginAppObj_294/logo-assur-tempo.jpg)'><img src='pluginAppObj/pluginAppObj_294/logo-assur-tempo.jpg' style='visibility: hidden; max-height:102px; max-width:256px;' /></div></a></div><div class='item link described zoom'><a href='https://tap-assurances.fr/particuliers/assurance-temporaire/' target='_blank'><div title=' On vous assure directement ' class='logo-slide-img' data-index='9' data-height='166' data-width='256' style='background-image: url(pluginAppObj/pluginAppObj_294/logo-TAP-ASSURANCE.png)'><img src='pluginAppObj/pluginAppObj_294/logo-TAP-ASSURANCE.png' style='visibility: hidden; max-height:166px; max-width:256px;' /></div></a></div>";  
        return allItems;
    }    
}