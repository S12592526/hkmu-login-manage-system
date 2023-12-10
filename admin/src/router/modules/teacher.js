/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const teacherRouter = {
  path: '/',
  component: Layout,
  redirect: '/achievement',
  name: 'Teacher',
  meta: {
    title: 'achievement',
    icon: 'table', roles: ['teacher']
  },
  children: [
    {
      path: 'achievement',
      component: () => import('@/views/management/achievement'),
      name: 'achievement',
      meta: { title: 'achievement', roles: ['teacher'] }
    }
  ]
}
export default teacherRouter
