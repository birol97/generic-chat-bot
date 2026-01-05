"use client";

import { useState } from "react";
import { askQuestion, imageUrl } from "@/lib/api";

type Evidence = {
  file: string;
  header_path?: string;
  content: string;
  images?: string[];
};

export default function Home() {
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState("");
  const [images, setImages] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  // PDF Upload State
  const [file, setFile] = useState<File | null>(null);
  const [uploadMsg, setUploadMsg] = useState("");

  async function send() {
    if (!input.trim() || loading) return;

    const question = input;
    setInput("");

    setMessages(m => [...m, { role: "user", text: question }]);
    setLoading(true);

    try {
      const data = await askQuestion(question);

      const imageSet = new Set<string>();
      (data.evidence || []).forEach((ev: Evidence) =>
        ev.images?.forEach(img => imageSet.add(img))
      );
      setImages([...imageSet]);

      setMessages(m => [
        ...m,
        {
          role: "bot",
          text: data.answer,
          evidence: data.evidence,
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  async function uploadPDF() {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:8000/ingest/pdf", {
        method: "POST",
        body: formData,
      });

      if (res.ok) {
        setUploadMsg("PDF uploaded and knowledge updated!");
        setFile(null);
      } else {
        const err = await res.text();
        setUploadMsg(`Error: ${err}`);
      }
    } catch (e) {
      setUploadMsg(`Error: ${e}`);
    }
  }

  return (
    <div className="container">
      <div className="layout">

        {/* CHAT */}
        <div className="chat-container">
          <header>Internal Knowledge Assistant</header>

          <div className="chat">
            {messages.map((m, i) => (
              <div key={i} className={`message ${m.role}`}>
                {m.text}

                {m.evidence && (
                  <div className="evidence">
                    <details>
                      <summary>Evidence ({m.evidence.length})</summary>
                      {m.evidence.map((ev: Evidence, j: number) => (
                        <div key={j} style={{ marginTop: 8 }}>
                          <b>{ev.file}</b><br />
                          <i>{ev.header_path}</i>
                          <pre>{ev.content}</pre>
                        </div>
                      ))}
                    </details>
                  </div>
                )}
              </div>
            ))}

            {loading && (
              <div className="message bot loading">Thinking…</div>
            )}
          </div>

          <footer>
            <input
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === "Enter" && send()}
              placeholder="Ask me about me…"
            />
            <button onClick={send}>Send</button>
          </footer>
        </div>

        {/* IMAGE PANEL */}
        <div className="image-panel">
          <h3>Related Images</h3>
          {images.map((img, i) => (
            <img
              key={i}
              src={imageUrl(img)}
              onClick={() => window.open(imageUrl(img))}
            />
          ))}
        </div>

        {/* PDF UPLOAD PANEL */}
        <div className="upload-panel" style={{ marginLeft: 16 }}>
          <h3>Update Knowledge Base</h3>
          <input
            type="file"
            accept=".pdf"
            onChange={e => e.target.files && setFile(e.target.files[0])}
          />
          <button onClick={uploadPDF} disabled={!file} style={{ marginLeft: 8 }}>
            Upload PDF
          </button>
          {uploadMsg && <p>{uploadMsg}</p>}
        </div>

      </div>
    </div>
  );
}
