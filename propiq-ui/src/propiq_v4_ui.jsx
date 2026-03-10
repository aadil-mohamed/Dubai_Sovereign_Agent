import { useState, useEffect, useRef, useCallback } from "react";

const AGENTS = [
  { id:"parser",    label:"Query Parser",    copy:"Deploying NLP Intelligence",   sub:"Parsing natural language → strict JSON",     icon:"01", color:"#C9A84C", ms:900  },
  { id:"vision",    label:"GPT-4o Vision",   copy:"Scoring Luxury Aesthetics",    sub:"GPT-4o scanning property image",             icon:"02", color:"#00E5A0", ms:2200 },
  { id:"financial", label:"XGBoost Engine",  copy:"Validating Market Pricing",    sub:"10,000 DLD records computing baseline",      icon:"03", color:"#60A5FA", ms:600  },
  { id:"scout",     label:"Market Scout",    copy:"Scanning Live Comparables",    sub:"Tavily scraping Bayut + PropertyFinder",     icon:"04", color:"#FBBF24", ms:1800 },
  { id:"legal",     label:"Legal / Risk",    copy:"Scanning Compliance Matrix",   sub:"Supabase RAG probing UAE law",               icon:"05", color:"#F472B6", ms:700  },
  { id:"supervisor",label:"Supervisor AI",   copy:"Synthesising Final Verdict",   sub:"Deterministic override + LLM synthesis",    icon:"06", color:"#A78BFA", ms:500  },
];

const GRADE = {
  A:{ color:"#00FF88", glow:"0 0 60px #00FF8877, 0 0 140px #00FF8833, 0 0 280px #00FF8811",
      bg:"rgba(0,255,136,0.04)", border:"rgba(0,255,136,0.2)",
      label:"SUPREMACY CONFIRMED", rec:"DEPLOY CAPITAL", sub:"Prime acquisition. No obstacles detected." },
  B:{ color:"#C9A84C", glow:"0 0 60px #C9A84C77, 0 0 140px #C9A84C33",
      bg:"rgba(201,168,76,0.04)", border:"rgba(201,168,76,0.2)",
      label:"OPPORTUNITY IDENTIFIED", rec:"HOLD FOR TERMS", sub:"Moderate upside. Negotiate entry price." },
  C:{ color:"#FB923C", glow:"0 0 60px #FB923C77, 0 0 140px #FB923C33",
      bg:"rgba(251,146,60,0.04)", border:"rgba(251,146,60,0.2)",
      label:"ELEVATED RISK ZONE", rec:"PROCEED WITH CAUTION", sub:"Risk-adjusted returns marginal." },
  D:{ color:"#FF4444", glow:"0 0 60px #FF444477, 0 0 140px #FF444433",
      bg:"rgba(255,68,68,0.04)", border:"rgba(255,68,68,0.2)",
      label:"DEFICIT DETECTED — ABORT", rec:"DO NOT PROCEED", sub:"Budget breach confirmed. Renegotiate or exit." },
};

const TICKER = ["DUBAI MARINA ▲2.4M","DOWNTOWN DXB ▼3.1M","PALM JUMEIRAH ▲8.7M","BUSINESS BAY ◆1.8M","JVC ▲950K","ARABIAN RANCHES ▼4.2M","CREEK HARBOUR ▲2.9M","MBR CITY ◆5.6M","DIFC ▲5.1M","JBR ▼3.3M","CITY WALK ▲2.2M","BLUEWATERS ◆6.8M"];

function useCounter(target, active, duration = 2000) {
  const [v, setV] = useState(0);
  useEffect(() => {
    if (!active || !target) return;
    let s = null;
    const tick = ts => {
      if (!s) s = ts;
      const p = Math.min((ts - s) / duration, 1);
      setV(Math.floor((1 - Math.pow(1 - p, 4)) * target));
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }, [target, active]);
  return v;
}

function useRipple() {
  const [ripples, setRipples] = useState([]);
  const add = useCallback((e) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - rect.left, y = e.clientY - rect.top;
    const id = Date.now();
    setRipples(r => [...r, { id, x, y }]);
    setTimeout(() => setRipples(r => r.filter(rp => rp.id !== id)), 700);
  }, []);
  return [ripples, add];
}

function QuantumStream() {
  const particles = Array.from({ length: 30 }, (_, i) => ({
    id: i,
    x: Math.random() * 100,
    y: Math.random() * 100,
    size: 1 + Math.random() * 2,
    dur: 8 + Math.random() * 16,
    delay: Math.random() * 12,
    color: i % 3 === 0 ? "#C9A84C" : i % 3 === 1 ? "#00E5A0" : "#A78BFA",
  }));
  return (
    <div style={{ position:"fixed", inset:0, pointerEvents:"none", zIndex:0, overflow:"hidden" }}>
      {particles.map(p => (
        <div key={p.id} style={{ position:"absolute", left:`${p.x}%`, top:`${p.y}%`, width:p.size, height:p.size, borderRadius:"50%", background:p.color, boxShadow:`0 0 4px ${p.color}`, opacity:0, animation:`drift ${p.dur}s ease-in-out ${p.delay}s infinite` }}/>
      ))}
    </div>
  );
}

function Vignette() {
  return <div style={{ position:"fixed", inset:0, pointerEvents:"none", zIndex:1, background:"radial-gradient(ellipse at 50% 50%, transparent 40%, rgba(0,0,0,0.55) 100%)" }}/>;
}

