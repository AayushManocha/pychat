"use client"

import { FormEvent, useContext, useState } from "react"
import axios from 'axios'
import { useNavigate } from "@remix-run/react"
import { UserContext } from "~/root"

export default function LoginPage() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  const [errorMessage, setErrorMessage] = useState<any | undefined>()

  const navigate = useNavigate()

  const userContext = useContext(UserContext)

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    axios.post('http://localhost:8000/login', { username, password }, { withCredentials: true })
      .then(res => {
        userContext?.setUser(res.data?.user)
        navigate('/')
      })
      .catch(err => setErrorMessage(err.response.data.detail))
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
      <h2> Login</h2>
      <form onSubmit={handleSubmit}>
        <fieldset>
          <label>
            Username
            <input onChange={e => setUsername(e.target.value)} value={username} type="text" name="username" />
          </label>
          <label>
            Password
            <input onChange={e => setPassword(e.target.value)} value={password} type="password" name="password" />
          </label>
        </fieldset>
        <p style={{ color: 'red' }}>{JSON.stringify(errorMessage)}</p>
        <button type="submit">Login</button>
      </form>
    </ div>
  )
}