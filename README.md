# A pox ethernet controller in mininet
The switch is connected to the controller. Switch maintains a flow table which contains matchaction
rules that are are added/removed/updated by the controller. At the beginning, there are no rules installed in the flow table. When packets are sent by hosts to one another, the
controller extracts information from these packets and builds certain internal data structures
(such as a hashmap, etc.) to represent the topology. The controller will use these internal
data structures to decide what rules should be installed in the switch’s flow table.
