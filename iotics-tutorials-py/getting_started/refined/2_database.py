import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


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
from helpers.utilities import make_api_call,get_did_from_csv


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


#csv_file = "twin_key_name.csv"
#twin_key_name = input("Enter the twin_key_name:\n")
#twin_did = get_did_from_csv(twin_key_name, csv_file)
#print("TWIN DID:", twin_did)



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

    csv_file = "twin_key_name.csv"
    twin_key_name = input("Enter the twin_key_name:\n")
    twin_did = get_did_from_csv(twin_key_name, csv_file)
    if twin_did is None:
        print("Shall I create new twin")
    else:
        print("TWIN DID:", twin_did)
   

    twin_publisher_did: str = twin_did

    META_DATA = "http://data.iotics.com/public#hostMetadataAllowList"
    DATA = "http://data.iotics.com/public#hostAllowList"

    share_all = "http://data.iotics.com/public#all"
    share_none = "http://data.iotics.com/public#none"
    sharing_allowed = 'did:iotics:iotFmc6tRmH64DddY4dzPq827nywu6eSEAzM'
    sharing_allowed1 = 'did:iotics:didexample1234absd'
    sharing_allowed3 = 'did:iotics:didexample1234abs6'


    #twin_publisher_did = "did:iotics:iotTmYUYKbgLwbgBVVD1Q2AxDyJMu1as1sym"
    location_properties = create_location(lat=LONDON_LAT, lon=LONDON_LON)
    twin_properties = [
        # 'Label' represents a short human-readable name for the Twin
        create_property(key=LABEL, value=twin_key_name, language="en"),
        # 'Created By' represents the name of the User that creates the Twin
        create_property(key=CREATED_BY, value="msg"),
        #create_property(key=TYPE, value="ship"),

        #create_property(key = META_DATA,value = sharing_allowed1),
        #create_property(key = META_DATA,value = sharing_allowed),
        #create_property(key = DATA ,value = share_all),
        #create_property(key="https://www.w3.org/2001/XMLSchema#decimal",
                      #  value="100", datatype="decimal",)
        
       
       #property_literal_datatype = prop.literalValue.dataType
    ]

    #twin_publisher_did = "did:iotics:iotCh4C7WphnMHYULrzbepcfobPvu6d5F5tf"
    #print(iotics_api.describe_twin(twin_did = twin_publisher_did))
    #iotics_api.update_twin(twin_did = twin_publisher_did,
                          # props_added = [create_property(key = META_DATA,value = sharing_allowed),create_property(key = 'https://www.w3.org/2001/XMLSchema#decimal',value = '5')],
                           #props_deleted = [create_property(key = META_DATA,value = sharing_allowed1)])
                          # props_keys_deleted = [META_DATA])
    iotics_api.upsert_twin(twin_did = twin_publisher_did, location = location_properties, properties = twin_properties)


    


if __name__ == "__main__":
    main()
