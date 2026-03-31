export type User = {
  id: string;
  name: string;
  email: string;
  role?: 'LISTENER'|'ADMIN';
  sellerId?:string;
  createdAt: string;
  updatedAt?: string;
}




export type CreateUserDTO = {
    name: string;
    email: string;
    password: string;
    role?: 'LISTENER'|'ADMIN';
};


export type UpdateUserDTO = {
    name?: string;
    email?: string;
    password?: string;
};
