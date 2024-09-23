import os
import json
import aiohttp

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
VERSION = os.getenv("VERSION")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")


async def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }

    async with aiohttp.ClientSession() as session:
        url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
        try:
            async with session.post(
                url, json=json.loads(data), headers=headers
            ) as response:
                if response.status == 200:
                    print("Status:", response.status)
                    print("Content-type:", response.headers["content-type"])
                    html = await response.text()
                    print("Body:", html)
                else:
                    print(response.status)
                    print(response)
        except aiohttp.ClientConnectorError as e:
            print("Connection Error", str(e))


# Add a second arg with custom text?
def get_text_message_input(recipient):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "to": recipient,
            "type": "template",
            "template": {"name": "hello_world", "language": {"code": "en_US"}},
        }
    )
