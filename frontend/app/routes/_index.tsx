import { useNavigate } from "@remix-run/react"
import { useEffect } from "react"
import useAuthenticationGuard from "~/hooks/useAuthenticationGuard"

export default function ChatIndex() {
  useAuthenticationGuard()
  const navigate = useNavigate()
  useEffect(() => navigate('/chats'), [navigate])
  return <></>
}