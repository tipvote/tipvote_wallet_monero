import requests
from requests.auth import HTTPDigestAuth
import json
from walletconfig import rpcpassword, rpcusername, url

from app import db
from app.models import \
    MoneroWalletWork, \
    MoneroWallet, \
    User

###
# This script is a faster and simpler version of monero_full_accounts
# Used 90% of the time
###
# standard json header
headers = {'content-type': 'application/json'}


def create_subaddress(user_id):
    """
    This functions creates an account in the wallet
    :param user_id:
    :return:
    """
    rpc_input = {
        "method": "create_address",
        "params": {
            "account_index": int(0),
            "label": str(user_id),

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

    return response.json()


def checkforwork():
    # query for work ..#2 = create a wallet
    work = MoneroWalletWork.query \
        .filter(MoneroWalletWork.type == 2) \
        .all()
    if work:
        for f in work:
            # get user wallet
            user_wallet = MoneroWallet.query. \
                filter(MoneroWallet.user_id == f.user_id) \
                .first()

            # get the user
            theuser = User.query.get(f.user_id)
            # create an account
            userinfo = create_subaddress(user_id=f.id)
            # get new address
            useraddress = userinfo["result"]["address"]

            # put address into database from new account
            user_wallet.address1 = useraddress
            # label work as done
            print("created address for user")
            print(theuser.user_name)
            print(useraddress)
            f.type = 0

            # add to db
            db.session.add(user_wallet)
            db.session.add(f)

        db.session.commit()
    else:
        print("no new accounts :(")


if __name__ == '__main__':
    checkforwork()

