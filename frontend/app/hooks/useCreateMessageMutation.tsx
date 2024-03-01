import { useMutation } from "@tanstack/react-query"
import axios from "axios"

export default function useCreateMessageMutation(chatId: string | undefined) {
  const { mutate } = useMutation({
    mutationKey: ["chat-messages", chatId],
    mutationFn: async ({ message, to_id }: { message: string, to_id: string }) => {
      const res = await axios.post(`http://localhost:8000/message/`, {
        to_id,
        message
      }, { withCredentials: true })
      return res.data
    }
  })

  return mutate
}