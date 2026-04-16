import { useState, useEffect } from "react";
import axios from "axios";
import { motion } from "framer-motion";


const API = "https://ai-code-reviewer-rbas.onrender.com";

export default function App() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState("");
  const [repo, setRepo] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [displayText, setDisplayText] = useState("");
  const [loading, setLoading] = useState(false);

  // ✨ Typing Effect
  useEffect(() => {
    let i = 0;
    setDisplayText("");
    if (answer) {
      const interval = setInterval(() => {
        setDisplayText(prev => prev + answer.charAt(i));
        i++;
        if (i >= answer.length) clearInterval(interval);
      }, 20);
      return () => clearInterval(interval);
    }
  }, [answer]);

  // ✅ SIGNUP
  const signup = async () => {
    try {
      const res = await fetch(`${API}/signup`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password })
      });

      const data = await res.json();
      console.log(data);

      if (res.ok) {
        alert("User created ✅");
      } else {
        alert("Signup failed ❌");
      }
    } catch (error) {
      console.error(error);
      alert("Server not responding ❌");
    }
  };

  // ✅ LOGIN
  const login = async () => {
    try {
      const res = await axios.post(`${API}/login`, { username, password });
      setToken(res.data.token);
      alert("Login success ✅");
    } catch (err) {
      console.error(err);
      alert("Login failed ❌");
    }
  };

  // ✅ ANALYZE
  const analyze = async () => {
    try {
      setLoading(true);
      await axios.post(
        `${API}/analyze`,
        { repo_url: repo },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert("Repo analyzed ✅");
      setLoading(false);
    } catch (err) {
      console.error(err);
      setLoading(false);
      alert("Analyze failed ❌");
    }
  };

  // ✅ ASK AI
  const ask = async () => {
    try {
      setLoading(true);
      const res = await axios.post(
        `${API}/ask`,
        { q: question },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setAnswer(res.data.answer);
      setLoading(false);
    } catch (err) {
      console.error(err);
      setLoading(false);
      alert("Ask failed ❌");
    }
  };

  return (
    <div style={styles.bg}>
      <motion.h1
        initial={{ opacity: 0, y: -40 }}
        animate={{ opacity: 1, y: 0 }}
        style={styles.title}
      >
        🚀 AI Code Reviewer
      </motion.h1>

      <div style={styles.container}>

        {/* AUTH */}
        <motion.div style={styles.card} whileHover={{ scale: 1.08 }}>
          <h2>🔐 Auth</h2>
          <input placeholder="Username" onChange={e=>setUsername(e.target.value)} />
          <input type="password" placeholder="Password" onChange={e=>setPassword(e.target.value)} />
          <button onClick={signup}>Signup</button>
          <button onClick={login}>Login</button>
        </motion.div>

        {/* ANALYZE */}
        <motion.div style={styles.card} whileHover={{ scale: 1.08 }}>
          <h2>📂 Analyze</h2>
          <input placeholder="GitHub Repo URL" onChange={e=>setRepo(e.target.value)} />
          <button onClick={analyze}>Analyze Repo</button>
        </motion.div>

        {/* ASK */}
        <motion.div style={styles.card} whileHover={{ scale: 1.08 }}>
          <h2>🤖 Ask AI</h2>
          <input placeholder="Ask something..." onChange={e=>setQuestion(e.target.value)} />
          <button onClick={ask}>Ask</button>

          {loading && <div style={styles.loader}></div>}

          {displayText && (
            <motion.div style={styles.answer} initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
              {displayText}
            </motion.div>
          )}
        </motion.div>

      </div>
    </div>
  );
}

const styles: any = {
  bg: {
    minHeight: "100vh",
    background: "radial-gradient(circle at top, #0f2027, #203a43, #2c5364)",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    paddingTop: "50px",
    color: "white"
  },
  title: {
    fontSize: "42px",
    marginBottom: "40px",
    textShadow: "0 0 20px #00f2ff"
  },
  container: {
    display: "flex",
    gap: "30px",
    flexWrap: "wrap",
    justifyContent: "center"
  },
  card: {
    background: "rgba(255,255,255,0.08)",
    backdropFilter: "blur(20px)",
    borderRadius: "20px",
    padding: "25px",
    width: "300px",
    display: "flex",
    flexDirection: "column",
    gap: "12px",
    boxShadow: "0 0 20px rgba(0,255,255,0.3)"
  },
  answer: {
    marginTop: "10px",
    background: "rgba(0,0,0,0.5)",
    padding: "12px",
    borderRadius: "10px",
    border: "1px solid #00f2ff"
  },
  loader: {
    width: "40px",
    height: "40px",
    border: "4px solid #00f2ff",
    borderTop: "4px solid transparent",
    borderRadius: "50%",
    animation: "spin 1s linear infinite",
    margin: "10px auto"
  }
};