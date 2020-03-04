<template>
  <div id="app">
    <div class="m-top-nav" v-show="showTopNav">
      <nav>
        <ul class="clearfix">
          <li><router-link to="/processing">图像处理</router-link></li>
          <li><router-link to="/knowledge">算法解析</router-link></li>
        </ul>
      </nav>
      <div class="userinfo">
        <span class="username">{{ username }}</span>
        <span class="logout" @click="logout">退出</span>
      </div>
    </div>
    <router-view/>
    <loading-mask :show="showLoading" :message="loadingMessage"></loading-mask>
  </div>
</template>

<script>
import LoadingMask from '@/components/LoadingMask.vue'

export default {
  data () {
    return {
      showTopNav: false
    }
  },
  computed: {
    username() {
      return this.$store.state.username
    },
    showLoading() {
      return this.$store.state.loading.count > 0
    },
    loadingMessage() {
      return this.$store.state.loading.message
    }
  },
  methods: {
    logout() {
      this.$api.base.logout({
        username: this.username
      }).then(res => {
        if (res.data) {
          this.$store.commit('clearUsername')
          this.$router.push('/login')
        }
      })
    }
  },
  watch: {
    async '$route' () {
      await this.$store.dispatch('getUserInfo')
      const path = this.$route.path
      this.showTopNav = path !== '/login'
      if (path === '/login') {
        if (this.username) this.$router.replace('/processing')
      } else {
        if (!this.username) this.$router.replace('/login')
      }
    }
  },
  components: {
    LoadingMask
  }
}
</script>

<style lang="scss">
@import '~@/assets/base.scss';
</style>
