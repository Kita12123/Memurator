// ロードアイコン表示
function showLoading(){
    document.querySelector('#loading').style.display = '';
}
//main-form
function showForm(){
    document.querySelector('#extract').style.display   = '';
    document.querySelector('#extract-').style.display  = '';
    document.querySelector('#extract--').style.display = 'none';
}
function hideForm(){
    document.querySelector('#extract').style.display   = 'none';
    document.querySelector('#extract-').style.display  = 'none';
    document.querySelector('#extract--').style.display = '';
}
//明細データ
function showTable(){
    document.querySelector('#table').style.display    = '';
    document.querySelector('#totall1').style.display  = 'none';
    document.querySelector('#totall2').style.display  = 'none';
    document.querySelector('#totall3').style.display  = 'none';
}
//集計1
function showTotall1(){
    document.querySelector('#table').style.display    = 'none';
    document.querySelector('#totall1').style.display  = '';
    document.querySelector('#totall2').style.display  = 'none';
    document.querySelector('#totall3').style.display  = 'none';
}
//集計2
function showTotall2(){
    document.querySelector('#table').style.display    = 'none';
    document.querySelector('#totall1').style.display  = 'none';
    document.querySelector('#totall2').style.display  = '';
    document.querySelector('#totall3').style.display  = 'none';
}
//集計3
function showTotall3(){
    document.querySelector('#table').style.display    = 'none';
    document.querySelector('#totall1').style.display  = 'none';
    document.querySelector('#totall2').style.display  = 'none';
    document.querySelector('#totall3').style.display  = '';
}