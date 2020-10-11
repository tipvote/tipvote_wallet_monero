import requests
from requests.auth import HTTPDigestAuth
import json
from walletconfig import rpcpassword, rpcusername, url

from app import db
from app.models import \
    MoneroWallet, \
    User, \
    MoneroUnconfirmed

# standard json header
headers = {'content-type': 'application/json'}


###
# This script used once a day
# It will go through each account.
# check they got a wallet
# then check they got an address
# make sure all is ok
###


def createnewdbentry(userid):
    monero_newunconfirmed = MoneroUnconfirmed(
        user_id=userid,
        unconfirmed1=0,
        unconfirmed2=0,
        unconfirmed3=0,
        unconfirmed4=0,
        unconfirmed5=0,
        txid1='',
        txid2='',
        txid3='',
        txid4='',
        txid5='',
    )

    # creates monero wallet  in db
    monero_walletcreate = MoneroWallet(user_id=userid,
                                       currentbalance=0,
                                       unconfirmed=0,
                                       address1='',
                                       address1status=1,
                                       locked=0,
                                       transactioncount=0,
                                       )

    db.session.add(monero_newunconfirmed)
    db.session.add(monero_walletcreate)

    db.session.commit()


def create_subaddress(user_id):

    rpc_input = {
        "method": "create_address",
        "params": {"label": str(user_id),
                   "account_index": int(2),
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


def balance_validate_address(theaddress):

    rpc_input = {
        "method": "get_address_index",
        "params": {"address": str(theaddress)}
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
    # get all users
    the_users = db.session.query(User).order_by(User.id.asc()).all()
    # loop through them
    print("Starting program ..")
    for f in the_users:

        print("***********Start*********")

        # Get users wallet in database
        user_wallet = db.session.query(MoneroWallet) \
            .filter(MoneroWallet.user_id == f.id) \
            .first()

        if user_wallet is None:
            print("creating new wallet for user: ", f.user_name)
            # create new thing in database
            createnewdbentry(userid=f.id)

            # re query wallet
            user_wallet = db.session.query(MoneroWallet) \
                .filter(MoneroWallet.user_id == f.id) \
                .first()

            print("Creating address for :", f.user_name)
            # create an account
            userinfo = create_subaddress(user_id=f.id)
            # get response string
            useraddress = userinfo["result"]["address"]
            # set variable
            user_wallet.address1 = useraddress
            db.session.add(user_wallet)
            print("address created", user_wallet.address1)

        else:
            print("user wallet exists: ", f.user_name)
            # see if address exists
            if len(user_wallet.address1) > 10:
                theaddresresponse = balance_validate_address(user_wallet.address1)
                # if its got major then it exists just move on
                if theaddresresponse["result"]['index']["major"] == 2:
                    print("account exists, user has address and wallet")
                    print("account major index:", theaddresresponse["result"]['index']["major"])
                    print("account minor index:", theaddresresponse["result"]['index']["minor"])
                    print(user_wallet.address1)
                    pass
                else:
                    print("Adding new address for user")
                    print(f.user_name)
                    # create an subaddress
                    userinfo = create_subaddress(user_id=f.id)
                    # get the response string
                    useraddress = userinfo["result"]["address"]
                    # put address into database from new account
                    user_wallet.address1 = useraddress
                    print("User Address", user_wallet.address1)
                    db.session.add(user_wallet)

                    print(f.user_name)
                    print(user_wallet.address1)
                    print("*")

        print("***********End*********")

    # final commit
    print("DONE!")
    db.session.commit()


if __name__ == '__main__':
    checkforwork()
