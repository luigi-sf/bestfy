import type { SignupDTO,Credentials } from "./auth"
import type { User } from "../user"

export type AuthContextData = {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  loading: boolean;
  login: (credentials: Credentials) => Promise<User | null>;
  signup: (data: SignupDTO) => Promise<boolean>;
  logout: () => void;
  setUser: React.Dispatch<React.SetStateAction<User | null>>;
  setToken: (token: string | null) => void;
  
};

