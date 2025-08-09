
import {useEffect, useState} from 'react'

export default function Home() {
  const [notes, setNotes] = useState([])
  const api = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'

  useEffect(()=>{
    fetch(api + '/api/notes?username=demo') // for quick demo use username=demo
      .then(r=>r.json())
      .then(setNotes).catch(console.error)
  },[])

  return <div style={{padding:20}}>
    <h1>Memnotes - Notes</h1>
    <a href="/login">Login / Signup</a>
    <a style={{marginLeft:20}} href="/create">Create Note</a>
    <ul>
      {notes && notes.map(n=>(<li key={n.code}><strong>{n.title}</strong> - {n.content.slice(0,80)} <a href={'/notes/'+n.code}>open</a></li>))}
    </ul>
  </div>
}
