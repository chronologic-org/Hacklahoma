import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { ApiTest } from './components/ApiTest'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div>
      <h1>Hacklahoma 2025</h1>
      <ApiTest />
    </div>
  )
}

export default App
