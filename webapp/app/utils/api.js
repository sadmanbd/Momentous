class API {
  constructor(options) {
    this.$http = options.http
  }

  setToken(token, type = null, scopes = 'common') {
    this.$http.setToken(token, type, scopes)
  }

  clearToken() {
    this.setToken(false)
  }

  async createWallet(id, fullname) {
    const res = await this.post('user/wallet/' + id, fullname)
    return res
  }

  get(resource, params = {}) {
    return this.$http.$get(resource, {
      params
    })
  }

  post(resource, data = {}, params = {}) {
    return this.$http.$post(resource, data, {
      params
    })
  }

  listCauses() {
    return this.get('/causes/list')
  }

  async upVote(userId, causeId, type) {
    const res = await this.post('/cause/vote/' + userId + '/' + causeId, type)
    return res
  }

  getLeaderboard() {
    return this.get('/users/leaderboard')
  }
}

export default API
