import { useEffect, useState } from "react"
import Barchart from "@/components/Barchart"

function KnownFieldResults() {
  const [data, setData] = useState({"average-salary": 0, "skills": {}})
  const dataFromLocalStorage = localStorage.getItem("scrapped-data")
  useEffect(()=>{
    const parsedDataFromLocalStroage = dataFromLocalStorage != null ? JSON.parse(dataFromLocalStorage) : "nothing"
    setData(parsedDataFromLocalStroage)
  }, [dataFromLocalStorage])
  return (
    <div>
      <h1 className="mb-4 text-xl font-bold leading-none tracking-tight text-gray-900 md:text-2xl lg:text-2xl dark:text-white">
        Average Salary = {data["average-salary"]}
      </h1>
      {/* <Barchart /> */}
    </div>
  )
}

export default KnownFieldResults