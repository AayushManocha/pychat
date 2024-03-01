import { useParams } from "@remix-run/react"
import { set } from "node_modules/cypress/types/lodash"
import { useContext, useMemo, useState } from "react"
import useAuthenticationGuard from "~/hooks/useAuthenticationGuard"
import useCreateMessageMutation from "~/hooks/useCreateMessageMutation"
import { useGetChatByIdService } from "~/hooks/useGetChatByIdService"
import useGetChatMessagesService from "~/hooks/useGetChatMessagesService"
import { UserContext } from "~/root"

export default function ChatDetailPage() {
  useAuthenticationGuard()

  const { chatid } = useParams()
  const { user } = useContext(UserContext)


  const createMessageMutation = useCreateMessageMutation(chatid)
  const { isLoading, isError, data: chatMessagesData } = useGetChatMessagesService(chatid)
  const { isLoading: chatIsLoading, isError: chatIsError, data: chatData } = useGetChatByIdService(chatid)

  const to_id = useMemo(() => {
    const user1_id = chatData?.data?.user1_id
    const user2_id = chatData?.data?.user2_id

    return user?.id == user1_id ? user2_id : user1_id
  }, [chatData, user])


  const [message, setMessage] = useState('')

  const handleSubmitMessage = (e: any) => {
    e.preventDefault()
    const to = to_id.toString()
    createMessageMutation({ message, to_id: to })
    setMessage('')
  }

  if (isLoading) return <div>Loading...</div>
  if (isError) return <div>Error</div>

  return (
    <div>
      <h1>Chat {chatid}</h1>
      <ul>
        {chatMessagesData?.data.map((message: any) => {
          return (
            <li key={message.id}>{message.message}</li>
          )
        })}
      </ul>
      <form onSubmit={handleSubmitMessage}>
        <input value={message} onChange={e => setMessage(e.target.value)} type="text" placeholder="Please enter a message..." />
        <button type="submit">Send</button>
      </form>
    </div>
  )
}

