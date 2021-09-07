from server.app import app
import ssl

if __name__ == "__main__":
  ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
  ssl_context.load_cert_chain(certfile="ssl/certificate.crt", keyfile='ssl/private.key')
  app.run(host="0.0.0.0", port=5000, threaded=True, debug=True, ssl_context=ssl_context)
