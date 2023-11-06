import unittest
import requests
import logging
import pydantic
from sqlalchemy import create_engine
from sqlalchemy.sql import text

ENTRYPOINT = 'http://policy-enforcement-service:5000/'
DATABASE_DSN = 'postgresql://home-automation:home-automation@postgresql:5432/home-automation'
ACCESS_DENIED_MESSAGE = {"message":"Content not found"}
ADMIN_GROUP_ID = 1
USER_GROUP_ID = 2

# setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-9s %(message)s"
)

class User(pydantic.BaseModel):
    id: str 
    email: str
    is_active: bool
    is_superuser: bool
    is_verified: bool
    first_name: str
    last_name: str
    age: int
    group_id: int

class TestCommonFunctionality(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_service_availability(self):
        response = requests.get(ENTRYPOINT)
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertDictEqual(data, ACCESS_DENIED_MESSAGE)

class BaseUserTestCase(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.test_user: User = None
        self.access_token: str = None

    def setUp(self, group_id: int, age: int) -> None:
        self._register_test_user(group_id, age)
        self._login()

    def tearDown(self) -> None:
        self._delete_test_user()

    def _register_test_user(self, group_id: int, age: int) -> User:
        payload = {
            "email": "test-user@example.com",
            "password": "password",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "first_name": "string",
            "last_name": "string",
            "age": age,
            "group_id": group_id
        }   
        try:
            response = requests.post(f'{ENTRYPOINT}auth/register', json=payload) 
            response.raise_for_status()
            self.test_user = User(**response.json())
        except requests.exceptions.HTTPError as exc:
            logger.error(exc)

    def _raise_if_invalid_user(self):
        if self.test_user is None:
            raise Exception('Cannot continue test without valid user!')

    def _delete_test_user(self):
        if self.test_user is None:
            return
        engine = create_engine(DATABASE_DSN)
        with engine.connect() as connection:
            connection.execute(text(f"""DELETE FROM "user" WHERE id = '{self.test_user.id}';"""))
            connection.commit()

    def _set_superuser(self, is_superuser: bool):
        if self.test_user is None:
            return
        self.test_user.is_superuser = is_superuser
        engine = create_engine(DATABASE_DSN)
        with engine.connect() as connection:
            connection.execute(text(f"""UPDATE "user" SET is_superuser = {self.test_user.is_superuser} WHERE id = '{self.test_user.id}';"""))
            connection.commit()

    def _login(self):
        self._raise_if_invalid_user()
        try:
            data = {
                'username': 'test-user@example.com',
                'password': 'password',
            }
            response = requests.post(
                f'{ENTRYPOINT}auth/jwt/login', data=data
            ) 
            response.raise_for_status()
            self.access_token = response.json()['access_token']
        except requests.exceptions.HTTPError as exc:
            logger.error(exc)

    @property
    def auth_headers(self):  
        return {
            'Authorization': f'Bearer {self.access_token}'
        }  
         
class TestAdminPolicies(BaseUserTestCase):
    def setUp(self) -> None:
        super().setUp(ADMIN_GROUP_ID, 30)
        self._set_superuser(True)
        self._login()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_get_groups_list(self):
        self._raise_if_invalid_user()
        response = requests.get(
            f'{ENTRYPOINT}groups', headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

class TestUserPolicies(BaseUserTestCase):
    def setUp(self) -> None:
        super().setUp(USER_GROUP_ID, 30)

    def tearDown(self) -> None:
        return super().tearDown()

    def test_get_groups_list(self):
        self._raise_if_invalid_user()
        response = requests.get(
            f'{ENTRYPOINT}groups', headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertDictEqual(data, ACCESS_DENIED_MESSAGE)

    def test_get_devices_list(self):
        self._raise_if_invalid_user()
        response = requests.get(
            f'{ENTRYPOINT}devices', headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

class TestAgePolicies(BaseUserTestCase):
    def setUp(self) -> None:
        super().setUp(USER_GROUP_ID, 75)

    def tearDown(self) -> None:
        return super().tearDown()

    def test_get_devices_list(self):
        self._raise_if_invalid_user()
        response = requests.get(
            f'{ENTRYPOINT}devices', headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertDictEqual(data, ACCESS_DENIED_MESSAGE)

if __name__ == '__main__':
    unittest.main()
