import os

import logging
from google.maps import places_v1, routing_v2
from google.maps.routing_v2.types import Waypoint
from google.maps.routing_v2.types import Location
logger = logging.getLogger(__name__)

class GoogleClient:
    def __init__(self):
        self._places_client = places_v1.PlacesClient(
            client_options={"api_key": os.getenv("goog_key")}
        )
        self._routing_client = routing_v2.RoutesClient(
            client_options={"api_key": os.getenv("goog_key")}
        )

    def get_location(self, location_name: str):
        logger.debug(f"Searching for location: {location_name}")
        payload = places_v1.SearchTextRequest(**{
            "text_query": location_name,
            "included_type": "school",
            "strict_type_filtering": False,
            "location_restriction": {
                "rectangle": {
                    "low": {
                        "latitude": 41.58978737860814,
                        "longitude": -87.36885653178716,
                    },
                    "high": {
                        "latitude": 44.886055931941,
                        "longitude": -82.17232366399891,
                    },
                }
            },
        })
        fieldMask = "places.location,places.googleMapsUri"

        resp = self._places_client.search_text(payload,metadata=[("x-goog-fieldmask",fieldMask)])
        logger.debug(resp.places.google_maps_uri)
        if not resp.places:
            logger.error(f"No places found for {location_name}")
            return None
        return resp
    

    def get_directions(self, origin: Waypoint, destination: Waypoint):

        request = routing_v2.ComputeRoutesRequest(
            origin=origin, 
            destination=destination, 
            routing_preference=routing_v2.RoutingPreference.TRAFFIC_AWARE
        )

        fieldMask = "routes.localized_values"
        return self._routing_client.compute_routes(request,metadata=[("x-goog-fieldmask",fieldMask)])
    

    def calc_distance_and_time(self,destination_name: str = "Madonna", origin_address: str = "6441 Drumlin Ct SE, Ada, MI 49301"):
        """
        Calculate distance and time from the route object.
        """
        resp = self.get_location(destination_name)
        logger.info(resp)
        if not resp:
            raise ValueError(f"No location found for {destination_name}")

        route = self.get_directions(
            origin=Waypoint(address=origin_address),
            destination=Waypoint(location=Location(
                lat_lng=resp.places[0].location,  # Assuming the first place is the desired destination
            ))
        )
        
        logger.debug(route)

        distance = route.routes[0].localized_values.distance.text
        time = route.routes[0].localized_values.duration.text
        logger.info(f"Distance: {distance}, Time: {time}")