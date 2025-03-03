import requests


URL_TOKEN = 'http://127.0.0.1:8000/api/token/'
URL_TOKEN_REFRESH = 'http://127.0.0.1:8000/api/token/refresh/'

def get_access_token(username, password):
    """
        Gets an access and refresh token by sending the provided username and password to the endpoint.

        This function sends a POST request to the token URL with the provided user data. If the user data is
        valid, it returns a JSON response containing the access and refresh tokens. If the request fails, it returns an error message.

        Args:
            username (str): The username of the user requesting the token.
            password (str): The password of the user requesting the token.

        Returns:
            dict: A dictionary containing the access and refresh tokens if the request is successful.
                  Or an error message if the request fails.
        """
    data = {
        'username': username,
        'password': password
            }
    response = requests.post(url=URL_TOKEN, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Request failed with status {response.status_code}"}


def get_access_token_refreshed(refresh_token):
    """
    Gets a new access token using a valid refresh token.

    This function sends a POST request to the token refresh URL with the provided refresh token. If the refresh token is valid,
    it returns a new access token. If the request fails, it returns an error message.

    Args:
        refresh_token (str): The refresh token used to request a new access token.

    Returns:
        dict: A dictionary containing the new access token if the request is successful,
              or an error message if the request fails.
    """
    data = {
        'refresh': refresh_token,
            }
    response = requests.post(url=URL_TOKEN_REFRESH, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Request failed with status {response.status_code}"}


# Probably not needed. Default in Django.
