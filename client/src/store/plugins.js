import axios from 'axios'
import qs from 'qs'
import baseAPI from '@/apis/base'

function getRequestInstance(store) {
  const instance = axios.create()
  instance.defaults.withCredentials = true // 跨域请求携带cookie
  
  instance.interceptors.request.use((config) => {
    if (!config.hideLoading) store.commit('pushLoading') // 添加loading弹窗
    
    const headers = {}
  
    // 后端不支持 json 格式的 data，需要将 json 格式转为 x-www-form-urlencoded
    if (typeof config.data === 'object' && !(config.data instanceof FormData)) {
      config.data = qs.stringify(config.data)
      Object.assign(headers, { 'Content-Type': 'application/x-www-form-urlencoded' })
    }
    
    // 添加 X-Requested-With，表明是AJax异步请求
    Object.assign(headers, { 'X-Requested-With': 'XMLHttpRequest' })

    return Object.assign(config, { headers })
  });

  /* 添加响应拦截器 */
  instance.interceptors.response.use((response) => {
    if (!response.config.hideLoading) store.commit('popLoading') // 去除loading弹窗

    switch (response.data.code) {
      // 未登录
      case 302:
        if (response.data.data) {
          window.location.href = response.data.data.redirectUrl
        }
        return Promise.reject()
      // 正常
      case 0:
        return Promise.resolve({
          code: response.data.code,
          data: response.data.data,
          message: response.data.message
        })
      // 其他错误
      default:
        return Promise.reject(response.data.message)
    }
  }, (error) => {
    return Promise.reject(`与服务器通信遇到了问题（${error.message}）`);
  });

  return instance;
}

export default function plugins(store) {
  const axios = getRequestInstance(store);
  store.api = Object.assign(
    {},
    { base: baseAPI(axios.request) }
  )
}
