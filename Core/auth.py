import os
import msal

from dotenv import load_dotenv


CACHE_FILE = "token_cache.bin"


def load_env():
    load_dotenv()


def get_token():

    load_env()

    dataverse_url = os.getenv("DATAVERSE_URL").rstrip("/")

    cache = msal.SerializableTokenCache()

    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            cache.deserialize(f.read())

    app = msal.PublicClientApplication(
        client_id="51f81489-12ee-4a9e-aaae-a2591f45987d",
        authority="https://login.microsoftonline.com/common",
        token_cache=cache
    )

    accounts = app.get_accounts()

    if accounts:

        result = app.acquire_token_silent(
            scopes=[f"{dataverse_url}/.default"],
            account=accounts[0]
        )

        if result and "access_token" in result:
            print("Token récupéré depuis le cache")
            return result["access_token"]
    print("Authentification interactive")

    result = app.acquire_token_interactive(
        scopes=[f"{dataverse_url}/.default"],
        prompt="select_account"
    )

    if "access_token" not in result:
        raise Exception(result)

    if cache.has_state_changed:
        with open(CACHE_FILE, "w") as f:
            f.write(cache.serialize())

    print("Nouveau token enregistré")

    return result["access_token"]