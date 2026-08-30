mkdir -p server/certs
openssl genrsa -out server/certs/server.key 4096
openssl req -new -x509 -key server.key -out server.crt -days 365 -config cert.conf -extensions v3_req