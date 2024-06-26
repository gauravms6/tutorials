"""A new Identity, be it a User, an Agent or a Twin can be created with:
1.  A Key Name: a string of characters that uniquely identifies the entity;
2.  A Seed: a random string of characters generated via the API;
3.  A Name (optional): a human-friendly string of characters that represents the entity.
The creation (or retrieval) of a User and an Agent Identity will most likely be the entry point of any
IOTICS application.
While the User Identity represents the Identity of yourself,
the Agent Identity represents the Identity of the Software application that will manage your Twins.
This means, you will create (and re-use) only 1 User Identity and a different Agent Identity per application.
This script is intended to show what the setup of a User and an Agent Identity will be like.
"""

from iotics.lib.identity.api.high_level_api import (
    get_rest_high_level_identity_api,
    HighLevelIdentityApi,
    RegisteredIdentity,
)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


RESOLVER_URL: str = "https://did.stg.iotics.com"  # You can find it at <space_url>/index.json --> "resolver"
USER_KEY_NAME: str = "msg"
USER_SEED: str = "b8b8df11738e53b503f4c152eb996aed49aac1be207d07e5634331dcd8fea641"  # A random string of hex characters generated via the API (you can use "generate_new_seed.py")
AGENT_KEY_NAME: str = "msg_agent"  # A string of characters that uniquely identifies the Agent (i.e. your application/script name)
AGENT_SEED: str = "fd7749e73e5fa8d8408e3b3681fc03f7279e99063866ff593a14cd963c8eeabe"  # A random string of hex characters generated via the API (you can use "generate_new_seed.py")


def main():
    identity_api: HighLevelIdentityApi = get_rest_high_level_identity_api(
        resolver_url=RESOLVER_URL
    )

    user_identity: RegisteredIdentity
    agent_identity: RegisteredIdentity
    (
        user_identity,  # It won't be used in this script
        agent_identity,  # It won't be used in this script
    ) = identity_api.create_user_and_agent_with_auth_delegation(
        # The user seed has to be converted back to a "bytes" object.
        # We can use the built-in function "bytes.fromhex()"
        user_seed=bytes.fromhex(USER_SEED),
        user_key_name=USER_KEY_NAME,
        # The agent seed has to be converted back to a "bytes" object
        agent_seed=bytes.fromhex(AGENT_SEED),
        agent_key_name=AGENT_KEY_NAME,
    )

    # Make sure you store the following credentials in a safe place
    # as they will be used any time you want to use the API.
    # If you lose them you will not be able to interact with your twins anymore.
    # Now that User and Agents are created with authentication delegation, you can now copy-paste:
    # - the User credentials into the "constants.py" file within the "helpers" folder;
    # - the Agent credentials into each script you want to run.
    print("User and Agent created with Authentication Delegation")
    print("Please store the following credentials in a safe place !!")
    print("---")
    print("USER_KEY_NAME:", USER_KEY_NAME)
    print("USER_SEED:", USER_SEED)
    print("---")
    print("AGENT_KEY_NAME:", AGENT_KEY_NAME)
    print("AGENT_SEED:", AGENT_SEED)

    data = {
        "USER_KEY_NAME": USER_KEY_NAME,
        "USER_SEED": USER_SEED,
        "AGENT_KEY_NAME": AGENT_KEY_NAME,
        "AGENT_SEED": AGENT_SEED
    }
    # Convert dictionary to DataFrame
    df = pd.DataFrame.from_dict(data, orient='index', columns=['Value'])

    # Transpose the DataFrame
    df = df.T

    # Define the file name
    csv_file = "credentials.csv"

    # Save DataFrame to CSV
    df.to_csv(csv_file, index=False)

    print("Data saved to", csv_file)


if __name__ == "__main__":
    main()
