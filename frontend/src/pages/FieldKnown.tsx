import { useEffect, useState } from "react"
import axios from "axios"
import { Button } from "@/components/ui/button"
import { Label } from '@/components/ui/label'
import { Card, CardContent } from '@/components/ui/card'
import { Input } from "@/components/ui/input"



function FieldKnown() {
    const [field, setField] = useState("");
    const [location, setLocation] = useState("");
    const [experience, setExperience] = useState(0);
    const [scrappedData, setScrappedData] = useState({});
    function getScrappedDataForKnownField(field: string, location: string, experience: number){
        console.log("inside onclick function!!!!!")
        console.log(field)
        console.log(location)
        console.log(experience)
        
        axios({
            method:"POST",
            url: "http://localhost:5000/api/v1/known-field-data",
            data:{
                title: field,
                location: location,
                experience: experience
            }
            
        }).then((response)=>{
            console.log(response.data)
            setScrappedData(response.data);
            console.log(scrappedData)
        }).catch((e) => {
            console.log("error!")
            console.log(e)
        })
    }
    return (
        <div className='h-screen flex items-center justify-center'>
            <Card>
                <CardContent>
                    <div className='flex items-center h-full justify-center'>
                        {/* <form className='space-y-4 p-4 w-[26rem]' action="/"> */}
                        <div className='space-y-4 p-4 w-[26rem]'>
                            <div>
                                <Label>Field</Label>
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
                        </div>
                        {/* </form> */}
                    </div>
                    <div>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}

export default FieldKnown