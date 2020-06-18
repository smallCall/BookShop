from django import template
from django.utils.html import format_html
register = template.Library()


# 自定义过滤器
@register.filter
def xjq_upper(val):
    return val.upper()


@register.simple_tag
def jia(a, b):
    return int(a) + int(b)


# 自定义分页页码的显示的标签
@register.simple_tag
def show_page(total_page, request):
    # 要求，显示的页码数不能超过十个

    # 定义开头显示的页码和结尾显示的页码
    page_now = request.GET.get('page', 1)
    page_now = int(page_now)
    start = page_now-5
    end = page_now+5

    if not total_page:
        return ''

    # 判断，当前页面处于左右两边的临界区域
    if page_now < 6:
        start = 1
        end = 10
    if page_now > total_page-4:
        start = total_page-9
        end = total_page
    if total_page <= 10:
        start = 1
        end = total_page

    page_html = ''
    page_html += f'<li><a href="?page={1}">首页</a></li>'
    if page_now-1 < 1:
        page_html += f'<li class="am-disabled"><a href="?page={page_now - 1}">上一页</a></li>'
    else:
        page_html += f'<li><a href="?page={page_now-1}">上一页</a></li>'
    for i in range(start, end+1):
        # 如果是当前页，需要高亮
        if i == page_now:
            page_html += f'<li class="am-active" ><a href="?page={i}">{i}</a></li>'
        else:
            page_html += f'<li><a href="?page={i}">{i}</a></li>'

    if page_now + 1 > total_page:
        page_html += f'<li class="am-disabled"><a href="?page={page_now + 1}">下一页</a></li>'
    else:
        page_html += f'<li><a href="?page={page_now + 1}">下一页</a></li>'
    page_html += f'<li><a href="?page={total_page}">尾页</a></li>'
    return format_html(page_html)