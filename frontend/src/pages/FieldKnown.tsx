import { useEffect, useState } from "react"
import axios from "axios"
import { Button } from "@/components/ui/button"
import { Label } from '@/components/ui/label'
import { Card, CardContent } from '@/components/ui/card'
import { Input } from "@/components/ui/input"


function getScrappedDataForKnownField(field: string, location: string, experience: number){
    console.log("function!!!!!")
    // const data = axios.get("http://localhost:8080/known-field-data").then((response) => response.data)
    const data = axios.get("http://localhost:5000/known-field-data").then((response) => response.data)
    console.log(data);
    return data
}

function FieldKnown() {
    const [field, setField] = useState("");
    const [location, setLocation] = useState("");
    const [experience, setExperience] = useState(0);
    return (

    <div className='h-screen flex items-center justify-center'>
        <Card>
            <CardContent>
                <div className='flex items-center h-full justify-center'>
                    <form className='space-y-4 p-4 w-[26rem]' action="">
                        <div>
                            <Label>Feild</Label>
                            <Input placeholder="Web development" onChange={(e) => setField(e.target.value)} />
                        </div>
                        <div>
                            <Label>Location</Label>
                            <Input placeholder="Vadodara" onChange={(e) => setLocation(e.target.value)} />
                        </div>
                        <div>
                            <Label>Experience</Label>
                            <Input type="number" placeholder="0"  onChange={(e) => setExperience(parseInt(e.target.value))} />
                        </div>
                        <Button className='w-full' onClick={()=>getScrappedDataForKnownField(field, location, experience)}>Search</Button>
                    </form>
                </div>
            </CardContent>
        </Card>
    </div>
)
}

export default FieldKnown