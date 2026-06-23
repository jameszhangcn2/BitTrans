# BitTrans
translator of bit to man readable



@startuml

header BitTrans Architecture

left to right direction

node App 

file xx.json
file xx.output

App ..> xx.json:find the explanatin for the bits
App --> xx.output: print the bit and the explanaiton together
@enduml

