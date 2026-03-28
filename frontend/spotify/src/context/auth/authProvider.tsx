// src/contexts/auth/authProvider.tsx
import { useState } from "react";
import type { ReactNode } from "react";
import { AuthContext } from "./authContext";
import type { User } from "../../types/user";
import type { Credentials, SignupDTO } from "../../types/auth/auth";
import { authService } from "../../service/authService";
import { tokenService } from "../../service/tokenService";

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(() => {
    return tokenService.get(); // busca token no local storage
  });

  const [user, setUser] = useState<User | null>(() => {
    const storedUser = localStorage.getItem("user"); //pega user do storage e tranfotma em json

    if (!storedUser || storedUser === "undefined") return null;

    try {
      return JSON.parse(storedUser);
    } catch {
      localStorage.removeItem("user");
      return null;
    }
  });

  const [loading, setLoading] = useState(false);

  const isAuthenticated = !!token;

  async function login(credentials: Credentials): Promise<User | null> {
    setLoading(true);

    try {
      const response = await authService.login(credentials);

      const access_token = response.access_token;

      tokenService.set(access_token);
      setToken(access_token);

      // pega usuário
      const user = await authService.me();

      setUser(user);
      localStorage.setItem("user", JSON.stringify(user));

      return user;
    } catch (err) {
      console.error("❌ Erro no login:", err);
      return null;
    } finally {
      setLoading(false);
    }
  }

  async function signup(data: SignupDTO): Promise<boolean> {
    setLoading(true);

    try {
      await authService.signup(data);

      // opcional: já loga depois do cadastro
      const loginResponse = await authService.login({
        email: data.email,
        password: data.password,
      });

      const token = loginResponse.access_token;

      tokenService.set(token);
      setToken(token);

      const user = await authService.me();
      setUser(user);
      localStorage.setItem("user", JSON.stringify(user));

      return true;
    } catch (err) {
      console.error("❌ Erro no signup:", err);
      return false;
    } finally {
      setLoading(false);
    }
  }

  function logout() {
    setUser(null);
    setToken(null);
    tokenService.remove();
    localStorage.removeItem("user");
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated,
        loading,
        login,
        signup,
        logout,
        setUser,
        setToken,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}