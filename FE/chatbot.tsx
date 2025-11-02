import React, { useEffect, useRef, useState } from "react";
import "./chatbot.css";

type Sender = "user" | "bot" | "system";

type Message = {
	id: string;
	sender: Sender;
	text: string;
	time?: string;
};

type ChatbotProps = {
	// Optional backend endpoint. If not provided, component will echo messages locally.
	apiUrl?: string;
	title?: string;
};

function nowTime() {
	return new Date().toLocaleTimeString();
}

export default function Chatbot({ apiUrl, title = "Chatbot" }: ChatbotProps) {
	const [messages, setMessages] = useState<Message[]>([]);
	const [input, setInput] = useState("");
	const [loading, setLoading] = useState(false);
	const listRef = useRef<HTMLDivElement | null>(null);

	useEffect(() => {
		// Scroll to bottom on new message
		if (listRef.current) {
			listRef.current.scrollTop = listRef.current.scrollHeight;
		}
	}, [messages]);

	const postMessage = async (text: string) => {
		const id = String(Date.now()) + Math.random().toString(36).slice(2, 7);
		const userMsg: Message = { id, sender: "user", text, time: nowTime() };
		setMessages((m) => [...m, userMsg]);

		setLoading(true);
		try {
			if (apiUrl) {
				// Try to POST to backend and expect JSON { reply: string } or { message: string }
				const resp = await fetch(apiUrl, {
					method: "POST",
					headers: { "Content-Type": "application/json" },
					body: JSON.stringify({ message: text }),
				});
				if (!resp.ok) throw new Error(`Server returned ${resp.status}`);
				const data = await resp.json();
				const reply = data?.reply ?? data?.message ?? JSON.stringify(data);
				const botMsg: Message = { id: id + "-r", sender: "bot", text: String(reply), time: nowTime() };
				setMessages((m) => [...m, botMsg]);
			} else {
				// Local echo (demo)
				await new Promise((r) => setTimeout(r, 450));
				const botMsg: Message = { id: id + "-r", sender: "bot", text: `Echo: ${text}`, time: nowTime() };
				setMessages((m) => [...m, botMsg]);
			}
		} catch (err: any) {
			const errMsg: Message = { id: id + "-e", sender: "system", text: `Lỗi: ${err?.message ?? err}`, time: nowTime() };
			setMessages((m) => [...m, errMsg]);
		} finally {
			setLoading(false);
		}
	};

	const handleSend = () => {
		const text = input.trim();
		if (!text) return;
		setInput("");
		postMessage(text);
	};

	const handleKeyDown: React.KeyboardEventHandler<HTMLInputElement> = (e) => {
		if (e.key === "Enter" && !e.shiftKey) {
			e.preventDefault();
			handleSend();
		}
	};

	const clear = () => setMessages([]);

	return (
		<div className="chatbot-root">
			<div className="chatbot-header">
				<strong>{title}</strong>
				<div className="chatbot-actions">
					<button className="btn small" onClick={clear} title="Clear chat">
						Clear
					</button>
				</div>
			</div>

			<div className="chatbot-list" ref={listRef}>
				{messages.length === 0 && <div className="chatbot-empty">Chào! Gõ tin nhắn để bắt đầu.</div>}
				{messages.map((m) => (
					<div key={m.id} className={`chatbot-msg ${m.sender}`}> 
						<div className="meta">{m.sender === "user" ? "Bạn" : m.sender === "bot" ? "Bot" : "Hệ thống"} • {m.time}</div>
						<div className="text">{m.text}</div>
					</div>
				))}
				{loading && (
					<div className="chatbot-msg bot">
						<div className="meta">Bot • {nowTime()}</div>
						<div className="text">Đang trả lời...</div>
					</div>
				)}
			</div>

			<div className="chatbot-input">
				<input
					placeholder="Nhập tin nhắn..."
					value={input}
					onChange={(e) => setInput(e.target.value)}
					onKeyDown={handleKeyDown}
					aria-label="Chat input"
				/>
				<button className="btn" onClick={handleSend} disabled={loading || input.trim() === ""}>
					Gửi
				</button>
			</div>
			<div className="chatbot-footer">API: {apiUrl ?? "(offline - echo)"}</div>
		</div>
	);
}
