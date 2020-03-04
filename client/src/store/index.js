import Vue from 'vue'
import Vuex from 'vuex'
import plugins from './plugins';

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    config: {
      isFetching: false,
      initiated: false
    },
    username: '',
    loading: {
      count: 0,
      message: ''
    }
  },
  mutations: {
    getUserInfo(state, payload) {
      Object.assign(state.config, {
        isFetching: false,
        initiated: true
      })
      state.username = payload.username
    },
    clearUsername(state) {
      state.username = ''
    },
    pushLoading(state, payload) {
      state.loading.count++
      if (payload) {
        state.loading.message = payload.message
      }
    },
    popLoading(state) {
      state.loading.count--
      state.loading.message = ''
    }
  },
  actions: {
    getUserInfo: ({ commit }) => new Promise((resolve, reject) => {
      const dataState = store.state.config
      if (dataState.initiated) {
        // 已调接口且返回数据成功
        resolve(dataState)
        return
      }
      if (dataState.isFetching) {
        // 已调接口且没有数据返回，解决数据重复请求但返回较慢的情况
        const disableWatcher = store.watch(state => state.config.isFetching, () => {
          if (dataState.initiated) {
            resolve(dataState)
            disableWatcher()
            return
          }
        })
      } else {
        dataState.isFetching = true
        store.api.base.getUserInfo().then(data => {
          commit('getUserInfo', { username: data.username })
          resolve()
        }).catch(reject)
      }
    })
  },
  plugins: [plugins]
})

function wrapApi(vm, obj) {
  const api = {}
  Object.keys(obj).forEach(key => {
    switch (typeof obj[key]) {
      case 'object':
        api[key] = wrapApi(vm, obj[key])
        return
      case 'function': {
        api[key] = (...apiArgs) => new Promise((resolve, reject) => {
          obj[key].apply(obj, apiArgs).then((...resolvedArgs) => {
            if (!vm._isDestroyed) {
              resolve.apply(null, resolvedArgs)
            }
          }).catch(reject)
        })
        return
      }
      default:
    }
  })
  return api
}

Vue.mixin({
  created() {
    let wrapped
    const vm = this
    if (vm.$api) return
    /**
     * 异步回调可能会在 vm 销毁后才被调用（如切换页面后），此时 vm 的 computed 变量
     * 被置为 null，使用到 computed 的变量的回调在 vm 被销毁后调用时可能会抛错。
     *
     * 为了避免这种抛错，应该在 vm 销毁前判断取消回调 或 调用回调前判断 vm 是否被销毁。
     *
     * 可能用到了异步回调的地方：
     *   - setTimeout / setInterval
     *       应在 beforeDestroy 的 hook 中 cancel 掉
     *   - EventListener.listen 等注册
     *       应有对应的 remove 方法并在 beforeDestroy 中调用
     *   - 一个异步调用的调用栈很深且其中的参数有函数
     *       暂无解决
     *   - $api 请求
     *       resolve 前判断 vm 是否已销毁
     *
     * 为了避免修改大量已有代码，这里对 $api 用 Promise 包装
     * 若 $api 请求 resolve 后 vm 已销毁，则该 Promise 不 resolve
    */
    Object.defineProperty(this, '$api', {
      /**
       * 仅在 vm 第一次获取 $api 时才包装，否则初始化一个页面会多耗时 30ms
       */
      get() {
        if (wrapped) return wrapped
        wrapped = wrapApi(vm, store.api)
        return wrapped
      }
    })
  }
})

export default store