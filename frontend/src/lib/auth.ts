import Keycloak from "keycloak-js";

const keycloakConfig = {
  url: process.env.NEXT_PUBLIC_KEYCLOAK_URL || "http://localhost:8080",
  realm: process.env.NEXT_PUBLIC_KEYCLOAK_REALM || "quicktrust",
  clientId: process.env.NEXT_PUBLIC_KEYCLOAK_CLIENT_ID || "quicktrust-web",
};

let keycloakInstance: Keycloak | null = null;

export function getKeycloak(): Keycloak {
  if (!keycloakInstance) {
    keycloakInstance = new Keycloak(keycloakConfig);
  }
  return keycloakInstance;
}

export async function initKeycloak(): Promise<boolean> {
  const kc = getKeycloak();
  try {
    const authenticated = await kc.init({
      onLoad: "check-sso",
      pkceMethod: "S256",
      silentCheckSsoRedirectUri:
        typeof window !== "undefined"
          ? `${window.location.origin}/silent-check-sso.html`
          : undefined,
    });
    return authenticated;
  } catch (error) {
    console.error("Keycloak init failed:", error);
    return false;
  }
}

export function login() {
  const kc = getKeycloak();
  kc.login({ redirectUri: window.location.origin + "/dashboard" });
}

export function logout() {
  const kc = getKeycloak();
  kc.logout({ redirectUri: window.location.origin });
}

export function getToken(): string | undefined {
  return getKeycloak().token;
}

export async function refreshToken(): Promise<boolean> {
  const kc = getKeycloak();
  try {
    const refreshed = await kc.updateToken(30);
    return refreshed;
  } catch {
    return false;
  }
}
