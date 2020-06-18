window.onload = function() {
    var input = document.getElementById("upgteimg");
    var showui = document.getElementById("showui");
    var result;
    var dataArr = [];
    var fd;
    var showinput = document.getElementById("showinput");
    var oSubmit = document.getElementById("submit");
    var dateli, dateinput;
    var oldids = getimgid()

    // 获取原来的 图片id

    function getimgid(){
        var imgids = []
        $('#showimg').find('.showimg').each(function(){
            imgids.push($(this).attr('id'))
        })
        return imgids
    }

    function randomString(len) {
        len = len || 32;
        var $chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678';
        var maxPos = $chars.length;
        var pwd = '';
        for (i = 0; i < len; i++) {
            pwd += $chars.charAt(Math.floor(Math.random() * maxPos));
        }
        return pwd;
    }
    console.log()
    if (typeof FileReader === 'undefined') {
        alert("抱歉，你的浏览器不支持 FileReader");
        input.setAttribute('disabled', 'disabled');
    } else {
        input.addEventListener('change', readFile, false);
    }
    function readFile() {
        fd = new FormData();
        var iLen = this.files.length;
        var index = 0;
        var currentReViewImgIndex = 0;
        for (var i = 0; i < iLen; i++) {
            if (!input['value'].match(/.jpg|.gif|.png|.jpeg|.bmp/i)) {
                return alert("上传的图片格式不正确，请重新选择");
            }
            var reader = new FileReader();
            reader.index = i;
            fd.append(i, this.files[i]);
            reader.readAsDataURL(this.files[i]);
            reader.fileName = this.files[i].name;
            reader.files = this.files[i];
            reader.onload = function(e) {
                // console.log(this)
                var imgMsg = {
                    name: this.fileName,
                    base64: this.result,
                }
                dataArr.push(imgMsg);
                for (var j = 0; j < dataArr.length; j++) {
                    currentReViewImgIndex = j
                }
                result = '<div class="showdiv"><img class="left" src="/static/imgup/img/Arrow_left.svg" /><img class="center" src="/static/imgup/img/delete.svg" /><img class="right" src="/static/imgup/img/Arrow_right.svg" /></div><img id="' + this.fileName + '" class="showimg" src="' + this.result + '" />';
                var li = document.createElement('li');
                li.innerHTML = result;
                showui.appendChild(li);
                index++;
            }
        }
    }
    function onclickimg() {
        var dataArrlist = dataArr.length;
        var lilength = document.querySelectorAll('ul#showui li');
        for (var i = 0; i < lilength.length; i++) {
            lilength[i].getElementsByTagName('img')[0].onclick = function(num) {
                return function() {
                    if (num == 0) {} else {
                        var list = 0;
                        for (var j = 0; j < dataArr.length; j++) {
                            list = j
                        }
                        var up = num - 1;
                        dataArr.splice(up, 0, dataArr[num]);
                        dataArr.splice(num + 1, 1);
                        var lists = $("ul#showui li").length;
                        for (var j = 0; j < lists; j++) {
                            var usid = $("ul#showui li")[j].getElementsByTagName('img')[3];
                            $("#" + usid.id + "").attr("src", dataArr[j].base64)
                        }
                    }
                }
            }(i)
            lilength[i].getElementsByTagName('img')[1].onclick = function(num) {
                return function() {
                    if (dataArr.length == 1) {
                        dataArr = [];
                        $("ul#showui").html("")
                    } else {
                        $("ul#showui li:eq(" + num + ")").remove()
                        dataArr.splice(num, 1)
                    }
                }
            }(i)
            lilength[i].getElementsByTagName('img')[2].onclick = function(num) {
                return function() {
                    var list = 0;
                    for (var j = 0; j < dataArr.length; j++) {
                        list = j
                    }
                    var datalist = list + 1;
                    dataArr.splice(datalist, 0, dataArr[num]);
                    dataArr.splice(num, 1)
                    var lists = $("ul#showui li").length;
                    for (var j = 0; j < lists; j++) {
                        var usid = $("ul#showui li")[j].getElementsByTagName('img')[3];
                        $("#" + usid.id + "").attr("src", dataArr[j].base64)
                    }
                }
            }(i)
        }
    }
    showui.addEventListener("click",function() {
        onclickimg();
    },true)
    function send() {
        var names = ''
        for (var j = 0; j < dataArr.length; j++) {
            // console.log(dataArr[j].name)
            names += dataArr[j].name+','
        }
        names = names.substring(0,names.length-1)
        $('#booksform').append($('<input type="hidden" name="imgnames" value="'+names+'">'))
    }
    oSubmit.onclick = function() {

        if (!dataArr.length && !this.getAttribute('edit')){
            alert('请先选择文件');
            return false;
        }else{
            if(this.getAttribute('edit')){
                var newarr = getimgid()
                // console.log(newarr)// 上传的图片name
                names = ''
                for (var i = 0; i < newarr.length; i++) {
                    names += newarr[i]+','
                }
                names = names.substring(0,names.length-1)
                $('#booksform').append($('<input type="hidden" name="imgnames" value="'+names+'">'))

            }else{
                send()
            }

        }
    }
}
