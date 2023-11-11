import requests
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning


class ConfluenceConnector:
    def __init__(self, username, password, confluence_url):
        self.username = username
        self.password = password
        self.confluence_url = confluence_url
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        self.session = requests.Session()

    def _set_proxy(self):

            proxies = {
                 "http":"example.com" ,
                 "https": "example.com:8080",
            }
            self.session.proxies.update(proxies)

    def connect(self):
        self._set_proxy()
        # Perform any additional connection setup if needed

    def create_page(self, space, title, content):
        create_page_url = f"{self.confluence_url}/rest/api/content/"

        data = {
            'type': 'page',
            'title': title,
            'space': {'key': space},
            'body': {
                'storage': {
                    'value': content,
                    'representation': 'storage'
                }
            }
        }

        response = self.session.post(
            create_page_url,
            auth=HTTPBasicAuth(self.username, self.password),
            headers={'Content-Type': 'application/json'},
            json=data,
            verify=False
        )

        if response.status_code == 200:
            print(f"Page '{title}' created successfully!")
        else:
            print(f"Failed to create page. Status code: {response.status_code}")
            print(response.text)

    def get_page_id_by_title(self, space, title):
        search_url = f"{self.confluence_url}/rest/api/content"
        params = {
            'title': title,
            'spaceKey': space,
            'expand': 'version'
        }

        response = self.session.get(
            search_url,
            auth=HTTPBasicAuth(self.username, self.password),
            headers={'Content-Type': 'application/json'},
            params=params
        )

        if response.status_code == 200:
            results = response.json().get('results', [])
            if results:
                # Assuming the first result is the desired page
                return results[0]['id']
            else:
                print(f"No page found with title '{title}' in space '{space}'.")
                return None
        else:
            print(f"Failed to get page ID by title. Status code: {response.status_code}")
            print(response.text)
            return None

    def delete_page(self, page_id):
        delete_page_url = f"{self.confluence_url}/rest/api/content/{page_id}"

        response = self.session.delete(
            delete_page_url,
            auth=HTTPBasicAuth(self.username, self.password),
            headers={'Content-Type': 'application/json'}
        )

        if response.status_code == 204:
            print(f"Page with ID {page_id} deleted successfully!")
        else:
            print(f"Failed to delete page. Status code: {response.status_code}")
            print(response.text)


if __name__ == "__main__":
    # Example usage:
    username = input("Enter Confluence username: ")
    password = input("Enter Confluence password: ")
    confluence_url = input("Enter Confluence URL: ")
    space_key = input("Enter Confluence space key: ")

    connector = ConfluenceConnector(username, password, confluence_url)

    try:
        connector.connect()

        title = input("Enter page title to delete: ")

        # Get page ID by title
        page_id = connector.get_page_id_by_title(space_key, title)

        if page_id:
            # Delete the page
            connector.delete_page(page_id)
    except Exception as e:
        print(f"An error occurred: {str(e)}")