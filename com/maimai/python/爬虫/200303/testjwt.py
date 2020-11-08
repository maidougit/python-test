#coding:utf-8
from jose import jwt
import datetime


def generate_jwt():
    # read the private_key
    with open("private.txt", 'r') as f:
        private_key = f.read()
    #Generate the JWT
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #expire_time = current_time + datetime.timedelta(days=1)
    expire_time = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

    payload = {
        "accountId": 1234416518389448706,
        "identity":"consumer",
        "expire_time":expire_time,
        "current_time":current_time


    }
    #header
    header = {
        "type":"JWT"

    }
    #encode
    encoded = jwt.encode(claims=payload,key=private_key,algorithm='RS256',headers=header)
    return encoded

if __name__ == '__main__':
    token = generate_jwt()
    print(token)