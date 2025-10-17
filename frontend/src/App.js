import React, { useState } from "react";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState(null); // <-- Added to store session_id

  const send = async () => {
    if (!input.trim()) return;
    const user = input;
    setMessages((m) => [...m, { sender: "You", text: user }]);
    setInput("");

    try {
      // Build the backend URL
      let url = "http://127.0.0.1:8000/chat";
      if (sessionId) {
        // Append session_id as query param if exists
        url += `?session_id=${sessionId}`;
      }

      const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: user }),
      });

      const data = await res.json();

      // Store session_id from first response automatically
      if (!sessionId && data.session_id) {
        setSessionId(data.session_id);
      }

      setMessages((m) => [
        ...m,
        { sender: "Bot", text: data.answer }
      ]);
    } catch (err) {
      setMessages((m) => [...m, { sender: "Bot", text: "Error: " + err.message }]);
    }
  };

  return (
    <div style={{ maxWidth: 700, margin: "24px auto", fontFamily: "Arial" }}>
      <h2>Smart AI Chatbot (RAG + Llama2)</h2>
      <div style={{ border: "1px solid #ddd", padding: 12, height: 420, overflowY: "auto" }}>
        {messages.map((m, i) => (
          <div key={i} style={{ textAlign: m.sender === "You" ? "right" : "left", margin: "8px 0" }}>
            <strong>{m.sender}:</strong> {m.text}
          </div>
        ))}
      </div>
      <div style={{ marginTop: 10 }}>
        <input
          style={{ width: "78%", padding: 8 }}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask something..."
          onKeyDown={(e) => e.key === "Enter" && send()}
        />
        <button style={{ width: "20%", padding: 8 }} onClick={send}>Send</button>
      </div>
    </div>
  );
}

export default App;
