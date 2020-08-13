import pytest
from src import migrate
from src import settings

@pytest.mark.parametrize("client_id, client_secret, user_agent, username, password",[
    (None, None, None, None, None),
    ("", None, None, None, None),
    ("", "", None, None, None),
    ("", "", "", None, None),
    ("", "", "", "", None),
    ("", "", "", "", "")
])
def test_reddit_instance_is_none(client_id, client_secret, user_agent, username, password):
    """
    Returns true if the reddit instance is null
    """
    instance = migrate.get_reddit_instance
    (
        client_id,
        client_secret,
        user_agent,
        username,
        password
    )

    assert instance is None

def test_reddit_instance_is_not_none():
    """
    Returns true if the reddit instance is created successfully
    """
    instance = migrate.get_reddit_instance
    (
        settings.REDDIT_CLIENT_ID, 
        settings.REDDIT_CLIENT_SECRET, 
        settings.REDDIT_USER_AGENT, 
        settings.REDDIT_USERNAME, 
        settings.REDDIT_PASSWORD
    )

    assert instance is not None
