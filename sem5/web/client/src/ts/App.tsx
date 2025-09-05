import { useState } from 'react'
import { makeFetch } from './utils/myfetch';

function App() {
  const [count, setCount] = useState<number>(0);
  const [serverData, setServerData] = useState<string>("");

  const handleIncrease = () => {
    setCount(count + 1);
  }

  const handleDecrease = () => {
    if (count === 0) return;
    setCount(count - 1);
  }

  const handleFetch = () => {
    makeFetch(
      "test_get",
      {},
      (d: {data: string}) => {
        setServerData(d.data);
      },
      () => {
        setServerData("Error fetching from server")
      },
      "error!"
    )
  }

  return (
    <div>
      <button onClick={handleIncrease}>Click here to increase counter</button>
      <button onClick={handleDecrease} disabled={count === 0}>Click here to decrease counter</button>
      <div>Count: {count}</div>

      <button onClick={handleFetch}>Get data from server</button>
      <div>Server data: {serverData}</div>
    </div>
  )
}

export default App
