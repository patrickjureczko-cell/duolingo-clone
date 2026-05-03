import axios from 'axios'

function getSessionId(): string {
  let id = localStorage.getItem('session_id')
  if (!id) {
    id = crypto.randomUUID()
    localStorage.setItem('session_id', id)
  }
  return id
}

export const sessionId = getSessionId()

const client = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
})

client.interceptors.request.use((config) => {
  config.headers['X-Session-ID'] = sessionId
  return config
})

export default client
