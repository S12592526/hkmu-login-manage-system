from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


# 基本分页：正常的查第几页，每页显示多少条的方式---》常用
class CommonPageNumberPagination(PageNumberPagination):
    # 4 个类属性
    page_size = 10  # 每页显示条数
    page_query_param = 'page'  # 查询页码参数  ?page=10
    page_size_query_param = 'size'  # ?page=3&size=5000
    max_page_size = 50  # 可以通过size控制每页显示的条数，但是通过这个参数控制最多显示多少条


# http://127.0.0.1:8000/books/?page=1&size=300000


# 偏移分页
class CommonLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10  # 每页显示多少条
    limit_query_param = 'limit'  # 取多少条
    offset_query_param = 'offset'  # 从第0个位置偏移多少开始取数据
    max_limit = 50  # 最大限制条数
    # offset=6&limit=90000
    # http://127.0.0.1:8000/books/?limit=3&offset=3  # 从第三条开始取3条

    # limit_query_description = _('Number of results to return per page.')


# 游标分页---》针对于大数据量分页效率高---》可控性差--->只能选择上一页和下一页，不能直接跳转到某一个
class CommonCursorPagination(CursorPagination):
    cursor_query_param = 'cursor'  # 查询的名字  等同于  page=xx
    page_size = 10  # 每页显示多少条
    ordering = 'id'  # 排序规则，必须是表中有的字段，一般用id
# http://127.0.0.1:8000/books/?cursor=cD0z
