
import {useState} from 'react'
export default function Create(){
  const [content,setContent]=useState('')
  const api = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'
  async function doCreate(e){
    e.preventDefault()
    const res = await fetch(api+'/api/notes',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({content,username:'demo'})})
    if(res.ok) window.location='/'
    else alert('failed')
  }
  return <div style={{padding:20}}>
    <h2>Create Note</h2>
    <form onSubmit={doCreate}>
      <textarea value={content} onChange={e=>setContent(e.target.value)} rows={8} cols={60}></textarea><br/>
      <button>Create</button>
    </form>
  </div>
}
