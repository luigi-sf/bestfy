// src/services/authService.ts
import api from "./api";
import type { LoginRequest, SignupDTO,LoginResponse } from "../types/auth/auth";

export const authService = {
 async signup(data: SignupDTO) {
  const { data: response } = await api.post("/register", data);
  return response; // UserResponse
},

async login(data: LoginRequest): Promise<LoginResponse> {
  const { data: response } = await api.post('/login', data);

  return response;
},

  async me() {
    const { data } = await api.get("/me");
    return data;
  },

  async logout(): Promise<void> {
    await api.post("/logout");
  },
};