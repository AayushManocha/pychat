import { useState } from "react";
import NewMessageForm from "./NewMessageForm";
import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { set } from "node_modules/cypress/types/lodash";

export default function NewChatModal() {
  const [open, setOpen] = useState(false)
  const [stage, setStage] = useState('search') // ['search', 'new-message']
  const [selectedUser, setSelectedUser] = useState<null | number>()

  const handleUserSelect = (userId: number) => {
    setSelectedUser(userId)
    setStage('new-message')
  }

  const handleClose = () => {
    setOpen(false)
    setStage('search')
    setSelectedUser(null)
  }

  return (
    <div>
      <button onClick={() => setOpen(true)}>+ New Chat</button>
      {open && (
        <dialog open={open}>
          <article>
            <header>
              <h1>New Chat</h1>
              <p onClick={handleClose}>Close</p>
            </header>
            {stage === 'search' && <UserSearchField handleUserSelect={handleUserSelect} />}
            {stage === 'new-message' && <NewMessageForm toId={selectedUser} onMessageSent={handleClose} />}
          </article>
        </dialog>
      )}
    </div>
  );
}

interface UserSearchFieldProps {
  handleUserSelect: (userId: number) => void
}

const UserSearchField = (props: UserSearchFieldProps) => {
  const { handleUserSelect } = props

  const [searchTerm, setSearchTerm] = useState('')
  const { isLoading, isError, data } = useQuery({
    queryKey: ['users', searchTerm],
    queryFn: async (ctx) => {
      if (ctx.queryKey[1] !== '') {
        const response = await axios.get(`http://localhost:8000/user/search/${ctx.queryKey[1]}`)
        return response.data
      }
    }
  })

  return (
    <div>
      <input
        value={searchTerm}
        onChange={e => setSearchTerm(e.target.value)}
        type="search" name="search" placeholder="Search" aria-label="Search" />
      <div>
        {isLoading && <div>Loading...</div>}
        {isError && <div>Error</div>}
        {data && (
          <div>
            {data.map((user: any) => {
              return (
                <div key={user.id} style={{ display: 'flex', flexDirection: 'row' }}>
                  <p>{user.username}</p>
                  <button onClick={() => handleUserSelect(user.id)}>Start Chat</button>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  );
}