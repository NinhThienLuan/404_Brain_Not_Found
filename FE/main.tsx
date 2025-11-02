import React from 'react'
import ReactDOM from 'react-dom/client'
import Chatbot from './chatbot.tsx'
import './chatbot.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Chatbot />
  </React.StrictMode>,
)

