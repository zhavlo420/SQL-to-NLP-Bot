"use client";
import {useState} from "react";

type Result={answer:string;sql?:string;rows:Record<string,unknown>[];columns:string[];trace:{agent:string;message:string}[];assumptions:string[]};

export default function Home(){
  const [question,setQuestion]=useState("");
  const [loading,setLoading]=useState(false);
  const [result,setResult]=useState<Result|null>(null);
  const [error,setError]=useState("");

  async function ask(){
    if(!question.trim())return;
    setLoading(true);setError("");setResult(null);
    try{
      const r=await fetch(`${process.env.NEXT_PUBLIC_API_URL||"http://localhost:8000"}/api/chat`,{
        method:"POST",headers:{"Content-Type":"application/json"},
        body:JSON.stringify({question})
      });
      const d=await r.json();
      if(!r.ok)throw new Error(d.detail||"Request failed");
      setResult(d);
    }catch(e){setError(e instanceof Error?e.message:"Request failed")}
    finally{setLoading(false)}
  }

  return <main style={{maxWidth:1200,margin:"0 auto",padding:"48px 24px"}}>
    <header><h1 style={{fontSize:44,marginBottom:4}}>QueryMind</h1><p style={{color:"#a1a1aa"}}>Agentic SQL → Natural Language Intelligence</p></header>
    <section style={{marginTop:36,padding:24,border:"1px solid #27272a",borderRadius:18}}>
      <textarea value={question} onChange={e=>setQuestion(e.target.value)} rows={4}
        placeholder="Ask your database anything..."
        style={{width:"100%",boxSizing:"border-box",background:"#18181b",color:"#fff",border:"1px solid #3f3f46",borderRadius:12,padding:16,fontSize:17}}/>
      <button onClick={ask} disabled={loading} style={{marginTop:12,padding:"12px 20px",border:0,borderRadius:10}}>
        {loading?"Agents working...":"Run Query →"}
      </button>
    </section>
    {error&&<div style={{marginTop:20,padding:16,background:"#3f1515",borderRadius:12}}>{error}</div>}
    {result&&<div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:20,marginTop:24}}>
      <section style={{padding:20,border:"1px solid #27272a",borderRadius:16}}>
        <h2>Answer</h2><p>{result.answer}</p>
        <h3>SQL</h3><pre style={{overflowX:"auto",background:"#111113",padding:16,borderRadius:10}}>{result.sql}</pre>
        <h3>Assumptions</h3><ul>{result.assumptions.map((x,i)=><li key={i}>{x}</li>)}</ul>
      </section>
      <section style={{padding:20,border:"1px solid #27272a",borderRadius:16}}>
        <h2>Agent Trace</h2>
        {result.trace.map((t,i)=><div key={i} style={{padding:"10px 0",borderBottom:"1px solid #27272a"}}><b>{t.agent}</b><div style={{color:"#a1a1aa"}}>{t.message}</div></div>)}
        <h2>Results</h2>
        <div style={{overflowX:"auto"}}><table style={{width:"100%",borderCollapse:"collapse"}}><thead><tr>{result.columns.map(c=><th key={c} style={{textAlign:"left",padding:8}}>{c}</th>)}</tr></thead>
        <tbody>{result.rows.map((row,i)=><tr key={i}>{result.columns.map(c=><td key={c} style={{padding:8,borderTop:"1px solid #27272a"}}>{String(row[c]??"")}</td>)}</tr>)}</tbody></table></div>
      </section>
    </div>}
  </main>
}
