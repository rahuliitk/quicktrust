"use client";

import React, {
  createContext,
  useContext,
  useEffect,
  useState,
  useCallback,
} from "react";
import { getKeycloak, initKeycloak, login, logout } from "@/lib/auth";
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
    // Race Keycloak init against a timeout so we never hang on "Loading..."
    const timeout = new Promise<boolean>((resolve) =>
      setTimeout(() => resolve(false), 10000)
    );

    Promise.race([initKeycloak(), timeout]).then((auth) => {
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

      // User is not logged in — stay unauthenticated
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
