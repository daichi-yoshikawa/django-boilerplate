from django.core import paginator


class Paginator:
  DEFAULT_PAGE_SIZE = 20

  def __init__(self, query, query_params):
    try:
      self.page_size = int(query_params['page_size'])
      if self.page_size < 1:
        self.page_size = self.DEFAULT_PAGE_SIZE
    except Exception:
      self.page_size = self.DEFAULT_PAGE_SIZE

    self.query = query
    self.paginator = paginator.Paginator(query, self.page_size)
    self.page_size = self.page_size

  @property
  def pages(self):
    return self.paginator.page_range[-1]

  def get_page(self, query_params, allow_return_all=False):
    return_all = False

    try:
      page = int(query_params['page'])
    except Exception:
      page = 1
      return_all = allow_return_all

    if return_all:
      return paginator.Page(self.paginator.object_list, 1, self.paginator)
    return self.paginator.get_page(page)

  def get_profile(self):
    profile = {
      'pages': self.pages,
      'page_size': self.page_size,
    }
    return profile
