import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
function Home() {
    return (
        <div className='text-center h-screen flex items-center space-x-8 justify-center'>

            <a href="/fieldunknown">
                <Card className='p-8 overflow-hidden transition-all ease-in-out duration-300 hover:shadow-xl max-w-96 max-h-96 flex items-center'>
                    <CardHeader>
                        <CardTitle>Feild Unknown</CardTitle>
                        <CardDescription>You don't know your field that's why you want to research which field would be best for you</CardDescription>
                    </CardHeader>
                    {/* <CardContent>
        <p>Card Content</p>
    </CardContent> */}
                    {/* <Button>Button</Button> */}
                </Card>
            </a>
            <a href="/fieldknown">
                <Card className='p-8 overflow-hidden transition-all ease-in-out duration-300 hover:shadow-xl max-w-96 max-h-96 flex items-center'>
                    <CardHeader>
                        <CardTitle>Feild Known</CardTitle>
                        <CardDescription>You know the field you are interested in and you want to know which skills are the most in-demand for that field</CardDescription>
                    </CardHeader>
                    {/* <CardContent>
        <p>Card Content</p>
    </CardContent> */}
                    {/* <Button>Button</Button> */}
                </Card>
            </a>
        </div>
    )
}

export default Home