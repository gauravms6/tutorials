import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import sys
sys.path.append("/Users/gaurav/Desktop/wrapper/iotics-tutorials-py/getting_started")
from random import randint
from time import sleep

from helpers.constants import (
    INDEX_URL, 
)
from helpers.identity_interface import IdentityInterface
from helpers.utilities import make_api_call,save_twinKeyName_to_csv

from iotics.lib.grpc.iotics_api import IoticsApi
from iotics.lib.identity.api.high_level_api import (
    HighLevelIdentityApi,
    RegisteredIdentity,
    get_rest_high_level_identity_api,
)


def main():
    df = pd.read_csv("credentials.csv",)
    HOST_URL: str = "https://demo.iotics.space/"

    USER_KEY_NAME:str = df["USER_KEY_NAME"].values[0]
    USER_SEED:str = df["USER_SEED"].values[0]
    AGENT_KEY_NAME: str = df["AGENT_KEY_NAME"].values[0]
    AGENT_SEED: str = df["AGENT_SEED"].values[0]


    # Let's retrieve the gRPC and Resolver URLs automatically so we can instantiate an identity api variable
    iotics_index: dict = make_api_call(
        method="GET", endpoint=INDEX_URL.format(host_url=HOST_URL)
    )
    resolver_url: str = iotics_index.get("resolver")
    grpc_url: str = iotics_index.get("grpc")

    identity_api: HighLevelIdentityApi = get_rest_high_level_identity_api(
        resolver_url=resolver_url
    )

    identity_interface: IdentityInterface = IdentityInterface(
        grpc_endpoint=grpc_url, identity_api=identity_api
    )

    agent_identity: RegisteredIdentity
    (
        user_identity,
        agent_identity,
    ) = identity_api.create_user_and_agent_with_auth_delegation(
        user_seed=bytes.fromhex(USER_SEED),
        user_key_name=USER_KEY_NAME,
        agent_seed=bytes.fromhex(AGENT_SEED),
        agent_key_name=AGENT_KEY_NAME,
    )
    
    print(agent_identity.did)
    # Any IOTICS operation requires a token (JWT). The latter can be created using:
    # 1. A User DID;
    # 2. An Agent Identity;
    # 3. A duration (in seconds)
    # This token will only be valid for the duration expressed on point 3 above.
    # When the token expires you won't be able to use the API so you need to generate a new token.
    # Please remember that the longer the token's duration, the less secure your Twins are.
    # (The token may be stolen and a malicious user can use your Twins on your behalf).
    identity_interface.refresh_token(
        user_identity=user_identity, agent_identity=agent_identity, token_duration=60
    )

    # We can now instantiate an instance of the 'IoticsApi' in order to use the IOTICS operations
    iotics_api = IoticsApi(auth=identity_interface)

    # We now need to create a new Twin Identity which will be used for our Twin Publisher.
    # Only Agents can perform actions against a Twin.
    # This means, after creating the Twin Identity it has to "control-delegate" an Agent Identity
    # so the latter can control the Digital Twin.

    TWIN_KEY_NAME = input("Please enter unique twin name :\n")
    twin_publisher_identity: RegisteredIdentity = (
        identity_api.create_twin_with_control_delegation(
            # The Twin Key Name's concept is the same as Agent and User Key Name
            twin_key_name=TWIN_KEY_NAME,
            # It is a best-practice to re-use the "AGENT_SEED" as a Twin seed.
            twin_seed=bytes.fromhex(AGENT_SEED),
            agent_registered_identity=agent_identity,
        )
    )

   

    twin_publisher_did: str = twin_publisher_identity.did
    print(twin_publisher_did)
    data = {
        "USER":USER_KEY_NAME,
        "AGENT":AGENT_KEY_NAME,
        "TWIN_KEY_NAME":TWIN_KEY_NAME,
        "TWIN_DID":twin_publisher_did
    }
    csv_file = "twin_key_name.csv"
    save_twinKeyName_to_csv(data, csv_file)

    
    


if __name__ == "__main__":
    main()

