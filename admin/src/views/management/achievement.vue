<template>
    <div class="app-container">
        <div class="filter-container">
            <el-input v-model="listQuery.keywords" placeholder="account" style="width: 200px;" class="filter-item"
                @keyup.enter.native="handleFilter" />
            <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
                search
            </el-button>
        </div>

        <el-table :key="tableKey" v-loading="listLoading" :data="list" border fit highlight-current-row style="width: 100%;"
            @sort-change="sortChange">
            <el-table-column label="ID" prop="id" sortable="custom" align="center" width="80"
                :class-name="getSortClass('id')">
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
            <el-table-column label="emergency_contact" prop="emergency_contact" />
            <el-table-column label="emergency_phone" prop="emergency_phone" />
            <el-table-column label="major" prop="major" />
            <el-table-column label="operate" align="center" width="230" class-name="small-padding fixed-width">
                <template slot-scope="{row,$index}">
                    <el-button v-if="row.status != 'deleted'" size="mini" @click="handleShowScore(row.id)">
                        manager
                    </el-button>
                </template>
            </el-table-column>
        </el-table>

        <pagination v-show="total > 0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit"
            @pagination="getList" />

        <el-dialog title="performance management" :visible.sync="dialogTableVisible">

            <el-button v-waves type="primary" @click="handleCreate">
                new grades 
            </el-button>
            <el-table :key="1" :data="studentScoreList" border fit highlight-current-row
                style="width: 100%;">
                <el-table-column label="ID" prop="id" sortable="custom" align="center" width="80"
                    :class-name="getSortClass('id')">
                    <template slot-scope="{row}">
                        <span>{{ row.id }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="course" prop="course_id" min-width="110px">
                    <template slot-scope="{row}">
                    <span>{{ getCourseKeyValue(row.course_id) }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="grade" prop="grade" />
                <el-table-column label="midtermExamScore" prop="midterm_exam_score" />
                <el-table-column label="finalExamScore" prop="final_exam_score" />
                <el-table-column label="operate" align="center" width="230" class-name="small-padding fixed-width">
                    <template slot-scope="{row,$index}">
                        <el-button type="primary" size="mini" @click="handleUpdate(row)">
                            edit
                        </el-button>
                        <el-popconfirm
                            :key="row.id"
                            title="Are you sure to delete it?"
                            @onConfirm="handleDelete(row,$index)"
                        >
                            <el-button slot="reference" v-if="row.status!='deleted'" size="mini" type="danger">
                                delete
                            </el-button>
                        </el-popconfirm>
                    </template>
                </el-table-column>
            </el-table>
        </el-dialog>


    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :rules="rules" :model="formData" label-position="left" label-width="150px" style="width: 400px; margin-left:50px;">
        <el-form-item label="course" prop="course_id">
          <el-select v-model="formData.course_id" class="filter-item" placeholder="Please select">
            <el-option v-for="item in courseList" :key="item.id" :label="item.course_name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="grade" prop="grade">
          <el-input v-model="formData.grade" />
        </el-form-item>
        <el-form-item label="midtermExamScore" prop="midterm_exam_score">
          <el-input v-model="formData.midterm_exam_score" />
        </el-form-item>
        <el-form-item label="finalExamScore" prop="final_exam_score">
          <el-input v-model="formData.final_exam_score" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
            cancel
        </el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createData():updateData()">
            confirm
        </el-button>
      </div>
    </el-dialog>
    </div>
</template>
  
<script>
import { getStudentList, createUser, updateUser, deleteStudentUser, getStudentScoreList, getCourseList, createStudentScore, updateStudentScore, deleteStudentScore } from '@/api/user'
import waves from '@/directive/waves' // waves directive
import Pagination from '@/components/Pagination' // secondary package based on el-pagination
import crypto from '@/crypto'

const genderOptions = [
    { key: 0, display_name: 'unknown' },
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
        courseFilter(type) {
            return courseKeyValue[type]
        }
    },
    data() {
        return {
            student_id: null,
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
            dialogTableVisible: false,
            studentScoreList: [],
            courseList: [],
            formData: {
                student_id: '',
                teacher_id: '',
                course_id: '',
                grade: '',
                midterm_exam_score: '',
                final_exam_score: ''
            },
            dialogFormVisible: false,
            dialogStatus: '',
            textMap: {
                update: 'edit',
                create: 'add'
            },
            rules: {
                course_id: [{ required: true, message: 'Please select a course', trigger: 'change' }]
            }
        }
    },
    created() {
        this.getList()
        this.handleGetCourseList()
    },
    methods: {
        getList() {
            this.listLoading = true
            getStudentList({ ...this.listQuery, userType: this.$store.state.user.userType }).then(response => {
                this.list = response.data.results
                this.total = response.data.count

                this.listLoading = false
            })
        },
        handleGetCourseList() {
            getCourseList().then(response => {
                this.courseList = response.data
            })
        },
        getCourseKeyValue(type) {
            const courseKeyValue = this.courseList.reduce((acc, cur) => {
                    acc[cur.id] = cur.course_name
                    return acc
                }, {})
            return courseKeyValue[type]
        },
        handleShowScore(uid) {
            getStudentScoreList({...this.listQuery, uid}).then(response => {
                this.student_id = uid
                this.studentScoreList = response.data
                this.dialogTableVisible = true
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
        resetTemp() {
            this.formData = {
                student_id: '',
                teacher_id: '',
                course_id: '',
                grade: '',
                midterm_exam_score: '',
                final_exam_score: ''
            }
        },
        handleCreate() {
        this.resetTemp()
        this.dialogStatus = 'create'
        this.dialogFormVisible = true
        this.$nextTick(() => {
            this.$refs['dataForm'].clearValidate()
        })
        },
        createData() {
        this.$refs['dataForm'].validate((valid) => {
            if (valid) {
            let data = {...this.formData, userType: this.$store.state.user.userType}
            data.student_id = this.student_id
            createStudentScore(data).then(() => {
                this.dialogFormVisible = false
                this.handleShowScore(this.student_id)
                this.$notify({
                title: 'notice',
                message: 'Created successfully',
                type: 'success',
                duration: 2000
                })
            })
            }
        })
        },
        handleUpdate(row) {
        console.log(row)
        this.formData = Object.assign({}, row) // copy obj
        this.formData.password = crypto.decrypt(this.formData.password)
        this.dialogStatus = 'update'
        this.dialogFormVisible = true
        this.$nextTick(() => {
            this.$refs['dataForm'].clearValidate()
        })
        },
        updateData() {
        this.$refs['dataForm'].validate((valid) => {
            if (valid) {
            let data = {...this.formData, userType: this.$store.state.user.userType}
            data.student_id = this.student_id
            updateStudentScore(data).then(() => {
                this.dialogFormVisible = false
                this.handleShowScore(this.student_id)
                this.$notify({
                title: 'notice',
                message: 'Successfully modified',
                type: 'success',
                duration: 2000
                })
            })
            }
        })
        },
        handleDelete(row) {
            deleteStudentScore({ id: row.id, userType: this.$store.state.user.userType }).then(() => {
                this.handleShowScore(this.student_id)
                this.$notify({
                    title: 'notice',
                    message: 'Successfully deleted',
                    type: 'success',
                    duration: 2000
                })
            })
        },
        getSortClass: function (key) {
            const sort = this.listQuery.sort
            return sort === `${key}` ? 'ascending' : 'descending'
        }
    }
}
</script>
  
<style></style>
  