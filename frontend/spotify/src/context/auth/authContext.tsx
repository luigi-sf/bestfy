import { createContext } from 'react'
import type { AuthContextData } from '../../types/auth/authContext'

export const AuthContext = createContext<AuthContextData>(
  {} as AuthContextData
)
