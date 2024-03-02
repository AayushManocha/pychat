import { useParams } from "@remix-run/react"
import { set } from "node_modules/cypress/types/lodash"
import { useContext, useMemo, useState } from "react"
import NewMessageForm from "~/components/NewMessageForm"
import useAuthenticationGuard from "~/hooks/useAuthenticationGuard"
import useCreateMessageMutation from "~/hooks/useCreateMessageMutation"
import { useGetChatByIdService } from "~/hooks/useGetChatByIdService"
import useGetChatMessagesService from "~/hooks/useGetChatMessagesService"
import { UserContext } from "~/root"

export default function ChatDetailPage() {
  useAuthenticationGuard()

  const { chatid } = useParams()
  const { user } = useContext(UserContext)


  const { isLoading, isError, data: chatMessagesData } = useGetChatMessagesService(chatid, 1000)
  const { isLoading: chatIsLoading, isError: chatIsError, data: chatData } = useGetChatByIdService(chatid)

  if (isLoading) return <div>Loading...</div>
  if (isError) return <div>Error</div>

  console.log('chatMessagesData', chatMessagesData)

  return (
    <div>
      <h1>Chat {chatid}</h1>
      <div>
        {chatMessagesData?.data.map((message: any) => {
          return (
            <ChatMessage key={message.id} message={message} />
          )
        })}
      </div>
      <NewMessageForm chatData={chatData} />
    </div>
  )
}


function ChatMessage({ message }: { message: any }) {
  return (
    <div>
      <article>
        <header>
          <i>
            From: {message.sender_name}
          </i>
        </header>
        <p>{message.message}</p>
      </article>
    </div>
  )
}