function LiveTicker({ speed = 0.5 }) {
  const [x, setX] = useState(0);
  const spRef = useRef(speed);
  useEffect(() => { spRef.current = speed; }, [speed]);
  useEffect(() => {
    const id = setInterval(() => setX(v => v - spRef.current), 16);
    return () => clearInterval(id);
  }, []);
  const items = [...TICKER,...TICKER,...TICKER];
  return (
    <div style={{ overflow:"hidden", height:26, display:"flex", alignItems:"center", borderTop:"1px solid rgba(201,168,76,0.08)", background:"rgba(4,4,3,0.92)" }}>
      <div style={{ display:"flex", gap:56, whiteSpace:"nowrap", transform:`translateX(${x%(TICKER.length*182)}px)`, willChange:"transform" }}>
        {items.map((t,i) => <span key={i} style={{ fontSize:9, letterSpacing:"0.16em", color:"rgba(201,168,76,0.38)", fontFamily:"'DM Mono',monospace" }}>{t}</span>)}
      </div>
    </div>
  );
}

function AgentCard({ agent, status, index }) {
  const isRun = status === "running";
  const isDone = status === "done";
  return (
    <div style={{ flex:1, padding:"22px 10px 16px", border:`1px solid ${isDone ? agent.color : isRun ? `${agent.color}99` : "rgba(255,255,255,0.06)"}`, background: isDone ? `${agent.color}0C` : isRun ? `${agent.color}07` : "rgba(6,6,5,0.9)", display:"flex", flexDirection:"column", alignItems:"center", gap:10, position:"relative", overflow:"hidden", transition:"all 0.4s ease", boxShadow: isDone ? `0 0 35px ${agent.color}20, 0 0 70px ${agent.color}0A` : isRun ? `0 0 25px ${agent.color}30` : "none", animation:`cardIn 0.5s ease ${index*0.07}s both` }}>
      <div style={{ position:"absolute", bottom:0, left:0, right:0, height:isDone?"100%":isRun?"60%":"0%", background:`linear-gradient(0deg,${agent.color}12,transparent)`, transition:"height 0.8s ease" }}/>
      {isRun && <div style={{ position:"absolute", inset:0, background:`radial-gradient(ellipse at 50% 120%, ${agent.color}18, transparent 70%)`, animation:"trailPulse 1.8s ease-in-out infinite" }}/>}
      {(isDone||isRun) && <div style={{ position:"absolute", top:0, left:0, right:0, height:2, background:`linear-gradient(90deg,transparent,${agent.color},transparent)`, animation:"scanLine 2s ease-in-out infinite" }}/>}
      <div style={{ width:48, height:48, border:`1.5px solid ${isDone?agent.color:isRun?agent.color:"rgba(255,255,255,0.1)"}`, display:"flex", alignItems:"center", justifyContent:"center", position:"relative", background:isDone?`${agent.color}18`:"transparent", boxShadow:isRun?`0 0 25px ${agent.color}70, inset 0 0 12px ${agent.color}20`:"none", transition:"all 0.4s" }}>
        {isDone ? <span style={{ fontSize:22, color:agent.color }}>✓</span> : <span style={{ fontSize:13, fontFamily:"'DM Mono',monospace", fontWeight:700, color:isRun?agent.color:"rgba(255,255,255,0.15)", transition:"color 0.4s" }}>{agent.icon}</span>}
        {isRun && <><div style={{ position:"absolute", inset:-5, border:`1px solid ${agent.color}`, animation:"ring 1.5s ease-out infinite" }}/><div style={{ position:"absolute", inset:-10, border:`1px solid ${agent.color}44`, animation:"ring 1.5s ease-out 0.3s infinite" }}/></>}
      </div>
      <div style={{ textAlign:"center", position:"relative" }}>
        <div style={{ fontSize:8.5, fontFamily:"'DM Mono',monospace", letterSpacing:"0.12em", color:isDone||isRun?agent.color:"rgba(255,255,255,0.18)", transition:"color 0.4s", fontWeight:700 }}>{agent.label.toUpperCase()}</div>
        <div style={{ fontSize:7, fontFamily:"'DM Mono',monospace", color:isRun?"rgba(255,255,255,0.5)":"rgba(255,255,255,0.15)", marginTop:3, transition:"color 0.4s" }}>{isRun ? agent.copy : agent.sub}</div>
      </div>
    </div>
  );
}

function ThoughtLog({ entries, running }) {
  const ref = useRef();
  useEffect(() => { if(ref.current) ref.current.scrollTop = ref.current.scrollHeight; }, [entries]);
  return (
    <div ref={ref} style={{ background:"#010100", border:"1px solid rgba(255,255,255,0.05)", fontFamily:"'DM Mono',monospace", fontSize:11, lineHeight:1.8, padding:"14px 18px", height:158, overflowY:"auto" }}>
      <div style={{ fontSize:10, letterSpacing:"0.22em", color:"rgba(201,168,76,0.35)", marginBottom:10 }}>◆ LIVE INTELLIGENCE STREAM</div>
      {!entries?.length && <div style={{ color:"rgba(255,255,255,0.14)", fontSize:10, fontStyle:"italic" }}>Pipeline dormant. Deploy query to initiate.</div>}
      {entries?.map((e,i) => {
        const a = AGENTS.find(x=>x.id===e.agent);
        return (
          <div key={i} style={{ marginBottom:3, animation:"slideIn 0.22s ease both" }}>
            <span style={{ color:a?.color||"#C9A84C", marginRight:10, fontWeight:700 }}>[{a?.label || e.agent}]</span>
            <span style={{ color:"rgba(232,224,208,0.6)" }}>{e.out || e.text || JSON.stringify(e)}</span>
          </div>
        );
      })}
      {running && <span style={{ color:"#C9A84C", animation:"blink 0.8s step-end infinite", fontSize:15 }}>█</span>}
    </div>
  );
}

