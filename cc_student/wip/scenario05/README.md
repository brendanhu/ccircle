## Game
The goal of the game is to optimize the freight marketplace.

You will need to add your algorithm in the `./player_code.py` file. 

TODO: detail more.

## Terminology
TODO: define these and turn into a table.
- Shipper
- Shipment
- Pallet(ized Linear Feet)
- Carrier 
- Truck
- FTL
- LTL
- Marketplace

## public APIs

---
### Demand side APIs

---
### Supply side APIs

`carrier_network.getFullTruckloadRate(shipment)` -> {carrier_a: ftl_rate_a, carrier_b: ftl_rate_b}}

    Ask all carriers in the network for the FTL (Full Truckload) Rate of the `shipment`.
    The response is a map of each carrier to the dollar amount that the carrier would require
    to move the given shipment from its pickup to its dropoff in its _own_ truck.

`carrier_network.getLessThanTruckloadRate(shipment)` -> {carrier_a: ftl_rate_a, carrier_b: ftl_rate_b}}

    Ask all carriers in the network for the LTL (Full Truckload) Rate of the `shipment`.
    The response is a map of each carrier to the dollar amount that the carrier would require
    to move the given shipment from its pickup to its dropoff, using the LTL hub - potentially
    on _many_ trucks. 

---
### Marketplace APIs

`market.ship(shipment, truck, price)` -> bool

  Attempt to move the `shipment` with a truck.
  You must have enough money in your account or the function will fail!
