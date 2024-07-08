type ToggleViewProps = {
    display: boolean,
    children?: React.ReactNode
}
function ToggleView({ display, children }: ToggleViewProps) {
  if(display){
      return (
            <div>{children}</div>
        )
  }
}

export default ToggleView