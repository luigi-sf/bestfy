import type { User } from '../user'
import type { ReactNode } from 'react'

export interface LoginRequest {
  email: string
  password: string
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
  role: "LISTENER" | "ADMIN";
}

export type Credentials = {
  email: string
  password: string
}



export interface SignupDTO {
  name: string
  email: string
  password: string
}

export type AuthProviderProps = {
  children: ReactNode
}
export type PrivateRouteProps = {
  children: ReactNode
}