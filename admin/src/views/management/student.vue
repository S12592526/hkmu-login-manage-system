<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-model="listQuery.keywords" placeholder="名称" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        search
      </el-button>
    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;"
      @sort-change="sortChange"
    >
      <el-table-column label="ID" prop="id" sortable="custom" align="center" width="80" :class-name="getSortClass('id')">
        <template slot-scope="{row}">
          <span>{{ row.id }}</span>
        </template>
      </el-table-column>
      <el-table-column label="account" prop="account" min-width="110px">
        <template slot-scope="{row}">
          <span>{{ row.account }}</span>
        </template>
      </el-table-column>
      <el-table-column label="studentId" prop="student_id" min-width="110px" />
      <el-table-column label="phone" align="center">
        <template slot-scope="{row}">
          <span>{{ row.phone }}</span>
        </template>
      </el-table-column>
      <el-table-column label="address" prop="address" />
      <el-table-column label="emergencyContact" prop="emergency_contact" />
      <el-table-column label="emergencyPhone" prop="emergency_phone" />
      <el-table-column label="major" prop="major" />
      <el-table-column label="operate" align="center" width="230" class-name="small-padding fixed-width">
        <template slot-scope="{row,$index}">
          <el-button v-if="row.status!='deleted'" size="mini" type="danger" @click="handleDelete(row,$index)">
            delete
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />
  </div>
</template>

<script>
import { getStudentList, createUser, updateUser, deleteStudentUser, imageUpload } from '@/api/user'
import waves from '@/directive/waves' // waves directive
import Pagination from '@/components/Pagination' // secondary package based on el-pagination
import crypto from '@/crypto'

const genderOptions = [
  { key: 0, display_name: '未知' },
  { key: 1, display_name: 'male' },
  { key: 2, display_name: 'Female' }
]

const genderKeyValue = genderOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'Student',
  components: { Pagination },
  directives: { waves },
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'info',
        deleted: 'danger'
      }
      return statusMap[status]
    },
    typeFilter(type) {
      return genderKeyValue[type]
    },
    wechatFilter(type) {
      return type ? '是' : '否'
    },
    adminFilter(type) {
      return type ? '是' : '否'
    }
  },
  data() {
    return {
      tableKey: 0,
      list: null,
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        keywords: undefined,
        sort: '-id'
      },
      importanceOptions: [1, 2, 3],
      genderOptions,
      sortOptions: [{ label: 'ID Ascending', key: '+id' }, { label: 'ID Descending', key: '-id' }],
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      getStudentList({...this.listQuery, userType: this.$store.state.user.userType}).then(response => {
        this.list = response.data.results
        this.total = response.data.count

        this.listLoading = false
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    handleModifyStatus(row, status) {
      this.$message({
        message: 'Operation Success',
        type: 'success'
      })
      row.status = status
    },
    sortChange(data) {
      const { prop, order } = data
      if (prop === 'id') {
        this.sortByID(order)
      }
    },
    sortByID(order) {
      if (order === 'ascending') {
        this.listQuery.sort = 'id'
      } else {
        this.listQuery.sort = '-id'
      }
      this.handleFilter()
    },
    handleDelete(row) {
      deleteStudentUser({ id: row.id, userType: this.$store.state.user.userType }).then(() => {
        this.getList()
        this.$notify({
          title: 'notice',
          message: 'Successfully deleted',
          type: 'success',
          duration: 2000
        })
      })
    },
    getSortClass: function(key) {
      const sort = this.listQuery.sort
      return sort === `${key}` ? 'ascending' : 'descending'
    }
  }
}
</script>

<style>
</style>
