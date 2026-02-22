import httpx

from app.config import get_settings

settings = get_settings()


class KeycloakService:
    def __init__(self):
        self.base_url = settings.KEYCLOAK_URL
        self.realm = settings.KEYCLOAK_REALM
        self.client_id = settings.KEYCLOAK_CLIENT_ID
        self.client_secret = settings.KEYCLOAK_CLIENT_SECRET
        self._admin_token: str | None = None

    async def _get_admin_token(self) -> str:
        url = f"{self.base_url}/realms/{self.realm}/protocol/openid-connect/token"
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                url,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            self._admin_token = data["access_token"]
            return self._admin_token

    async def _get_headers(self) -> dict:
        token = await self._get_admin_token()
        return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    async def get_user(self, user_id: str) -> dict | None:
        headers = await self._get_headers()
        url = f"{self.base_url}/admin/realms/{self.realm}/users/{user_id}"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=headers)
            if resp.status_code == 404:
                return None
            resp.raise_for_status()
            return resp.json()

    async def create_user(
        self, email: str, first_name: str, last_name: str, temp_password: str
    ) -> str:
        headers = await self._get_headers()
        url = f"{self.base_url}/admin/realms/{self.realm}/users"
        payload = {
            "username": email,
            "email": email,
            "firstName": first_name,
            "lastName": last_name,
            "enabled": True,
            "emailVerified": True,
            "credentials": [
                {"type": "password", "value": temp_password, "temporary": True}
            ],
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            location = resp.headers.get("Location", "")
            return location.split("/")[-1]

    async def assign_realm_role(self, user_id: str, role_name: str):
        headers = await self._get_headers()
        # Get available roles
        roles_url = f"{self.base_url}/admin/realms/{self.realm}/roles/{role_name}"
        async with httpx.AsyncClient() as client:
            resp = await client.get(roles_url, headers=headers)
            resp.raise_for_status()
            role = resp.json()

            # Assign role
            assign_url = (
                f"{self.base_url}/admin/realms/{self.realm}/users/{user_id}/role-mappings/realm"
            )
            resp = await client.post(assign_url, json=[role], headers=headers)
            resp.raise_for_status()

    async def exchange_token(self, username: str, password: str) -> dict:
        url = f"{self.base_url}/realms/{self.realm}/protocol/openid-connect/token"
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                url,
                data={
                    "grant_type": "password",
                    "client_id": "quicktrust-web",
                    "username": username,
                    "password": password,
                },
            )
            resp.raise_for_status()
            return resp.json()


keycloak_service = KeycloakService()
