import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/login',
    method: 'post',
    data
  })
}

export function getInfo(userType) {
  return request({
    url: '/userInfo',
    method: 'post',
    data: { userType }
  })
}

export function logout() {
  return request({
    url: '/logout',
    method: 'post'
  })
}

export function getCaptcha(uuid) {
  return request({
    url: `/captcha/${uuid}/`,
    method: 'get'
  })
}

export function getStudentList(query) {
  return request({
    url: '/studentList',
    method: 'get',
    params: query
  })
}


export function getStudentInfo(query) {
  return request({
    url: '/studentInfo',
    method: 'get',
    params: query
  })
}


export function getStudentScoreList(query) {
  return request({
    url: '/studentScoreList',
    method: 'get',
    params: query
  })
}

export function getTeacherList(query) {
  return request({
    url: '/teacherList',
    method: 'get',
    params: query
  })
}

export function getCourseList(query) {
  return request({
    url: '/courseList',
    method: 'get',
    params: query
  })
}

export function registerStudent(data) {
  return request({
    url: '/registerStudent',
    method: 'post',
    data
  })
}

export function createTeacherUser(data) {
  return request({
    url: '/teacher',
    method: 'post',
    data
  })
}

export function updateTeacherUser(data) {
  return request({
    url: '/teacher',
    method: 'put',
    data
  })
}

export function deleteTeacherUser(data) {
  return request({
    url: '/teacher',
    method: 'delete',
    data
  })
}

export function setSecurityIssues(data) {
  return request({
    url: '/setSecurityIssues',
    method: 'put',
    data
  })
}

export function updateStudentUser(data) {
  return request({
    url: '/student',
    method: 'put',
    data
  })
}

export function studentEditPwd(data) {
  return request({
    url: '/studentEditPwd',
    method: 'put',
    data
  })
}

export function deleteStudentUser(data) {
  return request({
    url: '/student',
    method: 'delete',
    data
  })
}

export function createStudentScore(data) {
  return request({
    url: '/studentScore',
    method: 'post',
    data
  })
}

export function updateStudentScore(data) {
  return request({
    url: '/studentScore',
    method: 'put',
    data
  })
}

export function deleteStudentScore(data) {
  return request({
    url: '/studentScore',
    method: 'delete',
    data
  })
}

export function createCourse(data) {
  return request({
    url: '/course',
    method: 'post',
    data
  })
}

export function updateCourse(data) {
  return request({
    url: '/course',
    method: 'put',
    data
  })
}

export function deleteCourse(data) {
  return request({
    url: '/course',
    method: 'delete',
    data
  })
}