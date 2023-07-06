import http.client
import ssl


def send_message(destination_number, body):
    CONN = http.client.HTTPSConnection("api.ultramsg.com", context=ssl._create_unverified_context())
    payload = f"token=p25i2oy53uwkyte4&to={destination_number}&body={body}"
    payload = payload.encode('utf8').decode('iso-8859-1')
    headers = {'content-type': "application/x-www-form-urlencoded"}
    CONN.request("POST", "/instance53131/messages/chat", payload, headers)
    res = CONN.getresponse()
    data = res.read()


