import flask

def format_response(success=True, data={}, msg=''):
    status = 'success' if success else 'failed'

    result = {
        'data' : data,
        'msg' : msg
    }
    return flask.jsonify(status=status, data=data, msg=msg)

