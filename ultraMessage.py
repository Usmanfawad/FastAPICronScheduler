import http.client
import ssl


def send_message(destination_number, body):
    print("Sending message")
    CONN = http.client.HTTPSConnection("api.ultramsg.com", context=ssl._create_unverified_context())
    payload = f"token=p25i2oy53uwkyte4&to=+923352839515&body={body}"
    payload = payload.encode('utf8').decode('iso-8859-1')
    headers = {'content-type': "application/x-www-form-urlencoded"}
    CONN.request("POST", "/instance53326/messages/chat", payload, headers)
    res = CONN.getresponse()
    data = res.read()
    print("Message sent")