function ImageDrop({ onImage, preview }) {
  const [drag, setDrag] = useState(false);
  const ref = useRef();
  return (
    <div onClick={()=>ref.current?.click()} onDragOver={e=>{e.preventDefault();setDrag(true);}} onDragLeave={()=>setDrag(false)} onDrop={e=>{e.preventDefault();setDrag(false);const f=e.dataTransfer.files[0];if(f?.type.startsWith("image/"))onImage(URL.createObjectURL(f));}} style={{ border:`1px dashed ${drag?"rgba(0,229,160,0.7)":preview?"rgba(0,229,160,0.4)":"rgba(255,255,255,0.1)"}`, background:preview?"rgba(0,229,160,0.03)":"transparent", padding:preview?"10px":"16px 14px", cursor:"pointer", transition:"all 0.25s", display:"flex", alignItems:"center", gap:14 }}>
      <input ref={ref} type="file" accept="image/*" style={{display:"none"}} onChange={e=>{const f=e.target.files[0];if(f)onImage(URL.createObjectURL(f));}}/>
      {preview ? (
        <>
          <img src={preview} alt="" style={{ width:44, height:44, objectFit:"cover", border:"1px solid rgba(0,229,160,0.4)" }}/>
          <div>
            <div style={{ fontSize:9, color:"#00E5A0", fontFamily:"'DM Mono',monospace", letterSpacing:"0.14em", fontWeight:700 }}>GPT-4o VISION DEPLOYED</div>
            <div style={{ fontSize:8, color:"rgba(255,255,255,0.25)", fontFamily:"'DM Mono',monospace", marginTop:2 }}>Luxury multiplier active · 1.0× – 1.5×</div>
          </div>
          <div style={{ marginLeft:"auto", width:8, height:8, borderRadius:"50%", background:"#00E5A0", boxShadow:"0 0 10px #00E5A0", animation:"blink 1.6s ease infinite" }}/>
        </>
      ) : (
        <><div style={{ fontSize:26, opacity:0.25, color:"#00E5A0" }}>◈</div><div><div style={{ fontSize:9.5, fontFamily:"'DM Mono',monospace", letterSpacing:"0.14em", color:"rgba(255,255,255,0.3)" }}>DEPLOY PROPERTY IMAGE</div><div style={{ fontSize:8, fontFamily:"'DM Mono',monospace", color:"rgba(255,255,255,0.15)", marginTop:2 }}>GPT-4o luxury assessment · drag or click to deploy</div></div></>
      )}
    </div>
  );
}

