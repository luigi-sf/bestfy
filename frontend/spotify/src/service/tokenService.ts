export const tokenService = {
  get: () => {
    const token = localStorage.getItem("token");

    if (!token || token === "undefined" || token === "null") {
      return null;
    }

    return token;
  },

  set: (token: string | null) => {
    if (!token) return; // bloqueia undefined/null

    localStorage.setItem("token", token);
  },

  remove: () => {
    localStorage.removeItem("token");
  },
};