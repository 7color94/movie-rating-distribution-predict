//lightbox
function lightbox_close(e) {
    $('body').removeClass('noscroll');
    $('#lightbox').hide();
    $('#pjax').html('');
    history.pushState({},'',g_url_back);
};

$('#lightbox').click(function(e){
    if (e.target == this){
        lightbox_close(e);
    }
});

$(document).keyup(function(e) {
    if (e.keyCode == 27) {
        lightbox_close(e);
    }
});

//alerts
var delayTime  = 5000;
var alerts     = $('.messages.alert');

delayTime = delayTime + (alerts.length * 250);

alerts.each(function() {
    $(this).delay(delayTime).fadeOut('slow');
    delayTime -= 250;
});

//chosen
$('form.chosen select').chosen();

//popover
$('.pop-over').popover({
    placement: function(tip, element) {
            var offset = $(element).offset();
            height = $(document).outerHeight();
            width = $(document).outerWidth();
            vert = 0.5 * height - offset.top;
            vertPlacement = vert > 0 ? 'bottom' : 'top';
            horiz = 0.5 * width - offset.left;
            horizPlacement = horiz > 0 ? 'right' : 'left';
            placement = Math.abs(horiz) > Math.abs(vert) ?  horizPlacement : vertPlacement;
            return placement;
        }
});

$('.pop-over').click(function(e){
    $(this).popover('hide');
});

//message
Messenger.options = {
    extraClasses: 'messenger-fixed messenger-on-bottom messenger-on-right',
    theme: 'future',
};
function pop_msg(type,msg) {
    Messenger().post({
      message: msg,
      type: type,
      showCloseButton: true,
    });
};
function pop_info(msg) {pop_msg('info',msg)};
function pop_error(msg) {pop_msg('error',msg)};
function pop_success(msg) {pop_msg('success',msg)};

//baidu
var _hmt = _hmt || [];
(function() {
    var hm = document.createElement("script");
    hm.src = "//hm.baidu.com/hm.js?375aa6d601368176e50751c1c6bf0e82";
    var s = document.getElementsByTagName("script")[0];
    s.parentNode.insertBefore(hm, s);
})();

//google
(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','//www.google-analytics.com/analytics.js','ga');
ga('create', 'UA-40306673-1', 'readfree.me');
ga('send', 'pageview');

$('.z-link-search').click(function(){
    ga('send', 'event', 'link', 'click', 'z-link-search');
});

$('.z-link-product').click(function(){
    ga('send', 'event', 'link', 'click', 'z-link-product');
});

//btn js
function update_limit(css,title,left){
    var self = $('#id_limit');
    if (self.length){
        self.attr('class',css).attr('title',title).text(left);
    };
};

function disable_take(){
    var objs = $('.book-down,.book-push');
    if (objs.length){
        objs.attr('disabled','disabled');
        objs.attr('title','今日余额已用完');
    };
};

function on_book_push_click(){
    var self = $(this);
    var pk = $(this).data('pk');
    var pushmail = $(this).data('pushmail');
    var args = {pk: pk, pushmail: pushmail};
    $.get(g_url_push,args,function(data){
        var ret = data.ret;
        if (ret == 'ok') {
            if (self.is('button')) {
                self.find('span').text(data.count);
                self.addClass('btn-inverse').removeClass('btn-success');
                self.next('.dropdown-toggle').addClass('btn-inverse').removeClass('btn-success');
            } else {
                self.addClass('pushmail-inverse');
                self.parents('.btn-group').children('button').addClass('btn-inverse').removeClass('btn-success').find('.push-num').text(data.count);
            }
            update_limit(data.css,data.title,data.left);
            if (data.left < 1){
                disable_take();
            }
        } else {
            pop_info(ret);
        }
    })
}

function on_book_wish_click(){
    var self = $(this);
    var pk = self.closest('li').attr('pk');
    var args = {pk:pk};
    $.get(g_url_wish,args,function(data){
        var ret = data.ret;
        if (ret == 'ok') {
            self.find('span').text(data.count);
            self.toggleClass('btn-inverse').toggleClass('btn-success');
        } else {
            pop_info(ret);
        }
    })
}

g_pop_interval = 23 * 60 * 60 * 1000;

function on_book_down_click(){
    var self = $(this);
    var title = self.attr('title');
    var parent = self.closest('li');
    var count = self.find('span').text();
    var x = parseInt(count) + 1;
    self.find('span').text(x);
    self.addClass('btn-inverse').removeClass('btn-success');
    var limit_obj = $('#id_limit');
    if (limit_obj.length > 0){
        var left = parseInt(limit_obj.text());
        if (left > 0){
            left -= 1;
            limit_obj.text(left);
        };
        if (left < 3){
            limit_obj.css('badge badge-important');
        };
        if (left < 1){
            disable_take();
        };
    };
    if (false && g_show_ads && window.localStorage) {
        var key = "last_pop";
        var last_pop = localStorage.getItem(key, 0);
        var now = Date.now();
        if (now - last_pop > g_pop_interval) {
            localStorage.setItem(key, now);
            window.open('http://www.amazon.cn/gp/search?index=books&tag=readfreeme-23&keywords='+title,'_blank');
        }
    }
}

function bind_btn_click(){
    $('.book-push').click(on_book_push_click);
    $('.book-down').click(on_book_down_click);
    $('.book-wish').click(on_book_wish_click);
}

bind_btn_click();

$('.navbar-search-TODO').submit(function(e){
    var q = document.getElementById("q");
    if (q.value != "") {
        window.open('http://www.google.com/search?q=site:readfree.me  ' + q.value, "_blank");
    }
    return false;
});