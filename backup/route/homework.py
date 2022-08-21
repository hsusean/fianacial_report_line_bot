from flask import Blueprint
from flask import Flask, request, make_response
import json
from flasgger import swag_from
from controller.homework_controller import HomeworkController
blueprint = Blueprint('homework', __name__)

@blueprint.route("", methods=['GET'])
@swag_from('../document/homework/get_hello_world.yml')
def get_hello_world():
    try:
        result = HomeworkController.get_hello_world()
        return make_response(json.dumps(result), 200)
    except Exception as e:
        return make_response("Failure: %s." % str(e), 400)

@blueprint.route("", methods=['POST'])
@swag_from('../document/homework/post_hello_world.yml')
def post_hello_world():
    try:
        body = json.loads(request.data)
        result = HomeworkController.post_hello_world(body)
        return make_response(json.dumps(result), 200)
    except Exception as e:
        return make_response("Failure: %s." % str(e), 400)


