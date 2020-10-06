import requests
from requests.auth import HTTPDigestAuth
import json
from walletconfig import rpcpassword, rpcusername, url

####
# This scrit is used for running rpc commands to get info.
# not used in production
##
# standard json header
headers = {'content-type': 'application/json'}


def getbalance(account_index):
    rpc_input = {
        "method": "get_balance",
        "params": {"account_index ": int(account_index)}
    }

    # add standard rpc values
    rpc_input.update({"jsonrpc": "2.0", "id": "0"})

    # execute the rpc request
    response = requests.post(
        url,
        data=json.dumps(rpc_input),
        headers=headers,
        auth=HTTPDigestAuth(rpcusername, rpcpassword))
    print("BALANCE")
    print(json.dumps(response.json(), indent=4))
    return response.json()


def gettheaccounts():
    rpc_input = {
        "method": "get_accounts",
    }

    # add standard rpc values
    rpc_input.update({"jsonrpc": "2.0", "id": "0"})

    # execute the rpc request
    response = requests.post(
        url,
        data=json.dumps(rpc_input),
        headers=headers,
        auth=HTTPDigestAuth(rpcusername, rpcpassword))

    print(json.dumps(response.json(), indent=4))


def getaddresses():
    rpc_input = {
        "method": "get_address",
        "params": {"account_index": int(2),
                   "address_index": [1,150, 151]
                   }
    }

    # add standard rpc values
    rpc_input.update({"jsonrpc": "2.0", "id": "0"})

    # execute the rpc request
    response = requests.post(
        url,
        data=json.dumps(rpc_input),
        headers=headers,
        auth=HTTPDigestAuth(rpcusername, rpcpassword))

    print(json.dumps(response.json(), indent=4))


if __name__ == '__main__':
    #getaddresses()
    getbalance(2)
    gettheaccounts()