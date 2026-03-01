"use client";

import React, {
  createContext,
  useContext,
  useEffect,
  useState,
  useCallback,
} from "react";
import { getKeycloak, initKeycloak, login, logout, getToken } from "@/lib/auth";
import api from "@/lib/api";

interface AuthContextType {
  authenticated: boolean;
  loading: boolean;
  token: string | null;
  userInfo: {
    name: string;
    email: string;
    roles: string[];
    org_id: string | null;
  } | null;
  login: () => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType>({
  authenticated: false,
  loading: true,
  token: null,
  userInfo: null,
  login: () => {},
  logout: () => {},
});

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [authenticated, setAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState<string | null>(null);
  const [userInfo, setUserInfo] = useState<AuthContextType["userInfo"]>(null);

  useEffect(() => {
    initKeycloak().then((auth) => {
      setAuthenticated(auth);
      if (auth) {
        const kc = getKeycloak();
        const t = kc.token || null;
        setToken(t);
        api.setToken(t);
        setUserInfo({
          name: kc.tokenParsed?.name || kc.tokenParsed?.preferred_username || "",
          email: kc.tokenParsed?.email || "",
          roles: kc.tokenParsed?.realm_roles || [],
          org_id: kc.tokenParsed?.org_id || null,
        });

        // Token refresh interval
        const interval = setInterval(async () => {
          try {
            await kc.updateToken(30);
            const newToken = kc.token || null;
            setToken(newToken);
            api.setToken(newToken);
          } catch {
            setAuthenticated(false);
          }
        }, 60000);

        return () => clearInterval(interval);
      }

      // Dev mode: Keycloak not available, proceed without auth
      // Backend dev mode accepts requests without a Bearer token
      console.info("Keycloak not available — running in dev mode (no auth)");
      setUserInfo({
        name: "Dev Admin",
        email: "admin@quicktrust.dev",
        roles: ["super_admin"],
        org_id: "00000000-0000-0000-0000-000000000000",
      });
      setAuthenticated(true);
      setLoading(false);
    });
  }, []);

  useEffect(() => {
    if (authenticated) setLoading(false);
  }, [authenticated]);

  return (
    <AuthContext.Provider
      value={{ authenticated, loading, token, userInfo, login, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
