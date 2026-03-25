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
  // For projects service
  GET_USER_BY_EMAIL: (email) => `/users/email/${email}`,

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

  // GET - KPI CARDS
  GET_ALL_PRIVATE_TASKS_COUNTED: '/private-tasks/get-all-tasks-counted',
  GET_ALL_PRIVATE_COMPLETED_TASKS_COUNTED: '/private-tasks/get-all-tasks-completed-counted',
  GET_ALL_PRIAVTE_TASKS_IN_CURRENT_MONTH_COUNTED:
    '/private-tasks/get-all-tasks-current-month-counted',
  GET_ALL_PRIVATE_COMPLETED_TASKS_IN_CURRENT_MONTH_COUNTED:
    '/private-tasks/get-all-tasks-current-month-completed-counted',

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
  GET_KANBAN_MEMBER_BY_EMAIL: '/kanban/members/get-member-by-email',
  GET_KANBAN_MEMBERS_BY_ROLE: '/kanban/members/get-members-by-role',
  GET_ME_KANBAN_MEMBER: '/kanban/members/get-current-user',
  // POST
  ADD_KANBAN_MEMBER: 'kanban/members/add-member',
  // PUT
  UPDATE_KANBAN_MEMBER: '/kanban/members/update-member',
  // DELETE
  DELETE_KANBAN_MEMBER: '/kanban/members/delete-member',

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

  // ===== Workspace management =====

  // =====PROJECT:
  // GET
  GET_ALL_PROJECTS: '/workspace/projects/get-all-projects',
  GET_PROJECT_BY_TITLE: '/workspace/projects/get-project-by-title',
  // POST
  CREATE_PROJECT: '/workspace/projects/create-project',
  // PUT
  UPDATE_PROJECT: '/workspace/projects/update-project',
  // DELETE
  DELETE_PROJECT: '/workspace/projects/delete-project',

  // =====STAGES:
  // GET
  GET_ALL_PROJECT_STAGES: '/workspace/stages/get-all-stages',
  // POST
  CREATE_PROJECT_STAGE: '/workspace/stages/create-stage',
  CREATE_PROJECT_STAGE_RELATIVE: '/workspace/stages/insert-relative-stage',
  // PUT
  MOVE_PROJECT_STAGE: '/workspace/stages/move-stage',
  UPDATE_PROJECT_STAGE: '/workspace/stages/update-stage',
  // DELETE
  DELETE_PROJECT_STAGE: '/workspace/stages/delete-stage',

  // =====TASKS:
  // GET
  GET_ALL_PROJECT_TASKS: '/workspace/tasks/get-all-tasks',
  // POST
  CREATE_PROJECT_TASK: '/workspace/tasks/create-task',
  // PUT
  UPDATE_PROJECT_TASK: '/workspace/tasks/update-task',
  // DELETE
  DELETE_PROJECT_TASK: '/workspace/tasks/delete-task',

  // =====MEMBERS:
  // GET
  GET_PROJECT_ALL_MEMBERS: '/workspace/members/get-all-members',
  GET_PROJECT_MEMBER_BY_EMAIL: '/workspace/members/get-member-by-email',
  GET_PROJECT_MEMBERS_BY_ROLE: '/workspace/members/get-members-by-role',
  GET_ME_PROJECT_MEMBER: '/workspace/members/get-current-user',
  // POST
  ADD_PROJECT_MEMBER: '/workspace/members/add-member',
  // PUT
  UPDATE_PROJECT_MEMBER: '/workspace/members/update-member',
  // DELETE
  DELETE_PROJECT_MEMBER: '/workspace/members/delete-member',


  // ===== Selected project management =====

  // GET
  GET_SELECTED_PROJECT: '/workspace/selected-project/get-selected-project',
  GET_SELECTED_PROJECT_STAGES_COUNT: '/workspace/selected-project/get-stages-count',
  GET_PROJECT_DATE_RANGE: '/workspace/selected-project/get-stages-date-range',
  GET_PROJECT_TASKS_STATS: '/workspace/selected-project/get-project-tasks-stats',
  GET_PROJECTS_COUNT: '/workspace/projects/get-projects-count',
  // PUT
  SET_SELECTED_PROJECT: '/workspace/selected-project/set-selected-project',
  DELETE_SELECTED_PROJECT: '/workspace/selected-project/clear-selected-project',

}
