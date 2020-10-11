import requests
from requests.auth import HTTPDigestAuth
import json
from walletconfig import rpcpassword, rpcusername, url

from app import db
from app.models import MoneroBlockHeight


###
# This script updates blocks so you know what to define confirmations as
##

def getblockheight():

    # standard json header
    headers = {'content-type': 'application/json'}

    rpc_input = {
        "method": "get_height",
    }

    # add standard rpc values
    rpc_input.update({"jsonrpc": "2.0", "id": "0"})

    # execute the rpc request
    response = requests.post(
        url,
        data=json.dumps(rpc_input),
        headers=headers,
        auth=HTTPDigestAuth(rpcusername, rpcpassword))
    print(response)
    response_json = response.json()
    print(response_json)
    return response_json


def updateblockheight():
    response_json = getblockheight()

    if response_json["result"]['height'] > 1:

        lastheight = response_json["result"]['height']

        lastblockheight = db.session.query(MoneroBlockHeight).get(1)
        lastblockheight.blockheight = int(lastheight)

        db.session.add(lastblockheight)

        db.session.commit()


if __name__ == '__main__':
    updateblockheight()
