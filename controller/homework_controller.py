from controller.base import BaseController

class HomeworkController(BaseController):
    
    @classmethod
    def get_hello_world(cls):
        try:
            return 'Hello!'
        except Exception as e:
            raise(e)

    @classmethod
    def post_hello_world(cls, item):
        try:
            res = {}
            if type(item) == dict and item.get("item_name") == "Apple":
                res['result'] = 'success'
            else:
                res['result'] = 'fail'
            return res
        except Exception as e:
            raise(e)