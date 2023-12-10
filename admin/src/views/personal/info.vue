<template>
  <div class="app-container">
    <el-form ref="dataForm" :rules="rules" :model="formData" label-position="left" label-width="150px"
      style="width: 400px; margin-left:50px;">
      <el-form-item label="account" prop="account">
        <el-input v-model="formData.account" :disabled="true" />
      </el-form-item>
      <el-form-item label="studentId" prop="student_id">
        <el-input v-model="formData.student_id" />
      </el-form-item>
      <el-form-item label="phone" prop="phone">
        <el-input v-model="formData.phone" type="phone" />
      </el-form-item>
      <el-form-item label="email" prop="email">
        <el-input v-model="formData.email" />
      </el-form-item>
      <el-form-item label="address" prop="address">
        <el-input v-model="formData.address" />
      </el-form-item>
      <el-form-item label="emergencyContact" prop="emergency_contact">
        <el-input v-model="formData.emergency_contact" />
      </el-form-item>
      <el-form-item label="emergencyPhone" prop="emergency_phone">
        <el-input v-model="formData.emergency_phone" />
      </el-form-item>
      <el-form-item label="major" prop="major">
        <el-input v-model="formData.major" />
      </el-form-item>
    </el-form>
    <div class="footer">
      <el-button type="primary" @click="handleUpdataInfo()">save</el-button>
    </div>

    <el-dialog title="Set security issues" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :rules="securityRules" :model="securityFormData" label-position="left" label-width="130px"
        style="width: 400px; margin-left:50px;">
        <el-form-item label="securityIssues" prop="security_issues">
          <el-input v-model="securityFormData.security_issues" />
        </el-form-item>
        <el-form-item label="securityAnswer" prop="security_answer">
          <el-input v-model="securityFormData.security_answer" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="handleSetSecurity">
          confirm
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>
  
<script>
import { getStudentInfo, updateStudentUser, setSecurityIssues } from '@/api/user'
import waves from '@/directive/waves' // waves directive
import crypto from '@/crypto'

const genderOptions = [
  { key: 0, display_name: 'unknown' },
  { key: 1, display_name: 'male' },
  { key: 2, display_name: 'Female' }
]

export default {
  name: 'Info',
  directives: { waves },
  data() {
    const validateEmail = (rule, value, callback) => {
      var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      if (!re.test(value)) {
        callback(new Error('Please enter the correct user email'))
      } else {
        callback()
      }
    };
    return {
      genderOptions,
      formData: {
        account: '',
        student_id: '',
        phone: '',
        email: '',
        province: '',
        city: '',
        address: '',
        emergency_contact: '',
        emergency_phone: '',
        major: ''
      },
      rules: {
        email: [{ required: true, trigger: 'blur', validator: validateEmail }],
        student_id: [{ required: true, message: 'Please enter the student ID', trigger: 'change' }]
      },
      securityFormData: {
        security_issues: '',
        security_answer: ''
      },
      dialogFormVisible: false,
      dialogStatus: '',
      securityRules: {
        security_issues: [{ required: true, message: 'Please enter a security question', trigger: 'change' }],
        security_answer: [{ required: true, message: 'Please enter the answer to the security question', trigger: 'change' }]
      }
    }
  },
  created() {
    this.handleGetStudentInfo()
  },
  methods: {
    handleSetSecurity() {
      let data = { ...this.securityFormData, userType: this.$store.state.user.userType }
      data.security_answer = crypto.encrypt(data.security_answer)
      data.user_id = this.formData.id
      setSecurityIssues(data).then(() => {
        this.dialogFormVisible = false
        this.handleGetStudentInfo()
        this.$notify({
          title: 'notice',
          message: 'Successfully set',
          type: 'success',
          duration: 2000
        })
      })
    },
    handleGetStudentInfo() {
      getStudentInfo().then(response => {
        this.formData = response.data
        if (!response.data.security_issues && !response.data.security_answer) {
          this.dialogFormVisible = true
        }
      })
    },
    handleUpdataInfo() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          let data = { ...this.formData, userType: this.$store.state.user.userType }
          updateStudentUser(data).then(() => {
            this.handleGetStudentInfo()
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
  }
}
</script>
  
<style>
.footer {
  padding-left: 20px;
}
</style>
  