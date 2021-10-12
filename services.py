from fastapi import Body, Cookie, Form
from fastapi.responses import Response
from server import app

@app.post("/unify_phone_from_json")
def parse_phone_from_string(data: dict = Body(...)):
    input_string = data["phone"]
    buf = ''
    for char in input_string:
        if char.isnumeric():
            buf += char
    if (len(buf) == 11 and (buf[0] == '8' or buf[0] == '7') and buf[1] == '9'
            or len(buf) == 10 and buf[0] == '9'):
        output_string = (f"8 (9{buf[-9:-7]}) {buf[-7:-4]}-{buf[-4:-2]}-{buf[-2:len(buf)]}")
    else:
        output_string = buf
    return Response(output_string, media_type="text/html")


@app.post("/unify_phone_from_form")
def parse_phone_from_form(phone: str = Form(...)):
    buf = ''
    for char in phone:
        if char.isnumeric():
            buf += char
    if (len(buf) == 11 and (buf[0] == '8' or buf[0] == '7') and buf[1] == '9'
            or len(buf) == 10 and buf[0] == '9'):
        output_string = (f"8 (9{buf[-9:-7]}) {buf[-7:-4]}-{buf[-4:-2]}-{buf[-2:len(buf)]}")
    else:
        output_string = buf
    return Response(output_string, media_type="text/html")

@app.get("/unify_phone_from_query")
async def read_item(phone: str):
    buf = ''
    for char in phone:
        if char.isnumeric():
            buf += char
    if (len(buf) == 11 and (buf[0] == '8' or buf[0] == '7') and buf[1] == '9'
            or len(buf) == 10 and buf[0] == '9'):
        output_string = (f"8 (9{buf[-9:-7]}) {buf[-7:-4]}-{buf[-4:-2]}-{buf[-2:len(buf)]}")
    else:
        output_string = buf
    return Response(output_string, media_type="text/html")


@app.get("/unify_phone_from_cookies")
def parse_phone_from_cookies(phone = Cookie(...)):
    buf = ''
    for char in phone:
        if char.isnumeric():
            buf += char
    if (len(buf) == 11 and (buf[0] == '8' or buf[0] == '7') and buf[1] == '9'
            or len(buf) == 10 and buf[0] == '9'):
        output_string = (f"8 (9{buf[-9:-7]}) {buf[-7:-4]}-{buf[-4:-2]}-{buf[-2:len(buf)]}")
    else:
        output_string = buf
    return Response(output_string, media_type="text/html")