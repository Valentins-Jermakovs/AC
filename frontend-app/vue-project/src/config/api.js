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

  // ===== Tasks management =====

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

  // ===== Kanban management =====

  // =====BOARDS:
  // GET
  GET_ALL_BOARDS: '/kanban/boards/get-all-boards',
  GET_BOARDS_BY_TITLE: '/kanban/boards/get-board-by-title',
  // POST
  CREATE_BOARD: '/kanban/boards/create-board',
  // PUT
  UPDATE_BOARD: '/kanban/boards/update-board',
  // DELETE
  DELETE_BOARD: '/kanban/boards/delete-board',

  // =====MEMBERS:
  // GET
  GET_KANBAN_MEMBERS: '/kanban/members/get-all-members',
  // POST
  ADD_KANBAN_MEMBER: 'kanban/members/add-member',
  // PUT
  UPDATE_KANBAN_MEMBER: '/kanban/members/update-member',
  // DELETE
  REMOVE_KANBAN_MEMBER: '/kanban/members/delete-member',

  // =====STAGES:
  // GET
  GET_KANBAN_STAGES: '/kanban/stages/get-all-stages',
  // POST
  CREATE_KANBAN_STAGE: '/kanban/stages/create-stage',
  CREATE_KANBAN_STAGE_RELATIVE: '/kanban/stages/create-relative-stage',
  // PUT
  MOVE_KANBAN_STAGE: '/kanban/stages/move-stage',
  UPDATE_KANBAN_STAGE: '/kanban/stages/update-stage',
  // DELETE
  DELETE_KANBAN_STAGE: '/kanban/stages/delete-stage',

  // =====TASKS:
  // GET
  GET_KANBAN_TASKS: '/kanban/tasks/get-all-tasks',
  // POST
  CREATE_KANBAN_TASK: '/kanban/tasks/create-task',
  // PUT
  UPDATE_KANBAN_TASK: '/kanban/tasks/update-task',
  MOVE_KANBAN_TASK_IN_STAGE: '/kanban/tasks/move-task-in-stage',
  MOVE_KANBAN_TASK_BETWEEN_STAGES: '/kanban/tasks/move-task-between-stages',
  // DELETE
  DELETE_KANBAN_TASK: '/kanban/tasks/delete-task',
}
