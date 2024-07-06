import { useState } from "react"
import axios from "axios"
import { Button } from "@/components/ui/button"
import { Loader2 } from "lucide-react"
import { Label } from '@/components/ui/label'
import { Card, CardContent } from '@/components/ui/card'
import { Input } from "@/components/ui/input"


function FieldKnown() {
    const [field, setField] = useState("web devlopment");
    const [location, setLocation] = useState("");
    const [experience, setExperience] = useState(0);
    const [scrappedData, setScrappedData] = useState({});
    const [isLoading, setIsLoading] = useState(false);
    const [isDataReady, setIsDataReady] = useState(false);
    
    function getScrappedDataForKnownField(field: string, location: string, experience: number){
        setIsLoading(true);
        console.log(field)
        console.log(location)
        console.log(experience)
        
        axios({
            method:"POST",
            url: import.meta.env.VITE_SERVER_URL + "/api/v1/known-field-data",
            data:{
                title: field,
                location: location,
                experience: experience
            }
            
        }).then((response)=>{
            console.log("response data: " + JSON.stringify(response.data))
            setScrappedData(response.data);
            console.log(scrappedData)
            window.localStorage.setItem("scrapped-data", JSON.stringify(response.data))
            // console.log("value that is not in local storage" + window.localStorage.getItem("notinls"));
            setIsLoading(false);
            setIsDataReady(true);
        }).catch((e) => {
                setIsLoading(false);
                console.log("error!")
                console.log(e)
                })
            }
    function handleCheckData(){
        window.open(import.meta.env.VITE_CLOUDFRONT_URL + "/fieldknown/results")
    }
    return (
        <div className='h-screen flex items-center justify-center'>
            <Card>
                <CardContent>
                    <div className='flex items-center h-full justify-center'>
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
                            {(isLoading) ? 
                                <div className="">
                                    <Button disabled className='w-full my-2' onClick={()=>getScrappedDataForKnownField(field, location, experience)}>
                                        <Loader2 className="mr-2 h-4 w-4 animate-spin"/>
                                        <span>Search</span>
                                    </Button>
                                    
                                </div>
                                 : 
                                <div>
                                    {(isDataReady) ? 
                                        <Button className="w-full" onClick={handleCheckData}>
                                            <span>Check Data</span>
                                        </Button> : <div>
                                        <Button className='w-full' onClick={()=>getScrappedDataForKnownField(field, location, experience)}>
                                            <span>Search</span>
                                        </Button>
                                        </div>
                                    }
                                </div>
                            }
                            
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}

export default FieldKnown