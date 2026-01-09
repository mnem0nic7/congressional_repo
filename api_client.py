"""API client for api.data.gov services."""

import requests
from typing import Optional
from config import Config


class DataGovAPIClient:
    """Client for interacting with api.data.gov APIs."""

    def __init__(self):
        """Initialize the API client."""
        Config.validate()
        self.api_key = Config.API_KEY
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
        })

    def _make_request(
        self,
        url: str,
        params: Optional[dict] = None,
        method: str = "GET"
    ) -> dict:
        """Make an API request with error handling."""
        if params is None:
            params = {}

        # Add API key to params
        params["api_key"] = self.api_key

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                timeout=Config.TIMEOUT
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise APIError(f"HTTP error: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.ConnectionError:
            raise APIError("Connection error: Unable to connect to the API")
        except requests.exceptions.Timeout:
            raise APIError("Request timed out")
        except requests.exceptions.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")


class CongressAPIClient(DataGovAPIClient):
    """Client for Congress.gov API (https://api.congress.gov)."""

    def __init__(self):
        """Initialize the Congress API client."""
        super().__init__()
        self.base_url = Config.CONGRESS_API_BASE

    def get_bills(
        self,
        congress: Optional[int] = None,
        bill_type: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> dict:
        """
        Get a list of bills.

        Args:
            congress: Congress number (e.g., 118 for 118th Congress)
            bill_type: Type of bill (hr, s, hjres, sjres, hconres, sconres, hres, sres)
            limit: Number of results to return (max 250)
            offset: Starting position for results

        Returns:
            Dictionary containing bill data
        """
        if congress and bill_type:
            url = f"{self.base_url}/bill/{congress}/{bill_type}"
        elif congress:
            url = f"{self.base_url}/bill/{congress}"
        else:
            url = f"{self.base_url}/bill"

        params = {"limit": limit, "offset": offset}
        return self._make_request(url, params)

    def get_bill(self, congress: int, bill_type: str, bill_number: int) -> dict:
        """
        Get details for a specific bill.

        Args:
            congress: Congress number
            bill_type: Type of bill
            bill_number: Bill number

        Returns:
            Dictionary containing bill details
        """
        url = f"{self.base_url}/bill/{congress}/{bill_type}/{bill_number}"
        return self._make_request(url)

    def get_members(
        self,
        limit: int = 20,
        offset: int = 0,
        current_member: Optional[bool] = None
    ) -> dict:
        """
        Get a list of Congress members.

        Args:
            limit: Number of results to return
            offset: Starting position for results
            current_member: Filter for current members only

        Returns:
            Dictionary containing member data
        """
        url = f"{self.base_url}/member"
        params = {"limit": limit, "offset": offset}
        if current_member is not None:
            params["currentMember"] = str(current_member).lower()
        return self._make_request(url, params)

    def get_member(self, bioguide_id: str) -> dict:
        """
        Get details for a specific member.

        Args:
            bioguide_id: Member's Bioguide ID

        Returns:
            Dictionary containing member details
        """
        url = f"{self.base_url}/member/{bioguide_id}"
        return self._make_request(url)

    def get_committees(
        self,
        chamber: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> dict:
        """
        Get a list of congressional committees.

        Args:
            chamber: Chamber (house, senate, or joint)
            limit: Number of results to return
            offset: Starting position for results

        Returns:
            Dictionary containing committee data
        """
        if chamber:
            url = f"{self.base_url}/committee/{chamber}"
        else:
            url = f"{self.base_url}/committee"

        params = {"limit": limit, "offset": offset}
        return self._make_request(url, params)

    def get_amendments(
        self,
        congress: Optional[int] = None,
        limit: int = 20,
        offset: int = 0
    ) -> dict:
        """
        Get a list of amendments.

        Args:
            congress: Congress number
            limit: Number of results to return
            offset: Starting position for results

        Returns:
            Dictionary containing amendment data
        """
        if congress:
            url = f"{self.base_url}/amendment/{congress}"
        else:
            url = f"{self.base_url}/amendment"

        params = {"limit": limit, "offset": offset}
        return self._make_request(url, params)

    def get_summaries(
        self,
        congress: Optional[int] = None,
        bill_type: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> dict:
        """
        Get bill summaries.

        Args:
            congress: Congress number
            bill_type: Type of bill
            limit: Number of results to return
            offset: Starting position for results

        Returns:
            Dictionary containing summary data
        """
        if congress and bill_type:
            url = f"{self.base_url}/summaries/{congress}/{bill_type}"
        elif congress:
            url = f"{self.base_url}/summaries/{congress}"
        else:
            url = f"{self.base_url}/summaries"

        params = {"limit": limit, "offset": offset}
        return self._make_request(url, params)


class APIError(Exception):
    """Custom exception for API errors."""
    pass
