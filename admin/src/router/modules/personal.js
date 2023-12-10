/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const personalRouter = {
  path: '/',
  component: Layout,
  redirect: '/info',
  name: 'Personal',
  meta: {
    title: 'Personal',
    icon: 'user',
    roles: ['student']
  },
  children: [
    {
      path: 'info',
      component: () => import('@/views/personal/info'),
      name: 'info',
      meta: { title: 'info' }
    },
    {
      path: 'achievement',
      component: () => import('@/views/achievement/list'),
      name: 'achievement',
      meta: { title: 'achievement' }
    },
    {
      path: 'editpwd',
      component: () => import('@/views/personal/editpwd'),
      name: 'Change password',
      meta: { title: 'Change password' }
    }
  ]
}
export default personalRouter
