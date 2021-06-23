import hashlib
import hmac
import base64


class Signature:
    @staticmethod
    def generate(timestamp, method, uri, secretKey):
        message = "{}.{}.{}".format(timestamp, method, uri)
        hash = hmac.new(bytes(secretKey, "utf-8"),
                        bytes(message, "utf-8"), hashlib.sha256)

        hash.hexdigest()
        return base64.b64encode(hash.digest())
