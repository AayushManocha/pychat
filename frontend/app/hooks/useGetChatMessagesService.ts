import { useQuery } from "@tanstack/react-query"
import axios from "axios"

export default function useGetChatMessagesService(chatId: string | undefined) {
  const { isLoading, isError, data } = useQuery({
    queryKey: ["chat-messages", chatId],
    queryFn: async () => {
      const res = await axios.get(`http://localhost:8000/chat/${chatId}/message`, { withCredentials: true })
      return res
    }
  })

  return { isLoading, isError, data }
}
