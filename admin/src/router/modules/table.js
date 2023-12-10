/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const tableRouter = {
  path: '/',
  component: Layout,
  redirect: '/teacher',
  name: 'Management',
  meta: {
    title: 'Management',
    icon: 'table', roles: ['admin']
  },
  children: [
    {
      path: 'teacher',
      component: () => import('@/views/management/teacher'),
      name: 'teacher',
      meta: { title: 'teacher', roles: ['admin'] }
    },
    {
      path: 'student',
      component: () => import('@/views/management/student'),
      name: 'student',
      meta: { title: 'student', roles: ['admin'] }
    },
    {
      path: 'course',
      component: () => import('@/views/management/course'),
      name: 'course',
      meta: { title: 'course', roles: ['admin'] }
    }
  ]
}
export default tableRouter
