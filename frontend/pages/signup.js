
import {useState} from 'react'
export default function Signup(){
  const [username,setUsername]=useState('')
  const [password,setPassword]=useState('')
  const api = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'
  async function doSignup(e){
    e.preventDefault()
    const res = await fetch(api+'/api/signup',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username,password})})
    const data = await res.json()
    if(res.ok) window.location='/login'
    else alert(JSON.stringify(data))
  }
  return <div style={{padding:20}}>
    <h2>Signup</h2>
    <form onSubmit={doSignup}>
      <input placeholder='username' value={username} onChange={e=>setUsername(e.target.value)} />
      <input placeholder='password' type='password' value={password} onChange={e=>setPassword(e.target.value)} />
      <button>Signup</button>
    </form>
  </div>
}
