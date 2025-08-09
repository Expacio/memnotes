
import {useEffect, useState} from 'react'
import {useRouter} from 'next/router'
export default function Note(){
  const router = useRouter()
  const {id} = router.query
  const [note,setNote]=useState(null)
  const api = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'
  useEffect(()=>{
    if(!id) return
    fetch(api+'/api/notes/'+id+'?username=demo').then(r=>r.json()).then(setNote)
  },[id])
  if(!note) return <div>Loading...</div>
  return <div style={{padding:20}}>
    <h2>{note.title}</h2>
    <div>{note.content}</div>
  </div>
}
