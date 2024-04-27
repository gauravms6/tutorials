import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import sys
sys.path.append("/Users/gaurav/Desktop/wrapper/iotics-tutorials-py/getting_started")
from random import randint
from time import sleep

from helpers.constants import (
    CELSIUS_DEGREES,
    CREATED_BY,
    INDEX_URL,
    LABEL,
    LONDON_LAT,
    LONDON_LON,
    THERMOMETER,
    TYPE,

)
from helpers.identity_interface import IdentityInterface
from helpers.utilities import make_api_call
from iotics.lib.grpc.helpers import (
    create_feed_with_meta,
    create_location,
    create_property,
    create_value,
)
from iotics.lib.grpc.iotics_api import IoticsApi
from iotics.lib.identity.api.high_level_api import (
    HighLevelIdentityApi,
    RegisteredIdentity,
    get_rest_high_level_identity_api,
)

def main():
    df = pd.read_csv("/Users/gaurav/Desktop/wrapper/iotics-tutorials-py/getting_started/credentials.csv",)
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

    # A User and an Agent Identity need to be created with Authentication Delegation so you can:
    # 1. Create Twin Identities;
    # 2. Generate a Token to use the IOTICS API.
    # Be aware that, if Key Name and Seed don't change, multiple calls of the following function
    # will not create new Identities, it will retrieve the existing ones.
    user_identity: RegisteredIdentity
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


    identity_interface.refresh_token(
        user_identity=user_identity, agent_identity=agent_identity, token_duration=60
    )

    # We can now instantiate an instance of the 'IoticsApi' in order to use the IOTICS operations
    iotics_api = IoticsApi(auth=identity_interface)

    twin_did = "did:iotics:iotAzeYmevcMvSZoYiXUGqbRbJm1Z41TKCUe"
    feed_id = "Fuel"


    # Even the Feed needs to be semantically described. That's why its object includes
    # a list of Properties that follow the same principles as the Twin Properties.
    feed_properties = [create_property(key=LABEL, value="Fuel", language="en")]

    # Feed values represent the payload the Twin will share.
    # In particular it can be represented with:
    # - a 'label' representing the name of the data sample;
    # - an optional 'comment' representing a long description of the data sample;
    # - a 'dataType' representing the type of the data to be sent (integer, float, string, etc.);
    # - an optional 'unit' representing the URI of unity of measure of the data.
    value_label: str = "lat"
    feed_values = [create_value(label=value_label,comment="Fuel",data_type="decimal")]

    #iotics_api.create_feed(twin_did =twin_did,feed_id = feed_id )
    #iotics_api.update_feed(twin_did = twin_did, feed_id = feed_id,values_added = feed_values,props_added = feed_properties)
    #iotics_api.update_feed(twin_did = twin_did, feed_id = feed_id,values_added = feed_values,props_added = feed_properties)
    #iotics_api.delete_feed(twin_did=twin_did,feed_id='Temperature 121')
    #while True:
     #   iotics_api.share_feed_data(twin_did, 'Fuel', {'lat': 42,"readings":42})
    print(iotics_api.describe_feed(twin_did =twin_did,feed_id = feed_id))
    #print(iotics_api.list_all_feeds(twin_did =twin_did))

if __name__ == "__main__":
    main()
