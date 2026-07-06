import sys
print("DEBUG PYTHON:", sys.executable)
print("DEBUG VERSION:", sys.version)

from urllib.parse import quote

from bs4 import BeautifulSoup
from locust import HttpUser, task, between

DEBUG_MODE = __name__ == "__main__"

class N11SearchUser(HttpUser):
    host = "https://www.n11.com"
    wait_time = between(1, 3)

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/149.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;"
            "q=0.9,image/avif,image/webp,*/*;q=0.8"
        ),
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive"
    }

    search_keywords = [
        "iphone"
    ]

    def on_start(self):
        response = self.client.get(
            "/",
            name="Open n11 home page",
            headers=self.headers,
            catch_response=True,
            timeout=10
        )
        status_code = response.status_code
        body_text = response.text
        body_snippet = body_text[:300]

        print("HOME STATUS:", status_code)
        print("HOME BODY SNIPPET:", body_snippet)

        if status_code != 200:
            print(f"Home page failed. Status code: {status_code}")
            return


    @task
    def search_product_and_verify_results_are_listed(self):
        for keyword in self.search_keywords:
            encoded_keyword = quote(keyword)
            search_path = f"/arama?q={encoded_keyword}"

            response=self.client.get(
                search_path,
                name="Search product from header",
                headers=self.headers,
                catch_response=False,
                timeout=10
            )
            status_code = response.status_code
            body_text = response.text
            body_snippet = body_text[:500]

            print("SEARCH KEYWORD:", keyword)
            print("SEARCH STATUS:", status_code)
            print("SEARCH BODY SNIPPET:", body_snippet)

            if status_code != 200:
                print(
                    f"Search failed for keyword '{keyword}'. "
                    f"Status code: {status_code}"
                )
                continue

            is_loaded = self._is_search_page_loaded(body_text, keyword)

            print("IS SEARCH RESULT LOADED:", is_loaded)

            if not is_loaded:
                print(
                    f"Search result page loaded but indicators were not found "
                    f"for keyword '{keyword}'"
                )
                continue
        if DEBUG_MODE:
            from locust.exception import StopUser
            raise StopUser()


    @staticmethod
    def _is_search_page_loaded(html, keyword):
        soup = BeautifulSoup(html, "html.parser")
        page_text = soup.get_text(separator=" ", strip=True).lower()

        has_search_keyword = keyword.lower() in page_text

        search_page_indicators = [
            "arama",
            "ürün",
            "urun",
            "sonuç",
            "sonuc",
            "sepet",
            "mağaza",
            "magaza",
            "n11"
        ]

        has_search_indicator = any(
            indicator in page_text for indicator in search_page_indicators
        )

        product_or_listing_selectors = [
            ".productName",
            ".columnContent",
            ".productList",
            ".listView",
            ".catalogView",
            "[data-productid]",
            "[data-product-id]",
            "script"
        ]

        has_listing_related_html = any(
            soup.select_one(selector) is not None
            for selector in product_or_listing_selectors
        )

        return has_search_indicator and (has_search_keyword or has_listing_related_html)

if __name__ == "__main__":
    from locust.debug import run_single_user
    run_single_user(N11SearchUser,
                    include_time=True,
                    include_length=True,
                    loglevel="INFO")