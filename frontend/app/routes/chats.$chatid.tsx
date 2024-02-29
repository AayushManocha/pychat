import { useParams } from "@remix-run/react"
import { useQuery } from "@tanstack/react-query"
import axios from "axios"

export default function ChatDetailPage() {
  const params = useParams()
  const chatId = params.chatid

  const { isLoading, isError, data } = useQuery({
    queryKey: ["chat", chatId],
    queryFn: async () => {
      const res = await axios.get(`http://localhost:8000/chat/${chatId}/message`, { withCredentials: true })
      return res
    }
  })

  if (isLoading) return <div>Loading...</div>
  if (isError) return <div>Error</div>

  return (
    <div>
      <h1>Chat {chatId}</h1>
      <ul>
        {data?.data.map((message: any) => {
          return (
            <li key={message.id}>{message.message}</li>
          )
        })}
      </ul>
    </div>
  )

}