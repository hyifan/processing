<template>
  <div>
    <form @submit.prevent.stop @submit="checkForm" class="form clearfix">
      <div class="item">
        <label for="username">用户名</label>
        <input type="text" v-model="username" id="username" required>
      </div>
      <div class="item">
        <label for="password">密码</label>
        <input type="password" v-model="password" id="password" autocomplete required>
      </div>
      <button type="submit">登录</button>
    </form>
    <modal-dialog
      :show.sync="showSuccessModal"
      :content-style="modalStyle"
      noClose
      noCancel>
      <p>{{ message }}，{{ second }}秒后自动跳往首页</p>
      <template v-slot:footer>
        <button class="btn-right" @click="goIndex">前往首页</button>
      </template>
    </modal-dialog>
    <toast-message
      :show.sync="showErrorToast"
      :message="message"
      error
    ></toast-message>
  </div>
</template>


<script>
// @ is an alias to /src
import sha from 'js-sha256'
import ModalDialog from '@/components/ModalDialog.vue'
import ToastMessage from '@/components/ToastMessage.vue'

export default {
  data() {
    return {
      username: '',
      password: '',
      showSuccessModal: false,
      showErrorToast: false,
      message: '',
      second: 0,
      modalStyle: {
        width: '400px',
        height: '180px'
      }
    }
  },
  methods: {
    checkForm() {
      this.login()
    },
    login() {
      this.$api.base.login({
        username: this.username,
        password: sha.sha256(this.password)
      }).then(res => {
        this.message = res.message
        if (res.data) {
          this.showSuccessModal = true
          this.second = 3
          const set = setInterval(() => {
            this.second--
            if(this.second === 0) {
              clearInterval(set)
              this.goIndex()
            }
          }, 1000)
        } else {
          this.showErrorToast = true
        }
      })
    },
    goIndex() {
      this.$store.commit('getUserInfo', {
        username: this.username
      })
      this.$router.push('/processing')
    }
  },
  components: {
    ModalDialog,
    ToastMessage
  }
}
</script>
<style lang="scss" scoped>
.form {
  width: 312px;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  .item {
    margin-bottom: 20px;
  }
  label {
    width: 80px;
    text-align: right;
    display: inline-block;
    margin-right: 10px;
  }
  input {
    width: 200px;
  }
  button {
    float: right;
  }
}
</style>