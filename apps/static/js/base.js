
//#######################################################################################
//    クラス内容クリア
//#######################################################################################
function clearClassValue(className){
    let elements = document.getElementsByClassName(className);
    for (let i = 0; i < elements.length; i++) {
        elements[i].value = "";
    }
}

//#######################################################################################
//    ID表示非表示
//#######################################################################################
function toggleID(id){
    $(id).fadeToggle(300);
}

//#######################################################################################
//    ロードアイコン表示
//#######################################################################################
function showLoading(){
    document.querySelector('#loading').style.display = '';
}

//#######################################################################################
//    トップページへ戻る
//#######################################################################################
$(function() {
    var pagetop = $('#page_top');   
    pagetop.hide();
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {  //100pxスクロールしたら表示
            pagetop.fadeIn();
        } else {
            pagetop.fadeOut();
        }
    });
    pagetop.click(function () {
        $('body,html').animate({
            scrollTop: 0
        }, 500); //0.5秒かけてトップへ移動
        return false;
    });
});