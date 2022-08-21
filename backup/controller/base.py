

""" Abstract base controller """
class BaseController:
    def get(self):
        raise NotImplementedError

    def list(self):
        raise NotImplementedError

    def create(self):
        raise NotImplementedError

    def update(self, update_body):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError