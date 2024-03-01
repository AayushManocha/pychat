import { useContext, useMemo, useState } from "react"
import useCreateMessageMutation from "~/hooks/useCreateMessageMutation"
import { UserContext } from "~/root"

export default function NewMessageForm({ chatData }: any) {

  const [message, setMessage] = useState('')
  const { user } = useContext(UserContext)
  const chatid = chatData?.data?.id
  const createMessageMutation = useCreateMessageMutation(chatid)

  const to_id = useMemo(() => {
    const user1_id = chatData?.data?.user1_id
    const user2_id = chatData?.data?.user2_id

    return user?.id == user1_id ? user2_id : user1_id
  }, [chatData, user])

  const handleSubmitMessage = (e: any) => {
    e.preventDefault()
    const to = to_id.toString()
    createMessageMutation({ message, to_id: to })
    setMessage('')
  }
  return (
    <form onSubmit={handleSubmitMessage}>
      <input value={message} onChange={e => setMessage(e.target.value)} type="text" placeholder="Please enter a message..." />
      <button type="submit">Send</button>
    </form>
  )
}