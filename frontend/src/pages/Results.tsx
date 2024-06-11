import { useEffect, useState } from "react"

function Results() {
  const [data, setData] = useState("")
  useEffect(()=>{
    let dataFromLocalStorage = localStorage.getItem("scrapped-data")
    dataFromLocalStorage != null ? setData(dataFromLocalStorage) : setData("Null aaay bhai") 
  }, [localStorage.getItem("scrapped-data")])
  return (
    <div>
      <h1 className="mb-4 text-4xl font-extrabold leading-none tracking-tight text-gray-900 md:text-5xl lg:text-6xl dark:text-white">
        Results
      </h1>
      {data}
    </div>
  )
}

export default Results