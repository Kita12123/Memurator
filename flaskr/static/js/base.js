//#######################################################################################
//    入力フォームクリア
//#######################################################################################
function clearClassValue(className){
    let elements = document.getElementsByClassName(className);
    for (let i = 0; i < elements.length; i++) {
        elements[i].value = "";
    }
}

//#######################################################################################
//    ロードアイコン表示
//#######################################################################################
function showLoading(){
    document.querySelector('#loading').style.display = '';
}