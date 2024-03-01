import { Link } from "@remix-run/react";
import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { useContext } from "react";
import { UserContext } from "~/root";
import NewChatModal from "./NewChatModal";

interface ChatListProps {
}

export default function ChatList(props: ChatListProps) {
  const { user } = useContext(UserContext)

  const { isLoading, isError, data } = useQuery({
    queryKey: ["chats"],
    queryFn: async () => {
      const res = await axios.get("http://localhost:8000/chat", { withCredentials: true })
      return res.data
    }
  })
  if (isLoading) return <div>Loading...</div>
  if (isError) return <div>Error</div>

  return (
    <div style={{ display: 'flex', flexDirection: 'column', width: '30%', borderRight: '1px black solid', height: '100%' }}>
      {data.map((chat: any) => {
        const chatName: string = chat.user1_name == user?.username ? chat.user2_name : chat.user1_name
        return (
          <Link to={`/chats/${chat.id}`} key={chat.id}>
            <article>
              <h2>{chatName.toLocaleUpperCase()}</h2>
            </article>
          </Link>
        )
      })}
      <NewChatModal />
    </div>
  )

}