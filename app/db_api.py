"""
MongoDB database APIs.
"""
import copy
from typing import Dict, Any
import requests
import app.settings as settings


def create_session() -> requests.Session:
    """Create a session with the API header.

    Returns:
        requests.Session: Session with the API header.
    """
    session = requests.Session()
    session.headers.update(settings.HEADERS)
    return session

# let's create our own API function to insert one recipe


def insert_one(Gradebook: Dict[str, Any]) -> 'requests.Response':
    """Insert one recipe into the database.

    Args:
        recipe (Dict[str, Any]): Recipe to insert.

    Returns:
        requests.Response: Response from the API.
    """
    session = create_session()
    action = f'{settings.END_POINT}/insertOne'
    print(action)
    payload: Dict[str, Any] = copy.deepcopy(settings.PAYLOAD)
    payload['document'] = Gradebook
    response = session.post(action, json=payload)
    return response
