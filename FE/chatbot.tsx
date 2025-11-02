"use client";

import React, { useEffect, useRef, useState } from "react";
import "./chatbot.css";
import io, { Socket } from "socket.io-client";
import axios from "axios";

type Conversation = {
	_id: string;
	title: string;
};

type Message = {
	_id?: string;
	text: string;
	sender: "user" | "system";
};

export default function Chatbot() {
	const [socket, setSocket] = useState<Socket | null>(null);
	const [conversationId, setConversationId] = useState<string | null>(null);
	const [currentTitle, setCurrentTitle] = useState<string | null>(null);
	const [conversations, setConversations] = useState<Conversation[]>([]);
	const [messages, setMessages] = useState<Message[]>([]);
	const [msgInput, setMsgInput] = useState("");
	const [isThinking, setIsThinking] = useState(false);
	const [currentTheme, setCurrentTheme] = useState<"dark" | "light">("dark");
	const chatBoxRef = useRef<HTMLUListElement>(null);
	const fileInputRef = useRef<HTMLInputElement>(null);

	// Initialize socket connection
	useEffect(() => {
		const newSocket = io("http://localhost:8080");
		setSocket(newSocket);

		newSocket.on("connect", () => {
			console.log("✅ Socket connected:", newSocket.id);
		});

		newSocket.on("receive_message", (data: { text: string }) => {
			console.log("📩 Tin nhắn từ server:", data.text);
			setIsThinking(false);
			addMessage(data.text, "system");
		});

		newSocket.on("error", (data: { message: string }) => {
			console.log("❌ Lỗi từ server:", data.message);
			alert(data.message);
		});

		return () => {
			newSocket.close();
		};
	}, []);

	// Load theme from localStorage
	useEffect(() => {
		const savedTheme = localStorage.getItem("theme") as "dark" | "light" | null;
		if (savedTheme) {
			setCurrentTheme(savedTheme);
			document.documentElement.setAttribute("data-theme", savedTheme);
		}
	}, []);

	// Load conversations on mount
	useEffect(() => {
		loadConversations();
	}, []);

	// Auto-scroll chat box
	useEffect(() => {
		if (chatBoxRef.current) {
			chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
		}
	}, [messages, isThinking]);

	const loadConversations = () => {
		axios
			.get("http://localhost:8080/api/conversations")
			.then((res) => {
				setConversations(res.data.data.conversations);
			})
			.catch((err) => {
				console.error("❌ Lỗi tải conversations:", err);
			});
	};

	const selectConversation = (conv: Conversation) => {
		setConversationId(conv._id);
		setCurrentTitle(conv.title);
		setMessages([]);

		socket?.emit("join_room", conv._id);

		// Load messages
		axios
			.get(`http://localhost:8080/api/messages/${conv._id}`)
			.then((res) => {
				setMessages(res.data.data.messages);
			})
			.catch((err) => {
				console.error("Lỗi tải messages:", err);
			});
	};

	const createConversation = () => {
		const title = prompt("Nhập tiêu đề cuộc trò chuyện:");
		if (!title) return;

		axios
			.post("http://localhost:8080/api/conversations", { title })
			.then((res) => {
				const { conversation } = res.data.data;
				loadConversations();
				selectConversation(conversation);
			})
			.catch((err) => {
				console.error("❌ Lỗi tạo conversation:", err);
				alert("Không thể tạo cuộc trò chuyện mới!");
			});
	};

	const addMessage = (text: string, sender: "user" | "system") => {
		setMessages((prev) => [...prev, { text, sender }]);
	};

	const sendMsg = () => {
		const text = msgInput.trim();
		if (!text) return;
		if (!conversationId) {
			alert("Hãy chọn một cuộc trò chuyện trước!");
			return;
		}

		addMessage(text, "user");
		setMsgInput("");
		setIsThinking(true);

		socket?.emit("send_message", { conversationId, text });
	};

	const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
		if (e.key === "Enter" && !e.shiftKey) {
			e.preventDefault();
			sendMsg();
		}
	};

	const toggleTheme = () => {
		const newTheme = currentTheme === "dark" ? "light" : "dark";
		setCurrentTheme(newTheme);
		document.documentElement.setAttribute("data-theme", newTheme);
		localStorage.setItem("theme", newTheme);
	};

	const handleFileImport = (e: React.ChangeEvent<HTMLInputElement>) => {
		const file = e.target.files?.[0];
		if (!file) return;

		const reader = new FileReader();
		reader.onload = (event) => {
			const content = event.target?.result as string;
			setMsgInput(`[File: ${file.name}]\n${content.substring(0, 500)}...`);
		};
		reader.readAsText(file);
	};

	const handleFigmaButton = async () => {
		if (!conversationId) {
			alert("Vui lòng chọn một cuộc trò chuyện trước!");
			return;
		}

		try {
			const res = await axios.post(
				`http://localhost:8080/api/conversations/${conversationId}/figma-layout`
			);
			console.log("🎨 Figma layout response:", res.data);
			alert("Layout Figma đã được tạo thành công! Kiểm tra console để xem JSON layout.");
		} catch (err) {
			console.error("Lỗi khi tạo layout Figma:", err);
			alert("⚠️Không thể tạo layout Figma!");
		}
	};

	const escapeHtml = (text: string) => {
		const map: { [key: string]: string } = {
			"&": "&amp;",
			"<": "&lt;",
			">": "&gt;",
			'"': "&quot;",
			"'": "&#039;",
		};
		return text.replace(/[&<>"']/g, (m) => map[m]);
	};

	const formatMessage = (text: string) => {
		const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;

		return text.replace(codeBlockRegex, (_match, language, code) => {
			const lang = language || "text";
			return `<div class="code-block-container">
                <div class="code-block-header">
                    <span class="code-language">${lang}</span>
                    <button class="copy-btn" onclick="navigator.clipboard.writeText(\`${escapeHtml(
											code.trim()
										)}\`).then(() => { this.textContent='✓ Copied!'; this.classList.add('copied'); setTimeout(() => { this.textContent='📋 Copy'; this.classList.remove('copied'); }, 2000); })">📋 Copy</button>
                </div>
                <div class="code-content">
                    <pre><code>${escapeHtml(code.trim())}</code></pre>
                </div>
            </div>`;
		});
	};

	return (
		<div className="body-wrapper">
			<div className="container">
				{/* Sidebar */}
				<div className="sidebar">
					<div className="sidebar-header">AI Function 200</div>
					<button className="new-btn" onClick={createConversation}>
						New Chat
					</button>
					<div className="conversation-list">
						{conversations.map((conv) => (
							<div
								key={conv._id}
								className={`conversation-item ${conversationId === conv._id ? "active" : ""}`}
								onClick={() => selectConversation(conv)}
							>
								{conv.title}
							</div>
						))}
					</div>
				</div>

				{/* Chat Area */}
				<div className="chat-area">
					<div className="chat-header">
						<span id="chatTitle">
							{currentTitle || "Select a chat or create a new chat to begin"}
						</span>
						<div style={{ display: "flex", gap: "10px", alignItems: "center" }}>
							{conversationId && (
								<button id="figmaBtn" onClick={handleFigmaButton}>
									Generate Layout
								</button>
							)}
						</div>
						<button id="themeToggle" onClick={toggleTheme}>
							{currentTheme === "dark" ? "🌙 Dark" : "☀️ Light"}
						</button>
					</div>

					<ul id="chat" className="chat-box" ref={chatBoxRef}>
						{messages.map((m, idx) => (
							<li
								key={idx}
								className={m.sender}
								dangerouslySetInnerHTML={
									m.sender === "system"
										? { __html: formatMessage(m.text) }
										: undefined
								}
							>
								{m.sender !== "system" && m.text}
							</li>
						))}
						{isThinking && (
							<li className="system thinking-message">
								<span>🤖 AI đang suy nghĩ</span>
								<div className="thinking-dots">
									<span></span>
									<span></span>
									<span></span>
								</div>
							</li>
						)}
					</ul>

					<div className="chat-input">
						<input
							type="file"
							ref={fileInputRef}
							style={{ display: "none" }}
							accept=".txt,.pdf,.doc,.docx,.json"
							onChange={handleFileImport}
						/>
						<button className="import-btn" onClick={() => fileInputRef.current?.click()}>
							➕ Import
						</button>
						<input
							id="msg"
							type="text"
							placeholder="Type your message..."
							value={msgInput}
							onChange={(e) => setMsgInput(e.target.value)}
							onKeyDown={handleKeyDown}
							disabled={!conversationId}
						/>
						<button onClick={sendMsg}>➤ Send</button>
					</div>
				</div>
			</div>
		</div>
	);
}
