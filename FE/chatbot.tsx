"use client";

import React, { useEffect, useRef, useState } from "react";
import "./chatbot.css";
import axios from "axios";

// Backend API URL
const API_BASE_URL = "http://localhost:8000";

type Conversation = {
	id: string;
	title: string;
	createdAt: string;
};

type Message = {
	id: string;
	text: string;
	sender: "user" | "system";
	timestamp: string;
};

export default function Chatbot() {
	const [conversationId, setConversationId] = useState<string | null>(null);
	const [currentTitle, setCurrentTitle] = useState<string | null>(null);
	const [conversations, setConversations] = useState<Conversation[]>([]);
	const [messages, setMessages] = useState<Message[]>([]);
	const [msgInput, setMsgInput] = useState("");
	const [isThinking, setIsThinking] = useState(false);
	const [currentTheme, setCurrentTheme] = useState<"dark" | "light">("dark");
	const [agentSessionId, setAgentSessionId] = useState<string | null>(null);
	const [useAgentMode, setUseAgentMode] = useState(true);
	const chatBoxRef = useRef<HTMLUListElement>(null);
	const fileInputRef = useRef<HTMLInputElement>(null);
	const messageInputRef = useRef<HTMLInputElement>(null);

	// Load conversations from localStorage
	useEffect(() => {
		loadConversationsFromStorage();
	}, []);

	// Create Agent Session on mount
	useEffect(() => {
		const createAgentSession = async () => {
			try {
				const userId = localStorage.getItem("userId") || `user_${Date.now()}`;
				localStorage.setItem("userId", userId);
				
				const response = await axios.post(`${API_BASE_URL}/agent/session/create`, {
					user_id: userId,
					metadata: { source: "frontend_chatbot" }
				});
				
				setAgentSessionId(response.data.session_id);
				console.log("✅ Agent session created:", response.data.session_id);
			} catch (err) {
				console.error("❌ Error creating agent session:", err);
				setUseAgentMode(false); // Fallback to direct AI mode
			}
		};
		
		if (useAgentMode) {
			createAgentSession();
		}
	}, []);

	// Load theme from localStorage
	useEffect(() => {
		const savedTheme = localStorage.getItem("theme") as "dark" | "light" | null;
		if (savedTheme) {
			setCurrentTheme(savedTheme);
			document.documentElement.setAttribute("data-theme", savedTheme);
		}
	}, []);

	// Auto-scroll chat box
	useEffect(() => {
		if (chatBoxRef.current) {
			chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
		}
	}, [messages, isThinking]);

	// Save to localStorage whenever conversations or messages change
	useEffect(() => {
		if (conversations.length > 0) {
			localStorage.setItem("conversations", JSON.stringify(conversations));
		}
	}, [conversations]);

	useEffect(() => {
		if (conversationId && messages.length > 0) {
			localStorage.setItem(`messages_${conversationId}`, JSON.stringify(messages));
		}
	}, [messages, conversationId]);

	const loadConversationsFromStorage = () => {
		const saved = localStorage.getItem("conversations");
		if (saved) {
			try {
				const parsed = JSON.parse(saved);
				setConversations(parsed);
			} catch (err) {
				console.error("❌ Lỗi parse conversations:", err);
				setConversations([]);
			}
		}
	};

	const selectConversation = (conv: Conversation) => {
		setConversationId(conv.id);
		setCurrentTitle(conv.title);

		// Load messages from localStorage
		const savedMessages = localStorage.getItem(`messages_${conv.id}`);
		if (savedMessages) {
			try {
				const parsed = JSON.parse(savedMessages);
				setMessages(parsed);
			} catch (err) {
				console.error("❌ Lỗi parse messages:", err);
				setMessages([]);
			}
		} else {
			setMessages([]);
		}
	};

	const createConversation = () => {
		const title = prompt("Nhập tiêu đề cuộc trò chuyện:");
		if (!title || !title.trim()) return;

		const newConv: Conversation = {
			id: `conv_${Date.now()}`,
			title: title.trim(),
			createdAt: new Date().toISOString(),
		};

		setConversations((prev) => [newConv, ...prev]);
		selectConversation(newConv);
	};

	const addMessage = (text: string, sender: "user" | "system") => {
		const newMsg: Message = {
			id: `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
			text,
			sender,
			timestamp: new Date().toISOString(),
		};
		setMessages((prev) => [...prev, newMsg]);
	};

	const sendMsg = async () => {
		const text = msgInput.trim();
		if (!text) return;
		if (!conversationId) {
			alert("Hãy chọn một cuộc trò chuyện trước!");
			return;
		}

		// Add user message
		addMessage(text, "user");
		setMsgInput("");
		setIsThinking(true);

		try {
			// Detect if text starts with /context command
			if (text.toLowerCase().startsWith("/context ")) {
				// Parse context mode (F1)
				await parseContext(text.substring(9));
				return;
			} else if (text.toLowerCase() === "/analyze") {
				// Analyze code mode (F3)
				await analyzeCode();
				return;
			}

			// Use Agent Orchestration if available, otherwise fallback to direct AI
			if (useAgentMode && agentSessionId) {
				// Call Agent Orchestration API (F2)
				const userId = localStorage.getItem("userId") || "user_default";
				const response = await axios.post(`${API_BASE_URL}/agent/prompt/process`, {
					session_id: agentSessionId,
					user_id: userId,
					prompt: text,
					model: "gemini-2.5-flash",
				});

				if (response.data.success) {
					const intent = response.data.intent ? `🎯 Intent: ${response.data.intent}\n\n` : "";
					const aiResponse = `${intent}${response.data.generated_code ? `\`\`\`python\n${response.data.generated_code}\n\`\`\`` : response.data.message}`;
					addMessage(aiResponse, "system");
				} else {
					addMessage(`Lỗi: ${response.data.error_message}`, "system");
				}
			} else {
				// Fallback: Direct AI API
				const response = await axios.post(`${API_BASE_URL}/ai/generate`, {
					prompt: text,
					language: "python",
					model: "gemini-2.5-flash",
				});

				if (response.data.success) {
					const aiResponse = `${response.data.explanation}\n\n\`\`\`${response.data.language}\n${response.data.generated_code}\n\`\`\``;
					addMessage(aiResponse, "system");
				} else {
					addMessage(`Lỗi: ${response.data.error_message}`, "system");
				}
			}
		} catch (err: any) {
			console.error("❌ Lỗi gọi AI API:", err);
			const errorMsg = err.response?.data?.detail || err.message || "Không rõ lỗi";
			addMessage(`❌ Không thể kết nối đến AI: ${errorMsg}`, "system");
		} finally {
			setIsThinking(false);
			// Focus lại vào input sau khi gửi
			setTimeout(() => {
				messageInputRef.current?.focus();
			}, 100);
		}
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

	const parseContext = async (contextText: string) => {
		if (!agentSessionId) {
			addMessage("❌ Agent session chưa sẵn sàng!", "system");
			setIsThinking(false);
			return;
		}

		try {
			const response = await axios.post(
				`${API_BASE_URL}/agent/context/parse`,
				null,
				{
					params: {
						session_id: agentSessionId,
						context_text: contextText,
						model: "gemini-2.5-flash"
					}
				}
			);

			if (response.data.success) {
				const parsedJson = JSON.stringify(response.data.context_json, null, 2);
				const result = `✅ Context parsed! (Confidence: ${(response.data.confidence_score || 0) * 100}%)\n\n\`\`\`json\n${parsedJson}\n\`\`\``;
				addMessage(result, "system");
			} else {
				addMessage(`❌ Parse failed: ${response.data.error_message}`, "system");
			}
		} catch (err: any) {
			console.error("❌ Error parsing context:", err);
			addMessage(`❌ Error: ${err.message}`, "system");
		} finally {
			setIsThinking(false);
		}
	};

	const analyzeCode = async () => {
		if (!agentSessionId) {
			addMessage("❌ Agent session chưa sẵn sàng!", "system");
			setIsThinking(false);
			return;
		}

		try {
			const response = await axios.post(
				`${API_BASE_URL}/agent/code/analyze`,
				null,
				{ params: { session_id: agentSessionId } }
			);

			if (response.data.success) {
				addMessage(`📊 Code Analysis:\n\n${response.data.code_analysis}`, "system");
			} else {
				addMessage(`❌ Analysis failed: ${response.data.error_message}`, "system");
			}
		} catch (err: any) {
			console.error("❌ Error analyzing code:", err);
			addMessage(`❌ Error: ${err.message}`, "system");
		} finally {
			setIsThinking(false);
		}
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

	const handleCodeReview = async () => {
		if (!conversationId) {
			alert("❌ Vui lòng chọn một cuộc trò chuyện trước!");
			return;
		}

		const code = prompt("Nhập code để review:");
		if (!code || !code.trim()) return;

		const language = prompt("Nhập ngôn ngữ (python/javascript/java/...):", "python");
		if (!language) return;

		setIsThinking(true);
		addMessage(`Review code:\n\`\`\`${language}\n${code}\n\`\`\``, "user");

		try {
			const response = await axios.post(`${API_BASE_URL}/ai/review`, {
				code: code,
				language: language,
				review_type: "general",
				model: "gemini-1.5-flash",
			});

			if (response.data.success) {
				const review = response.data;
				let reviewText = `📊 **Code Review Result**\n\n`;
				reviewText += `**Score**: ${review.overall_score}/10\n\n`;
				reviewText += `**Summary**: ${review.summary}\n\n`;
				
				if (review.issues && review.issues.length > 0) {
					reviewText += `**Issues Found**:\n`;
					review.issues.forEach((issue: any, idx: number) => {
						reviewText += `${idx + 1}. [${issue.severity.toUpperCase()}] ${issue.description}\n`;
						reviewText += `   💡 Suggestion: ${issue.suggestion}\n\n`;
					});
				}

				if (review.improvements && review.improvements.length > 0) {
					reviewText += `**Improvements**:\n`;
					review.improvements.forEach((imp: string, idx: number) => {
						reviewText += `${idx + 1}. ${imp}\n`;
					});
				}

				addMessage(reviewText, "system");
			} else {
				addMessage(`Lỗi: ${response.data.error_message}`, "system");
			}
		} catch (err: any) {
			console.error("❌ Lỗi review code:", err);
			const errorMsg = err.response?.data?.detail || err.message || "Không rõ lỗi";
			addMessage(`❌ Không thể review code: ${errorMsg}`, "system");
		} finally {
			setIsThinking(false);
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
						{conversations.length === 0 && (
							<div style={{ padding: "20px", textAlign: "center", color: "#888" }}>
								Chưa có cuộc trò chuyện nào. <br />
								Bấm "New Chat" để bắt đầu!
							</div>
						)}
						{conversations.map((conv) => (
							<div
								key={conv.id}
								className={`conversation-item ${conversationId === conv.id ? "active" : ""}`}
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
						<div style={{ display: "flex", gap: "10px", alignItems: "center", marginLeft: "auto" }}>
							{conversationId && agentSessionId && (
								<button id="figmaBtn" onClick={() => analyzeCode()}>
									📊 Analyze Code
								</button>
							)}
							{conversationId && (
								<button 
									id="figmaBtn" 
									onClick={handleCodeReview}
									style={{ background: "linear-gradient(135deg, #10b981 0%, #059669 100%)" }}
								>
									🔍 Review Code
								</button>
							)}
							<button id="themeToggle" onClick={toggleTheme}>
								{currentTheme === "dark" ? "🌙 Dark" : "☀️ Light"}
							</button>
						</div>
					</div>

					<ul id="chat" className="chat-box" ref={chatBoxRef}>
						{messages.length === 0 && conversationId && (
							<div className="chatbot-empty" style={{ 
								textAlign: "center", 
								padding: "40px 20px", 
								color: "#888",
								fontSize: "14px",
								lineHeight: "1.8"
							}}>
								{agentSessionId ? (
									<>
										🤖 <strong>AI Agent Mode</strong> đã kích hoạt! <br /><br />
										💬 <strong>Gõ prompt</strong> để generate code<br />
										📝 <strong>/context &lt;text&gt;</strong> để parse context<br />
										📊 <strong>/analyze</strong> để phân tích code<br />
										🔍 Hoặc click <strong>Review Code</strong> để review<br /><br />
										<small style={{ color: "#666" }}>Session: {agentSessionId.substring(0, 8)}...</small>
									</>
								) : (
									<>
										👋 Xin chào! Tôi là AI Code Assistant. <br />
										Hãy hỏi tôi bất cứ điều gì về lập trình!
									</>
								)}
							</div>
						)}
						{messages.map((m) => {
						if (m.sender === "system") {
							return (
								<li
									key={m.id}
									className={m.sender}
									dangerouslySetInnerHTML={{ __html: formatMessage(m.text) }}
								/>
							);
						} else {
							return (
								<li key={m.id} className={m.sender}>
									{m.text}
								</li>
							);
						}
					})}
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
							ref={messageInputRef}
							type="text"
							placeholder="Ask AI to generate code..."
							value={msgInput}
							onChange={(e) => setMsgInput(e.target.value)}
					onKeyDown={handleKeyDown}
							disabled={!conversationId}
							autoComplete="off"
						/>
						<button 
							onClick={sendMsg}
							disabled={!conversationId || isThinking || msgInput.trim() === ""}
							title={!conversationId ? "Hãy chọn conversation trước" : "Gửi tin nhắn (hoặc bấm Enter)"}
						>
							➤ Send
				</button>
					</div>
				</div>
			</div>
		</div>
	);
}
