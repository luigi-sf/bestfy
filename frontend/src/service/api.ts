import axios from 'axios'
import type{AxiosInstance,
  InternalAxiosRequestConfig
} from 'axios'
import { tokenService } from './tokenService'
export const API_URL = "http://127.0.0.1:8000"

const api: AxiosInstance = axios.create({
  baseURL: API_URL
})

api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = tokenService.get()

    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

export default api
