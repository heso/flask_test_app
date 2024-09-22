import json
import os

import pytest

from main import DATABASE_FILE, app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with open(DATABASE_FILE, "w") as f:
        json.dump([], f)

    with app.test_client() as client:
        yield client

    if os.path.exists(DATABASE_FILE):
        os.remove(DATABASE_FILE)
