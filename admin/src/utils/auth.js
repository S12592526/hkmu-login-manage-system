import Cookies from 'js-cookie'

const TokenKey = 'Admin-Token'

export function getToken() {
  return Cookies.get(TokenKey)
}

export function getUserType() {
  return Cookies.get("UserType")
}

export function getUserId() {
  return Cookies.get("UserId")
}
 
export function setToken(token) {
  return Cookies.set(TokenKey, token)
}

export function setUserType(userType) {
  return Cookies.set("UserType", userType)
}

export function setUserId(UserId) {
  return Cookies.set("UserId", UserId)
}

export function removeToken() {
  return Cookies.remove(TokenKey)
}

export function removeUserType() {
  return Cookies.remove("UserType")
}

export function removeUserId() {
  return Cookies.remove("UserId")
}
