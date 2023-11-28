import backoff
import httpx

from http_client.exceptions import ClientError, ServerError


class HTTPClient:
    @backoff.on_exception(backoff.expo, (httpx.RequestError, ServerError))
    def _request(self, method: str, url: str) -> httpx.Response:
        if method == "GET":
            r = httpx.get(url)
        elif method == "POST":
            r = httpx.post(url)
        elif method == "PUT":
            r = httpx.put(url)
        elif method == "DELETE":
            r = httpx.delete(url)
        else:
            raise ValueError(f"Invalid http method {method}")

        try:
            return r.raise_for_status()
        except httpx.HTTPStatusError as exc:
            if 400 <= exc.response.status_code < 500:
                raise ClientError(exc)
            if exc.response.status_code >= 500:
                raise ServerError(exc)

        return r

    def get(self, url: str) -> httpx.Response:
        return self._request(method="GET", url=url)

    def post(self, url: str) -> httpx.Response:
        return self._request(method="POST", url=url)

    def put(self, url: str) -> httpx.Response:
        return self._request(method="PUT", url=url)

    def delete(self, url: str) -> httpx.Response:
        return self._request(method="DELETE", url=url)
