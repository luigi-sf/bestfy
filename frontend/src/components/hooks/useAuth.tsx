import { useContext } from 'react'
import { AuthContext } from '../../context/auth/authContext'

export function useAuth() {
  return useContext(AuthContext)
}