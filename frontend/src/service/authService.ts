import api from "./api";
import type { LoginRequest, SignupDTO,LoginResponse } from "../types/auth/auth";

// SIGNUP
export const authService = {
 async signup(data: SignupDTO) {
  const { data: response } = await api.post("/register", data);
  return response;
},

// LOGIN
async login(data: LoginRequest): Promise<LoginResponse> {
  const { data: response } = await api.post('/login', data);

  return response;
},

// ME
  async me() {
    const { data } = await api.get("/me");
    return data;
  },


// LOGOUT
  async logout(): Promise<void> {
    await api.post("/logout");
  },
};