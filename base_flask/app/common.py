from flask import jsonify, make_response


class ResponseGenerator:
    @staticmethod
    def generate_response(status_code, status, data=None, message=None):
        return make_response(
            jsonify(
                {
                    "status_code": status_code,
                    "status": status,
                    "data": data if data else {},
                    "message": message,
                }
            ),
            status_code,
        )


def log(content, char):
    print(char * 40)
    print(content)
    print(char * 40)
