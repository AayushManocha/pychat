import { useQuery } from "@tanstack/react-query"
import axios from "axios"

export const useGetChatByIdService = (chatId: string | undefined) => {
  const { isLoading, isError, data } = useQuery({
    queryKey: ["chat", chatId],
    queryFn: async () => {
      const res = await axios.get(`http://localhost:8000/chat/${chatId}`, { withCredentials: true })
      console.log('res', res.data)
      return res
    },
  })

  return { isLoading, isError, data }
}