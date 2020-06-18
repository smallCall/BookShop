/*
    name: UpImgs
    time: 2020
    author: 伊川
    email: 394853810@qq.com
    说明:
        UpImgs函数是为了完成web项目开发中的多图上传和多图修改封装的js的函数
        主要能够可以完成多图的预加载，并能进行多图片文件的表单上传，非ajax上传
        并且完成了web开发中多图修改的复杂性，使用更便捷
    案例：
     添加时：
            UpImgs(num=5,name="imgs")
     更新时：
            UpImgs(num=5,name="imgs",ajax_remove=function($this){
                // 获取 当前的图片id
                var imgid = $this.attr('imgid')
                // 判断当前imgID如果为真，则需要删除
                if(imgid){
                    $.get('/myadmin/books/imgs/delete',{'id':imgid},function(data){
                        console.log(data)
                    },'json')
                }
            })
*/

function UpImgs(num=5,name="imgs",func){
    if($('.upimg input[type="file"]').length < num){
        // 创建新的input控件
        createInput(name)
    }
    // 获取页面中的所有input type=file的上传的控件
    $(document).on('change','.upimg input[type="file"]',function(){
        //判断是否选择了图片
        if(this.files.length == 0){
            // 取消了图片的选择
             $(this).parents('li').find('.showimg').attr('src','')
        }else{
            // 加载图片
            readImgDateUrl(this,$(this))
            if($('.upimg input[type="file"]').length < num){
                // 创建新的input控件
                createInput(name)
            }

            // 设置删除的显示
            $(this).next('.showdiv').css('display','flex')
        }
    })

     // 获取图片删除元素，绑定事件，进行删除
    $(document).on('click','.showdiv',function(){
        func($(this))
        // 执行页面元素的删除
        $(this).parents('li').remove()
        // 判断长度
        if($('.upimg input[type="file"]').length < num){
            // 创建新的input控件
            createInput(name)
        }
    })
}

// 读取图片 dataurl
function readImgDateUrl($this,obj){
    // 获取当前用户选择的图片对象
    var file = $this.files[0]
    // 实例化文件读取对象
    var read = new FileReader()
    // 读取上传的文件数据为 DataURL
    read.readAsDataURL(file)
    // 读取成功后，显示
    read.onload = function(){
        obj.parents('li').find('.showimg').attr('src',this.result)
    }
}

// 创建 input
function createInput(name){
    var inp = $(' <li><img class="showimg" src="" alt=""><input type="file" name="'+name+'"><div class="showdiv"><img class="delete" src="/static/myupimg/delete.svg"></div></li>')
    $('.upimg').append(inp)
}



