export default function (request) {
  return {
    login(data) {
      return request({ url: '/login', method: 'POST', data })
        .then(data => data)
    },
    logout(data) {
      return request({ url: '/logout', method: 'POST', data })
        .then(data => data)
    },
    getUserInfo() {
      return request({ url: '/getUserInfo', method: 'GET' })
        .then(data => data.data)
    },
    upload(data) {
      return request({ url: '/upload', method: 'POST', data })
        .then(data => data)
    }
  }
}
