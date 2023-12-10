import router from './router'
import store from './store'
import { Message } from 'element-ui'
import NProgress from 'nprogress' // progress bar
import 'nprogress/nprogress.css' // progress bar style
import { getToken } from '@/utils/auth' // get token from cookie
import getPageTitle from '@/utils/get-page-title'

NProgress.configure({ showSpinner: false }) // NProgress Configuration

//白名单
const whiteList = ['/login'] // no redirect whitelist

router.beforeEach(async(to, from, next) => {
  // start progress bar
  NProgress.start()

  // set page title
  document.title = getPageTitle(to.meta.title)

  //获取token
  // determine whether the user has logged in
  const hasToken = getToken()

  if (hasToken) {
    //是否为登录
    if (to.path === '/login') {
      //去首页
      next({ path: '/' })
      NProgress.done()
    } else {
      //从vuex中获取权限
      const hasRoles = store.getters.roles && store.getters.roles.length > 0
      if (hasRoles) { //如果存在则放行
        next()
      } else {
        try {
          //roles 必须是一个数组
          //获取用户信息和权限信息，存到vuex中
          const { roles } = await store.dispatch('user/getInfo')

          //生产路由数据
          const accessRoutes = await store.dispatch('permission/generateRoutes', store.getters.roles)
          //const accessRoutes = []
          // dynamically add accessible routes
          router.addRoutes(accessRoutes)
          var tempRoutes = router.options.routes.slice(0,3).concat(accessRoutes); //将原路由侧边栏显示截取为初始三个（作者其实不支持这样）
          router.options.routes = tempRoutes; //将路由添加到侧边栏（作者其实不支持这样）
          // hack method to ensure that addRoutes is complete
          // set the replace: true, so the navigation will not leave a history record
          next({ ...to, replace: true })
        } catch (error) {
          // remove token and go to login page to re-login
          await store.dispatch('user/resetToken')
          Message.error(error || 'Has Error')
          //next(`/login?redirect=${to.path}`)
          next({ path: '/' })
          NProgress.done()
        }
      }
    }
  } else {
    /* has no token*/

    if (whiteList.indexOf(to.path) !== -1) {
      // in the free login whitelist, go directly
      next()
    } else {
      // other pages that do not have permission to access are redirected to the login page.
      next(`/login?redirect=${to.path}`)
      NProgress.done()
    }
  }
})

router.afterEach(() => {
  // finish progress bar
  NProgress.done()
})

