"""Example usage of the api.data.gov API client."""

from api_client import CongressAPIClient, APIError


def main():
    """Demonstrate API client usage."""
    try:
        # Initialize the client
        client = CongressAPIClient()

        # Example 1: Get recent bills from the 118th Congress
        print("=" * 50)
        print("Recent Bills from 118th Congress")
        print("=" * 50)
        bills = client.get_bills(congress=118, limit=5)
        for bill in bills.get("bills", []):
            print(f"- {bill.get('number')}: {bill.get('title', 'No title')[:60]}...")

        # Example 2: Get current members of Congress
        print("\n" + "=" * 50)
        print("Current Members of Congress")
        print("=" * 50)
        members = client.get_members(limit=5, current_member=True)
        for member in members.get("members", []):
            name = member.get("name", "Unknown")
            party = member.get("partyName", "Unknown")
            state = member.get("state", "Unknown")
            print(f"- {name} ({party}) - {state}")

        # Example 3: Get House committees
        print("\n" + "=" * 50)
        print("House Committees")
        print("=" * 50)
        committees = client.get_committees(chamber="house", limit=5)
        for committee in committees.get("committees", []):
            print(f"- {committee.get('name', 'Unknown')}")

        # Example 4: Get a specific bill
        print("\n" + "=" * 50)
        print("Specific Bill Details (HR 1)")
        print("=" * 50)
        try:
            bill = client.get_bill(congress=118, bill_type="hr", bill_number=1)
            bill_data = bill.get("bill", {})
            print(f"Title: {bill_data.get('title', 'N/A')}")
            print(f"Introduced: {bill_data.get('introducedDate', 'N/A')}")
            print(f"Latest Action: {bill_data.get('latestAction', {}).get('text', 'N/A')}")
        except APIError as e:
            print(f"Could not fetch bill: {e}")

    except APIError as e:
        print(f"API Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
