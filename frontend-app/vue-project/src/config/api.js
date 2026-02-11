export const API_ENDPOINTS = {
  // Auth
  GOOGLE_LOGIN: '/auth/google/login',
  LOGIN: '/auth/login',
  REGISTER: '/auth/register',
  LOGOUT: '/auth/logout',

  // Token
  TOKEN_CHECK: '/token/check',
  TOKEN_REFRESH: '/token/refresh',

  // Users
  GET_USERS: '/users/',
  GET_USER_BY_ID: (id) => `/users/${id}`,
  GET_USER_BY_USERNAME_OR_EMAIL: (value) => `/users/search/${value}`,
  GET_USER_BY_ROLE: (role) => `/users/role/${role}`,

  // Modifications
  CHANGE_USERNAME: '/modifications/username/',
  CHANGE_EMAIL: '/modifications/email/',
  CHANGE_PASSWORD: '/modifications/password/',

  // Activity
  CHANGE_USER_ACTIVITY: '/activity/',

  // Roles
  ADD_ROLES_TO_USER: '/roles/add',
  REMOVE_ROLES_FROM_USER: '/roles/remove',
}
