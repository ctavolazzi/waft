"""
Bob the Cartographer's API Integration Module

Provides Bob with the ability to access the OpenStreetMap Nominatim API
for geocoding and mapping tasks.

This module was evolved by Bob (being_20260113_003031_c29056ab) as part of
his evolution to access APIs from the public-apis repository.
"""

import requests
from typing import Dict, Any, Optional, List, Tuple
from time import sleep


class NominatimAPI:
    """
    OpenStreetMap Nominatim API client for Bob the Cartographer.
    
    Provides geocoding, reverse geocoding, and place search capabilities.
    """
    
    BASE_URL = "https://nominatim.openstreetmap.org"
    
    def __init__(self, user_agent: str = "BobTheCartographer/1.0"):
        """
        Initialize Nominatim API client.
        
        Args:
            user_agent: User agent string (required by Nominatim)
        """
        self.user_agent = user_agent
        self.headers = {
            "User-Agent": user_agent
        }
        # Rate limiting: Nominatim requires max 1 request per second
        self.last_request_time = 0.0
        self.min_request_interval = 1.0
    
    def _rate_limit(self):
        """Enforce rate limiting (1 request per second)."""
        import time
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            sleep(self.min_request_interval - time_since_last)
        self.last_request_time = time.time()
    
    def geocode_address(
        self,
        address: str,
        limit: int = 1,
        format: str = "json"
    ) -> List[Dict[str, Any]]:
        """
        Forward geocoding: Convert address to coordinates.
        
        Args:
            address: Address string to geocode
            limit: Maximum number of results (default: 1)
            format: Response format (json, xml) - default: json
        
        Returns:
            List of location results with coordinates
        
        Example:
            >>> api = NominatimAPI()
            >>> results = api.geocode_address("1600 Amphitheatre Parkway, Mountain View, CA")
            >>> print(results[0]['lat'], results[0]['lon'])
        """
        self._rate_limit()
        
        params = {
            "q": address,
            "format": format,
            "limit": limit,
            "addressdetails": 1
        }
        
        try:
            response = requests.get(
                f"{self.BASE_URL}/search",
                params=params,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return [{"error": str(e)}]
    
    def reverse_geocode(
        self,
        lat: float,
        lon: float,
        format: str = "json"
    ) -> Optional[Dict[str, Any]]:
        """
        Reverse geocoding: Convert coordinates to address.
        
        Args:
            lat: Latitude
            lon: Longitude
            format: Response format (json, xml) - default: json
        
        Returns:
            Address information for the coordinates
        
        Example:
            >>> api = NominatimAPI()
            >>> result = api.reverse_geocode(37.4224764, -122.0842499)
            >>> print(result['display_name'])
        """
        self._rate_limit()
        
        params = {
            "lat": lat,
            "lon": lon,
            "format": format,
            "addressdetails": 1
        }
        
        try:
            response = requests.get(
                f"{self.BASE_URL}/reverse",
                params=params,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}
    
    def search_place(
        self,
        query: str,
        limit: int = 10,
        format: str = "json"
    ) -> List[Dict[str, Any]]:
        """
        Search for places by name.
        
        Args:
            query: Place name or search query
            limit: Maximum number of results (default: 10)
            format: Response format (json, xml) - default: json
        
        Returns:
            List of matching places
        
        Example:
            >>> api = NominatimAPI()
            >>> results = api.search_place("Eiffel Tower")
            >>> print(results[0]['display_name'])
        """
        return self.geocode_address(query, limit=limit, format=format)
    
    def get_coordinates(self, address: str) -> Optional[Tuple[float, float]]:
        """
        Get coordinates (lat, lon) for an address.
        
        Convenience method that returns just the coordinates.
        
        Args:
            address: Address string
        
        Returns:
            Tuple of (latitude, longitude) or None if not found
        
        Example:
            >>> api = NominatimAPI()
            >>> coords = api.get_coordinates("San Francisco, CA")
            >>> print(f"Lat: {coords[0]}, Lon: {coords[1]}")
        """
        results = self.geocode_address(address, limit=1)
        if results and "error" not in results[0] and "lat" in results[0]:
            try:
                lat = float(results[0]["lat"])
                lon = float(results[0]["lon"])
                return (lat, lon)
            except (ValueError, KeyError):
                return None
        return None
    
    def get_address(self, lat: float, lon: float) -> Optional[str]:
        """
        Get address string for coordinates.
        
        Convenience method that returns just the display name.
        
        Args:
            lat: Latitude
            lon: Longitude
        
        Returns:
            Address string or None if not found
        
        Example:
            >>> api = NominatimAPI()
            >>> address = api.get_address(37.7749, -122.4194)
            >>> print(address)
        """
        result = self.reverse_geocode(lat, lon)
        if result and "error" not in result and "display_name" in result:
            return result["display_name"]
        return None


# Bob's convenience functions
def geocode_address(address: str) -> Optional[Tuple[float, float]]:
    """
    Bob's geocoding function - convert address to coordinates.
    
    Args:
        address: Address string to geocode
    
    Returns:
        Tuple of (latitude, longitude) or None
    """
    api = NominatimAPI(user_agent="BobTheCartographer/1.0")
    return api.get_coordinates(address)


def reverse_geocode(lat: float, lon: float) -> Optional[str]:
    """
    Bob's reverse geocoding function - convert coordinates to address.
    
    Args:
        lat: Latitude
        lon: Longitude
    
    Returns:
        Address string or None
    """
    api = NominatimAPI(user_agent="BobTheCartographer/1.0")
    return api.get_address(lat, lon)


def search_place(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Bob's place search function - find places by name.
    
    Args:
        query: Place name or search query
        limit: Maximum number of results
    
    Returns:
        List of matching places
    """
    api = NominatimAPI(user_agent="BobTheCartographer/1.0")
    return api.search_place(query, limit=limit)
