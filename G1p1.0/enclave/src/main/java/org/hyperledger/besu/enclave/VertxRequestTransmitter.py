import asyncio
import aiohttp

class AioHttpRequestTransmitter:
    def __init__(self, session):
        self.session = session

    async def post(self, content_type, content, endpoint, response_handler):
        return await self.send_request("POST", content_type, content, endpoint, response_handler, False)

    async def get(self, content_type, content, endpoint, response_handler, with_accept_json_header):
        return await self.send_request("GET", content_type, content, endpoint, response_handler, with_accept_json_header)

    async def send_request(self, method, content_type, content, endpoint, response_handler, with_accept_json_header):
        try:
            options = {
                'method': method,
                'url': endpoint,
                'headers': {},
                'timeout': aiohttp.ClientTimeout(total=5)
            }

            if with_accept_json_header:
                options['headers']['Accept'] = 'application/json'

            if content_type is not None:
                options['headers']['Content-Type'] = content_type

            if content is not None:
                options['data'] = content

            async with self.session.request(**options) as response:
                return await self.handle_response(response, response_handler)
        except aiohttp.ClientError as e:
            raise EnclaveIOException("Enclave Communication Failed") from e

    async def handle_response(self, response, response_handler):
        try:
            response_body = await response.read()
            return response_handler.convert_response(response.status, response_body)
        except Exception as e:
            raise EnclaveIOException("Error handling response") from e

async def convert_response(status_code, response_body):
    # Implement your response conversion logic here
    pass

async def main():
    async with aiohttp.ClientSession() as session:
        transmitter = AioHttpRequestTransmitter(session)
        response = await transmitter.post(
            "application/json",
            "request_content",
            "https://example.com/endpoint",
            convert_response
        )
        print(response)

asyncio.run(main())
