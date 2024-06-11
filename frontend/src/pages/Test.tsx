import { Button } from '@/components/ui/button'
import axios from 'axios'
import { useState } from 'react'

function Test() {
    const [message, setMessage] = useState("")
    function handleOnClick(){
        axios({
            method:"GET",
            url: "http://localhost:5000/api/v1/test",
            
        }).then((response)=>{
            setMessage(response.data)
            console.log(response.data)
        }).catch((e) => {
            console.log("error!")
            console.log(e)
        })
        // setMessage("testing...")
    }

  return (
    <div>

        {message}
        <Button onClick={handleOnClick}> Test </Button>
    </div>
)
}

export default Test