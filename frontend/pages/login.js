
import {useState} from 'react'
export default function Login(){
  const [username,setUsername]=useState('')
  const [password,setPassword]=useState('')
  const api = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'
  async function doLogin(e){
    e.preventDefault()
    const res = await fetch(api+'/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username,password}),credentials:'include'})
    const data = await res.json()
    if(res.ok) window.location='/'
    else alert(JSON.stringify(data))
  }
  return <div style={{padding:20}}>
    <h2>Login</h2>
    <form onSubmit={doLogin}>
      <input placeholder='username' value={username} onChange={e=>setUsername(e.target.value)} />
      <input placeholder='password' type='password' value={password} onChange={e=>setPassword(e.target.value)} />
      <button>Login</button>
    </form>
    <p>or <a href='/signup'>Signup</a></p>
  </div>
}
