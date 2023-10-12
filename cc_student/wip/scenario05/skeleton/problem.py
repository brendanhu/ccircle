from enum import Enum
from itertools import count
from typing import Generator, Any


# TODO: this should be modeled as an FSM.
class ShipmentState(Enum):
    QUOTE_REQUESTED, QUOTE_ACCEPTED, SHIPMENT_DELIVERED = range(3)


class Shipment:
    """ A shipment is a good that needs to be transported from its pickup location to its destination location."""
    shipment_id_counter = count(start=1)

    def __init__(self):
        self.id = next(Shipment.shipment_id_counter)
        self.state = ShipmentState.QUOTE_REQUESTED
        self.pickup_location = 'pickup; TODO: implement location generator'
        self.delivery_location = 'delivery; TODO: implement location generator'

    def get_id(self) -> int:
        return self.id

    def _quote_accepted(self) -> None:
        self.state = ShipmentState.QUOTE_ACCEPTED

    def _quote_delivered(self) -> None:
        self.state = ShipmentState.SHIPMENT_DELIVERED


class Truck:
    """ A truck is a vehicle that can transport shipments."""
    def __init__(self, id: int, ):
        self.id = id


class Carrier:
    """ A carrier is a company that owns trucks and can transport shipments."""
    def __init__(self, id: int):
        self.id = id
        self.trucks = [] # TODO: give carriers at least 1 truck.

    def _add_truck(self, truck: Truck) -> None:
        self.trucks.append(truck)


class Marketplace:
    """ The marketplace is the central hub for all freight-related activities."""
    _carriers_by_id: dict[int, Carrier]
    _shipments_by_id: dict[int, Shipment]

    def __init__(self):
        self._carriers_by_id = {}
        self._shipments_by_id = {}

    @property
    def shipment_ids(self) -> list[int]:
        """ Returns a list of all shipment ids in the marketplace."""
        return list(self._shipments_by_id.keys())

    @property
    def carrier_ids(self) -> list[int]:
        """ Returns a list of all carrier ids in the marketplace."""
        return list(self._carriers_by_id.keys())

    def _validate_shipment_exists(self, shipment_id: int) -> None:
        """ Raises an exception if there is no shipment with the given id in the marketplace."""
        if shipment_id not in self._shipments_by_id:
            raise Exception(f'There are no shipments with id {shipment_id} in the marketplace!')

    def _validate_carrier_exists(self, carrier_id: int) -> None:
        """ Raises an exception if there is no carrier with the given id in the marketplace."""
        if carrier_id not in self._carriers_by_id:
            raise Exception(f'There are no carriers with id {carrier_id} in the marketplace!')

    def get_carrier(self, carrier_id: int) -> Carrier:
        """ Returns the carrier with the given id."""
        self._validate_carrier_exists(carrier_id)
        return self._carriers_by_id[carrier_id]

    def get_shipment(self, shipment_id: int) -> Shipment:
        """ Returns the shipment with the given id."""
        self._validate_shipment_exists(shipment_id)
        return self._shipments_by_id[shipment_id]

    def add_shipment(self, shipment: Shipment) -> None:
        """ Adds the given shipment to the marketplace."""
        self._shipments_by_id[shipment.id] = shipment
        print(f'Added shipment {shipment.id} to the marketplace.')

    def add_carrier(self, carrier: Carrier) -> None:
        """ Adds the given carrier to the marketplace."""
        self._carriers_by_id[carrier.id] = carrier
        print(f'Added carrier {carrier.id} to the marketplace.')

    def update(self) -> None:
        """ Update the marketplace for the next day. """
        pass


def create_marketplace(shipment_count: int = 8, carrier_count: int = 4) -> Marketplace:
    # Validate that both parameters are positive integers.
    if not isinstance(shipment_count, int) or shipment_count < 1:
        raise Exception('shipment_count must be a positive integer!')
    if not isinstance(carrier_count, int) or carrier_count < 1:
        raise Exception('carrier_count must be a positive integer!')

    market = Marketplace()

    # Add shipments to the marketplace.
    shipments = [Shipment() for _ in range(shipment_count)]
    for shipment in shipments:
        market.add_shipment(shipment)

    # Add carriers to the marketplace.
    carriers = [Carrier(i) for i in range(carrier_count)]
    for carrier in carriers:
        market.add_carrier(carrier)

    return market
