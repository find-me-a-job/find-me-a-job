import { BrowserRouter, Routes, Route } from "react-router-dom"
import Home from './pages/Home'
import FieldKnown from "./pages/FieldKnown"
import FieldUnknown from "./pages/FieldUnknown"
import KnownFieldResults from "./components/KnownFieldResults"
import Test from "./pages/Test"
function App() {

  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />}></Route>
          <Route path="/test" element={<Test />}></Route>
          <Route path="/fieldknown" element={<FieldKnown />}></Route>
          <Route path="/fieldunknown" element={<FieldUnknown />}></Route>
          <Route path="/fieldknown/results" element={<KnownFieldResults />}></Route>
        </Routes>
      </BrowserRouter>

    </>
  )
}

export default App
