import { BrowserRouter, Routes, Route } from "react-router-dom"
import Home from './pages/Home'
import FieldKnown from "./pages/FieldKnown"
import FieldUnknown from "./pages/FieldUnknown"
function App() {

  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />}></Route>
          <Route path="/feildknown" element={<FieldKnown />}></Route>
          <Route path="/feildunknown" element={<FieldUnknown />}></Route>
        </Routes>
      </BrowserRouter>

    </>
  )
}

export default App
