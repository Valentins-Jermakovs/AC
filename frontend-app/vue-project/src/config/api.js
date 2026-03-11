export const API_ENDPOINTS = {
  // ===== Authentication =====

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
  GET_ME: '/users/me',
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

  // ===== Projects management =====

  // GET
  GET_ALL_PRIVATE_TASKS: '/private-tasks/get-all-tasks',
  GET_TASKS_BY_TITLE: '/private-tasks/get-tasks-by-title',
  GET_TASKS_BY_DESCRIPTION: '/private-tasks/get-tasks-by-description',
  GET_TASKS_BY_DUE_DATE: '/private-tasks/get-tasks-by-duedate',
  GET_TASKS_BY_MONTH: '/private-tasks/get-tasks-by-month',

  // POST
  CREATE_PRIVATE_TASK: '/private-tasks/create-task',
  // PUT
  UPDATE_PRIVATE_TASK: '/private-tasks/update-task',
  // DELETE
  DELETE_PRIVATE_TASK: '/private-tasks/delete-task',
}
