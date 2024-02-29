import { useNavigate } from "@remix-run/react"
import { useEffect } from "react"

export default function ChatIndex() {
  const navigate = useNavigate()
  useEffect(() => navigate('/chats'), [navigate])
  return <></>
}