function GradeReveal({ grade, active }) {
  const [p, setP] = useState(0);
  const [flash, setFlash] = useState(false);
  const cfg = GRADE[grade] || GRADE["C"];

  useEffect(() => {
    if (!active) return;
    setTimeout(() => setP(1), 80);
    setTimeout(() => setP(2), 550);
    setTimeout(() => { setFlash(true); setTimeout(() => { setFlash(false); setTimeout(() => setFlash(true), 120); setTimeout(() => setFlash(false), 240); }, 0); }, 900);
    setTimeout(() => setP(3), 1100);
  }, [active, grade]);

  return (
    <div style={{ position:"relative", display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", padding:"48px 20px 40px", background:cfg.bg, border:`1px solid ${cfg.border}`, overflow:"hidden", minHeight:360 }}>
      <div style={{ position:"absolute", inset:0, background:`radial-gradient(ellipse at 50% 30%, ${cfg.color}16 0%, transparent 62%)`, opacity:p>=2?1:0, transition:"opacity 1.4s" }}/>
      {flash && <div style={{ position:"absolute", inset:0, background:`${cfg.color}18`, zIndex:2 }}/>}
      {p>=2 && [0,1,2].map(i => (<div key={i} style={{ position:"absolute", top:0, bottom:0, width:1, background:`linear-gradient(180deg,transparent,${cfg.color}55,transparent)`, left:`${25+i*25}%`, animation:`shimmer 2.5s ease ${i*0.4}s infinite` }}/>))}
      {[0,1,2,3].map(i => (<div key={i} style={{ position:"absolute", width:30, height:30, top:i<2?16:"auto", bottom:i>=2?16:"auto", left:i%2===0?16:"auto", right:i%2===1?16:"auto", borderTop:i<2?`1.5px solid ${cfg.color}`:"none", borderBottom:i>=2?`1.5px solid ${cfg.color}`:"none", borderLeft:i%2===0?`1.5px solid ${cfg.color}`:"none", borderRight:i%2===1?`1.5px solid ${cfg.color}`:"none", opacity:p>=1?0.6:0, transition:"opacity 0.5s" }}/>))}
      <div style={{ fontSize:"clamp(140px,26vw,220px)", fontFamily:"'Bebas Neue',cursive", lineHeight:1, color:cfg.color, letterSpacing:"-0.03em", textShadow:p>=2?cfg.glow:"none", opacity:p>=1?1:0, transform:p>=1?"scale(1)":"scale(0.3)", transition:"all 0.6s cubic-bezier(0.34,1.56,0.64,1)", position:"relative", zIndex:1 }}>{grade}</div>
      <div style={{ opacity:p>=3?1:0, transform:p>=3?"translateY(0)":"translateY(16px)", transition:"all 0.55s ease 0.1s", textAlign:"center", position:"relative", zIndex:1 }}>
        <div style={{ fontSize:9.5, fontFamily:"'DM Mono',monospace", letterSpacing:"0.25em", color:`${cfg.color}CC`, marginBottom:8 }}>{cfg.label}</div>
        <div style={{ fontSize:8, fontFamily:"'DM Mono',monospace", color:`${cfg.color}66`, marginBottom:18, letterSpacing:"0.12em" }}>{cfg.sub}</div>
        <div style={{ display:"inline-block", padding:"8px 36px", border:`1.5px solid ${cfg.border}`, fontSize:11.5, fontFamily:"'DM Mono',monospace", letterSpacing:"0.38em", color:cfg.color, fontWeight:700, background:`${cfg.color}0A`, boxShadow:`0 0 20px ${cfg.color}22` }}>▶  {cfg.rec}</div>
      </div>
    </div>
  );
}

function StatCard({ label, value, sub, accent, teal, delay=0 }) {
  const borderCol = accent ? "rgba(201,168,76,0.38)" : teal ? "rgba(0,229,160,0.25)" : "rgba(255,255,255,0.07)";
  const valCol = accent ? "#C9A84C" : teal ? "#00E5A0" : "#E8E0D0";
  return (
    <div style={{ padding:"18px", border:`1px solid ${borderCol}`, background:accent?"rgba(201,168,76,0.04)":teal?"rgba(0,229,160,0.03)":"rgba(255,255,255,0.01)", position:"relative", overflow:"hidden", animation:`slideUp 0.5s ease ${delay}s both` }}>
      {(accent||teal) && <div style={{ position:"absolute", top:0, left:0, right:0, height:1, background:`linear-gradient(90deg,transparent,${accent?"rgba(201,168,76,0.65)":"rgba(0,229,160,0.5)"},transparent)` }}/>}
      <div style={{ fontSize:7.5, letterSpacing:"0.2em", color:"rgba(255,255,255,0.26)", marginBottom:8, fontFamily:"'DM Mono',monospace" }}>{label}</div>
      <div style={{ fontSize:22, fontWeight:700, fontFamily:"'DM Mono',monospace", color:valCol, letterSpacing:"-0.01em" }}>{value}</div>
      {sub && <div style={{ fontSize:8, color:"rgba(255,255,255,0.24)", marginTop:5, fontFamily:"'DM Mono',monospace" }}>{sub}</div>}
    </div>
  );
}

export default function PropIQ() {
  const [phase, setPhase]     = useState("idle");
  const [query, setQuery]     = useState("2BR apartment Dubai Marina under AED 2.5M off-plan");
  const [preview, setPreview] = useState(null);
  const [agentSt, setSt]      = useState({});
  const [log, setLog]         = useState([]);
  const [result, setResult]   = useState(null);
  const [focus, setFocus]     = useState(false);
  const [gradeGo, setGA]      = useState(false);
  const [tickerSpd, setTS]    = useState(0.5);
  const [ripples, addRipple]  = useRipple();

  const baseC = useCounter(result?.baseVal,    !!result, 2000);
  const adjC  = useCounter(result?.adjustedVal,!!result, 2200);
  const roiC  = useCounter(result?Math.round(result.roi*10):0, !!result, 1600);
  const dldC  = useCounter(result?.dldFee,     !!result, 1400);

  const runAnalysis = useCallback(async (e) => {
    if (phase !== "idle") return;
    addRipple(e);
    setTS(3); setTimeout(() => setTS(0.5), 1200);
    setPhase("processing"); 
    setResult(null); setLog([]); setSt({});
    
    const animateAgents = async () => {
      for (const a of AGENTS) {
        setSt(s=>({...s,[a.id]:"running"}));
        await new Promise(r=>setTimeout(r,800));
      }
    };
    animateAgents();
    
    try {
      const res = await fetch("/api/analyze", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({ query, image: preview })
      });
      const data = await res.json();
      
      AGENTS.forEach(a => setSt(s=>({...s,[a.id]:"done"})));
      
      if (data.agentLog?.length) setLog(data.agentLog);

      // --- PROACTIVE GEOGRAPHY OVERRIDE ---
      const NON_DUBAI = ["sharjah","abu dhabi","ajman","fujairah","ras al khaimah","rak","umm al quwain"];
      if (NON_DUBAI.some(k => query.toLowerCase().includes(k))) {
          data.outOfMarket = true;
          data.grade = "C";
          data.summary = "Out-of-market query detected. XGBoost model is trained on Dubai DLD data only. Mapped to nearest Dubai comparable for indicative valuation. Treat with caution — non-Dubai pricing dynamics apply.";
      }
      
      setResult(data);
      setPhase("result");
      setTimeout(()=>setGA(true), 180);
    } catch(err) {
      console.error("Pipeline failed:", err);
      setPhase("idle");
    }
  }, [phase, query, preview, addRipple]);

  const reset = () => { setPhase("idle"); setResult(null); setLog([]); setSt({}); setGA(false); };
  const downloadPDF = async () => {
  if (!result) return;
  try {
    const res = await fetch("/api/pdf", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ ...result, query })
    });

    if (!res.ok) throw new Error("PDF failed");

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = "PropIQ_Sovereign_Dossier.pdf";
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  } catch (err) {
    console.error(err);
    alert("Failed to generate PDF dossier.");
  }
};

  return (
    <div style={{ minHeight:"100vh", background:"#060605", fontFamily:"'DM Mono',monospace", color:"#E8E0D0", position:"relative", overflowX:"hidden" }}>

      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:ital,wght@0,300;0,400;0,500;0,700;1,300&display=swap');
        @keyframes ring       { 0%{opacity:1;transform:scale(1)} 100%{opacity:0;transform:scale(1.9)} }
        @keyframes blink      { 0%,100%{opacity:1} 50%{opacity:0} }
        @keyframes scanLine   { 0%{opacity:0;transform:scaleX(0.05)} 50%{opacity:1;transform:scaleX(1)} 100%{opacity:0;transform:scaleX(1)} }
        @keyframes shimmer    { 0%{opacity:0;transform:translateY(-100%)} 40%{opacity:0.6} 100%{opacity:0;transform:translateY(100%)} }
        @keyframes trailPulse { 0%,100%{opacity:0.5} 50%{opacity:1} }
        @keyframes slideIn    { from{opacity:0;transform:translateX(-8px)} to{opacity:1;transform:none} }
        @keyframes slideUp    { from{opacity:0;transform:translateY(24px)} to{opacity:1;transform:none} }
        @keyframes cardIn     { from{opacity:0;transform:translateY(20px)} to{opacity:1;transform:none} }
        @keyframes fadeIn     { from{opacity:0} to{opacity:1} }
        @keyframes drift      { 0%{opacity:0;transform:translateY(0) scale(1)} 20%{opacity:0.6} 80%{opacity:0.3} 100%{opacity:0;transform:translateY(-80px) scale(0.3)} }
        @keyframes rippleOut  { 0%{transform:scale(0);opacity:0.5} 100%{transform:scale(4);opacity:0} }
        @keyframes glowPulse  { 0%,100%{box-shadow:0 0 25px rgba(201,168,76,0.08)} 50%{box-shadow:0 0 55px rgba(201,168,76,0.22),0 0 110px rgba(201,168,76,0.07)} }
        @keyframes heroFloat  { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-6px)} }
        * { box-sizing:border-box; margin:0; padding:0; }
        textarea:focus,button:focus { outline:none; }
        ::-webkit-scrollbar { width:3px; }
        ::-webkit-scrollbar-thumb { background:rgba(201,168,76,0.2); }
        ::selection { background:rgba(201,168,76,0.18); }
      `}</style>

      <QuantumStream/>
      <Vignette/>

      <div style={{ position:"fixed", width:1000, height:1000, borderRadius:"50%", right:"-30%", top:"-25%", background:"radial-gradient(circle,rgba(201,168,76,0.04) 0%,transparent 70%)", pointerEvents:"none", zIndex:0 }}/>
      <div style={{ position:"fixed", width:700, height:700, borderRadius:"50%", left:"-20%", bottom:"0%", background:"radial-gradient(circle,rgba(0,229,160,0.025) 0%,transparent 70%)", pointerEvents:"none", zIndex:0 }}/>
      <div style={{ position:"fixed", width:500, height:500, borderRadius:"50%", left:"40%", top:"30%", background:"radial-gradient(circle,rgba(167,139,250,0.015) 0%,transparent 70%)", pointerEvents:"none", zIndex:0 }}/>

      <div style={{ position:"fixed", inset:0, pointerEvents:"none", zIndex:0 }}>
        <svg style={{ position:"absolute", inset:0, width:"100%", height:"100%", opacity:0.018 }}><defs><pattern id="g" width="52" height="52" patternUnits="userSpaceOnUse"><path d="M52 0L0 0 0 52" fill="none" stroke="#C9A84C" strokeWidth="0.4"/></pattern></defs><rect width="100%" height="100%" fill="url(#g)"/></svg>
      </div>

      <header style={{ position:"relative", zIndex:10, borderBottom:"1px solid rgba(201,168,76,0.1)", background:"rgba(6,6,5,0.95)", backdropFilter:"blur(24px)" }}>
        <div style={{ display:"flex", alignItems:"center", justifyContent:"space-between", padding:"0 32px", height:60 }}>
          <div style={{ display:"flex", alignItems:"center", gap:16 }}>
            <svg width="34" height="34" viewBox="0 0 34 34"><polygon points="17,2 32,10 32,24 17,32 2,24 2,10" fill="none" stroke="#C9A84C" strokeWidth="1.2"/><polygon points="17,9 26,14 26,20 17,25 8,20 8,14" fill="rgba(201,168,76,0.1)" stroke="#C9A84C" strokeWidth="0.5"/><text x="17" y="19.5" textAnchor="middle" fontSize="8.5" fontFamily="'DM Mono',monospace" fontWeight="700" fill="#C9A84C">IQ</text></svg>
            <div>
              <div style={{ fontFamily:"'Bebas Neue',cursive", fontSize:22, letterSpacing:"0.2em", color:"#C9A84C", lineHeight:1 }}>PROP<span style={{ color:"#E8E0D0" }}>IQ</span></div>
              <div style={{ fontSize:7, letterSpacing:"0.4em", color:"rgba(201,168,76,0.35)", marginTop:1 }}>UAE SOVEREIGN INTELLIGENCE</div>
            </div>
          </div>
          <div style={{ display:"flex", gap:22, alignItems:"center" }}>
            {[["#00E5A0","LANGGRAPH"],["#00E5A0","GPT-4O"],["#00E5A0","GROQ 70B"],["#00E5A0","SUPABASE"],["#00E5A0","TAVILY"]].map(([dot,lbl],i)=>(<div key={i} style={{ display:"flex", alignItems:"center", gap:5 }}><div style={{ width:5, height:5, borderRadius:"50%", background:dot, boxShadow:`0 0 6px ${dot}` }}/><span style={{ fontSize:8, letterSpacing:"0.14em", color:"rgba(255,255,255,0.26)" }}>{lbl}</span></div>))}
          </div>
          <div style={{ display:"flex", gap:14, alignItems:"center" }}>
            <span style={{ fontSize:8, color:"rgba(255,255,255,0.18)", letterSpacing:"0.12em" }}>DLD FEED ◆ LIVE</span>
            <div style={{ padding:"4px 12px", border:"1px solid rgba(201,168,76,0.3)", fontSize:10, letterSpacing:"0.2em", color:"#C9A84C" }}>v1.0 PROD</div>
          </div>
        </div>
        <LiveTicker speed={tickerSpd}/>
      </header>

      {phase === "idle" && (
        <div style={{ position:"relative", zIndex:2, maxWidth:680, margin:"0 auto", padding:"68px 24px 40px", animation:"fadeIn 0.7s ease both" }}>
          <div style={{ textAlign:"center", marginBottom:54, animation:"heroFloat 4s ease-in-out infinite" }}>
            <div style={{ fontSize:10, letterSpacing:"0.5em", color:"rgba(201,168,76,0.45)", marginBottom:20 }}>DEPLOYING MULTI-AGENT INTELLIGENCE</div>
            <h1 style={{ fontFamily:"'Bebas Neue',cursive", fontSize:"clamp(60px,11vw,104px)", lineHeight:0.9, letterSpacing:"0.02em", color:"#E8E0D0", marginBottom:24 }}>INVESTMENT<br/><span style={{ color:"#C9A84C", textShadow:"0 0 40px rgba(201,168,76,0.4)" }}>VERDICT</span><br/>IN 4 SECONDS</h1>
            <p style={{ fontSize:12, color:"rgba(232,224,208,0.3)", lineHeight:1.9, maxWidth:440, margin:"0 auto" }}>6 agents. XGBoost DLD. GPT-4o vision. Live market data.<br/>One institutional-grade decision. No compromises.</p>
          </div>

          <div style={{ border:`1px solid ${focus?"rgba(201,168,76,0.55)":"rgba(201,168,76,0.14)"}`, background:"rgba(8,8,7,0.96)", padding:"26px", transition:"border-color 0.3s", marginBottom:14, position:"relative", overflow:"hidden", animation:"glowPulse 3.5s ease infinite" }}>
            <div style={{ position:"absolute", top:0, left:0, right:0, height:1, background:"linear-gradient(90deg,transparent,rgba(201,168,76,0.55),transparent)" }}/>
            <div style={{ fontSize:10, letterSpacing:"0.24em", color:"rgba(201,168,76,0.4)", marginBottom:14 }}>◈ DEPLOY INVESTMENT QUERY</div>
            <textarea value={query} onChange={e=>setQuery(e.target.value)} onFocus={()=>setFocus(true)} onBlur={()=>setFocus(false)} rows={3} placeholder="e.g. 3BR villa Palm Jumeirah under AED 8M ready to move..." style={{ width:"100%", background:"transparent", border:"none", color:"#E8E0D0", fontSize:15, resize:"none", fontFamily:"'DM Mono',monospace", lineHeight:1.7 }}/>
          </div>

          <div style={{ marginBottom:14 }}><ImageDrop onImage={setPreview} preview={preview}/></div>

          <button onClick={runAnalysis} style={{ width:"100%", padding:"20px", position:"relative", overflow:"hidden", background:"rgba(0,229,160,0.08)", border:"1.5px solid rgba(0,229,160,0.5)", color:"#00E5A0", fontSize:12, letterSpacing:"0.45em", fontFamily:"'DM Mono',monospace", fontWeight:700, cursor:"pointer", transition:"all 0.3s", boxShadow:"0 0 35px rgba(0,229,160,0.1)" }} onMouseEnter={e=>{e.currentTarget.style.background="rgba(0,229,160,0.14)";e.currentTarget.style.boxShadow="0 0 65px rgba(0,229,160,0.25)";}} onMouseLeave={e=>{e.currentTarget.style.background="rgba(0,229,160,0.08)";e.currentTarget.style.boxShadow="0 0 35px rgba(0,229,160,0.1)";}}>
            {ripples.map(rp => (<span key={rp.id} style={{ position:"absolute", width:40, height:40, borderRadius:"50%", background:"rgba(0,229,160,0.3)", left:rp.x-20, top:rp.y-20, animation:"rippleOut 0.7s ease both", pointerEvents:"none" }}/>))}
            ▶  INITIATE SOVEREIGN ANALYSIS
          </button>

          <div style={{ display:"flex", gap:8, flexWrap:"wrap", justifyContent:"center", marginTop:34 }}>
            {["LangGraph","Groq LLaMA-70B","GPT-4o Vision","XGBoost DLD","Supabase pgvector","Tavily Live","ReportLab PDF"].map((s,i)=>(<span key={i} style={{ padding:"5px 13px", border:"1px solid rgba(255,255,255,0.07)", fontSize:8.5, color:"rgba(255,255,255,0.2)", letterSpacing:"0.1em", transition:"all 0.2s" }}>{s}</span>))}
          </div>
        </div>
      )}

      {phase === "processing" && (
        <div style={{ position:"relative", zIndex:2, maxWidth:940, margin:"0 auto", padding:"48px 24px", animation:"fadeIn 0.4s ease both" }}>
          <div style={{ textAlign:"center", marginBottom:40 }}>
            <div style={{ fontSize:10, letterSpacing:"0.42em", color:"rgba(201,168,76,0.45)", marginBottom:10 }}>◆ ACCELERATING DECISION INTELLIGENCE</div>
            <div style={{ fontFamily:"'Bebas Neue',cursive", fontSize:42, color:"#C9A84C", letterSpacing:"0.08em", textShadow:"0 0 30px rgba(201,168,76,0.3)" }}>SYNTHESISING INTELLIGENCE</div>
          </div>
          <div style={{ display:"flex", gap:8, marginBottom:22 }}>
            {AGENTS.map((a,i)=><AgentCard key={a.id} agent={a} status={agentSt[a.id]||"idle"} index={i}/>)}
          </div>
          <div style={{ display:"flex", alignItems:"center", padding:"0 24px", marginBottom:28 }}>
            {AGENTS.map((a,i)=>(
              <div key={a.id} style={{ display:"flex", alignItems:"center", flex:i<AGENTS.length-1?1:"none" }}>
                <div style={{ width:9, height:9, borderRadius:"50%", background:agentSt[a.id]==="done"?a.color:"rgba(255,255,255,0.1)", boxShadow:agentSt[a.id]==="done"?`0 0 10px ${a.color}`:"none", transition:"all 0.4s", flexShrink:0 }}/>
                {i<AGENTS.length-1 && (
                  <div style={{ flex:1, height:1, position:"relative", overflow:"hidden" }}><div style={{ position:"absolute", inset:0, background:"rgba(255,255,255,0.05)" }}/><div style={{ position:"absolute", inset:0, background:`linear-gradient(90deg,${a.color},${AGENTS[i+1].color})`, transform:`scaleX(${agentSt[a.id]==="done"?1:0})`, transformOrigin:"left", transition:"transform 0.6s cubic-bezier(0.4,0,0.2,1)" }}/></div>
                )}
              </div>
            ))}
          </div>
          <ThoughtLog entries={log} running={true}/>
        </div>
      )}

      {phase === "result" && result && (
        <div style={{ position:"relative", zIndex:2, maxWidth:1140, margin:"0 auto", padding:"38px 24px 64px", animation:"fadeIn 0.4s ease both" }}>
          <div style={{ display:"flex", alignItems:"center", justifyContent:"space-between", marginBottom:28 }}>
            <div>
              <div style={{ fontSize:10, letterSpacing:"0.32em", color:"rgba(201,168,76,0.4)", marginBottom:5 }}>★ INVESTMENT INTELLIGENCE REPORT — VERDICT DELIVERED</div>
              <div style={{ fontFamily:"'Bebas Neue',cursive", fontSize:30, color:"#E8E0D0", letterSpacing:"0.06em" }}>{query.length>60?query.slice(0,60)+"...":query}</div>
            </div>
            <button onClick={reset} style={{ padding:"9px 22px", border:"1px solid rgba(255,255,255,0.1)", background:"transparent", color:"rgba(255,255,255,0.28)", fontSize:9, letterSpacing:"0.2em", fontFamily:"'DM Mono',monospace", cursor:"pointer", transition:"all 0.2s" }} onMouseEnter={e=>{e.currentTarget.style.borderColor="rgba(0,229,160,0.4)";e.currentTarget.style.color="rgba(0,229,160,0.7)";}} onMouseLeave={e=>{e.currentTarget.style.borderColor="rgba(255,255,255,0.1)";e.currentTarget.style.color="rgba(255,255,255,0.28)";}}>↩  DEPLOY NEW QUERY</button>
          </div>

          <div style={{ display:"grid", gridTemplateColumns:"370px 1fr", gap:16, marginBottom:16 }}>
            <div style={{ display:"flex", flexDirection:"column", gap:12 }}>
              <GradeReveal grade={result.grade} active={gradeGo}/>
              {result.goldenVisa && (
                <div style={{ padding:"13px 16px", background:"rgba(0,229,160,0.04)", border:"1px solid rgba(0,229,160,0.2)", display:"flex", alignItems:"center", gap:12, animation:"slideUp 0.5s ease 0.3s both" }}>
                  <div style={{ width:8, height:8, borderRadius:"50%", background:"#00E5A0", boxShadow:"0 0 10px #00E5A0", flexShrink:0 }}/>
                  <div>
                    <div style={{ fontSize:9, color:"rgba(0,229,160,0.9)", letterSpacing:"0.15em", fontWeight:700 }}>GOLDEN VISA — RESIDENCY ACTIVATED</div>
                    <div style={{ fontSize:8, color:"rgba(0,229,160,0.5)", marginTop:2 }}>AED 2M threshold breached · 10-year UAE residency permit</div>
                  </div>
                </div>
              )}
              <div style={{ border:"1px solid rgba(255,255,255,0.07)", background:"rgba(6,6,5,0.85)", padding:"18px", animation:"slideUp 0.5s ease 0.4s both" }}>
                <div style={{ fontSize:10, letterSpacing:"0.22em", color:"rgba(201,168,76,0.38)", marginBottom:12 }}>⬟ LEGAL / COMPLIANCE MATRIX</div>
                {[["DLD Transfer (4%)",`AED ${result.dldFee?.toLocaleString()}`,"#C9A84C"],["Commission (2%)",`AED ${result.commission?.toLocaleString()}`,"#C9A84C"],["Risk Flags","ZERO DETECTED","#00E5A0"],["RERA Status","VERIFY DEVELOPER","#FBBF24"]].map(([l,v,col],i)=>(
                  <div key={i} style={{ display:"flex", justifyContent:"space-between", padding:"8px 0", borderBottom:"1px solid rgba(255,255,255,0.04)" }}><span style={{ fontSize:9, color:"rgba(255,255,255,0.3)" }}>{l}</span><span style={{ fontSize:9, color:col, fontWeight:700 }}>{v}</span></div>
                ))}
              </div>
            </div>

            <div style={{ display:"flex", flexDirection:"column", gap:12 }}>
              <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:10 }}>
                <StatCard label="BASE VALUATION"  value={`AED ${(baseC/1e6).toFixed(2)}M`}      sub="XGBoost DLD · 10K records"  delay={0.1}/>
                <StatCard label="ADJUSTED PRICE"  value={`AED ${(adjC/1e6).toFixed(2)}M`}       sub={`×${result.multiplier} luxury`} accent delay={0.15}/>
                <StatCard label="ROI PROJECTION"  value={`${(roiC/10).toFixed(1)}%`}             sub="Market avg 6.2% · +220bps"  teal delay={0.2}/>
                <StatCard label="DLD FEE"         value={`AED ${dldC.toLocaleString()}`}         sub="4% statutory transfer"      delay={0.25}/>
              </div>

              <div style={{ padding:"22px", background:"rgba(201,168,76,0.02)", border:"1px solid rgba(201,168,76,0.1)", animation:"slideUp 0.5s ease 0.3s both" }}>
                {result.outOfMarket && (
                  <div style={{ padding:"12px 16px", background:"rgba(251,191,36,0.08)", border:"1px solid rgba(251,191,36,0.4)", color:"#FBBF24", fontSize:9, letterSpacing:"0.15em", marginBottom:12, animation:"slideUp 0.5s ease 0.25s both", display:"flex", alignItems:"center", gap:10, fontWeight:700 }}>
                    <span style={{ fontSize: 12 }}>⚠️</span> OUT-OF-MARKET GEOGRAPHY WARNING
                  </div>
                )}
                <div style={{ fontSize:10, letterSpacing:"0.24em", color:"rgba(201,168,76,0.38)", marginBottom:13 }}>★ EXECUTIVE SYNTHESIS — SUPERVISOR AI</div>
                <p style={{ fontSize:12.5, lineHeight:1.95, color:"rgba(232,224,208,0.68)" }}>{result.summary}</p>
                <div style={{ marginTop:15, padding:"10px 14px", background:"rgba(255,68,68,0.04)", border:"1px solid rgba(255,68,68,0.14)", display:"flex", gap:10, alignItems:"center" }}>
                  <span style={{ fontSize:8.5, color:"rgba(255,107,107,0.5)", letterSpacing:"0.12em", flexShrink:0 }}>EXPOSURE:</span>
                  <span style={{ fontSize:8.5, color:"rgba(255,107,107,0.82)", fontStyle:"italic" }}>{result.topRisk}</span>
                </div>
              </div>

              <div style={{ border:"1px solid rgba(255,255,255,0.07)", background:"rgba(6,6,5,0.85)", padding:"18px", animation:"slideUp 0.5s ease 0.4s both" }}>
                <div style={{ fontSize:10, letterSpacing:"0.22em", color:"rgba(201,168,76,0.38)", marginBottom:4 }}>◉ LIVE COMPARABLES — MARKET SCAN</div>
                <div style={{ fontSize:7.5, color:"rgba(255,255,255,0.18)", marginBottom:14, letterSpacing:"0.1em" }}>BAYUT · PROPERTYFINDER — TAVILY LIVE INTELLIGENCE</div>
                {result.listings?.map((l,i)=>{
                  const pos = l.delta>=0;
                  return (
                    <div key={i} style={{ display:"grid", gridTemplateColumns:"1fr auto auto", gap:14, padding:"11px 0", borderBottom:"1px solid rgba(255,255,255,0.04)", alignItems:"center", animation:`slideUp 0.4s ease ${0.5+i*0.08}s both` }}>
                      <div>
                        <div style={{ fontSize:11, color:"rgba(232,224,208,0.75)" }}>{l.name}</div>
                        <div style={{ fontSize:8, color:"rgba(255,255,255,0.22)", marginTop:2, letterSpacing:"0.08em" }}>{l.src}</div>
                      </div>
                      <div style={{ fontSize:12, color:"#C9A84C", fontWeight:700 }}>AED {(l.price/1e6).toFixed(2)}M</div>
                      <div style={{ fontSize:9.5, color:pos?"rgba(255,107,107,0.85)":"rgba(0,229,160,0.85)", fontWeight:700, minWidth:46, textAlign:"right" }}>{pos?"+":""}{l.delta}%</div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

          <div style={{ marginBottom:16 }}><ThoughtLog entries={log} running={false}/></div>

          <button onClick={downloadPDF} style={{ width:"100%", padding:"19px", background:"rgba(201,168,76,0.07)", border:"1.5px solid rgba(201,168,76,0.45)", color:"#C9A84C", fontSize:11, letterSpacing:"0.42em", fontFamily:"'DM Mono',monospace", fontWeight:700, cursor:"pointer", transition:"all 0.3s" }} onMouseEnter={e=>{e.currentTarget.style.background="rgba(201,168,76,0.13)";e.currentTarget.style.boxShadow="0 0 50px rgba(201,168,76,0.2)";}} onMouseLeave={e=>{e.currentTarget.style.background="rgba(201,168,76,0.07)";e.currentTarget.style.boxShadow="none";}}>↓  FORGE INSTITUTIONAL PDF DOSSIER  —  REPORTLAB</button>
        </div>
      )}

      <LiveTicker speed={tickerSpd}/>
    </div>
  );
}