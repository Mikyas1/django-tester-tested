from unittest import IsolatedAsyncioTestCase
from django.test import AsyncClient
from django.urls import reverse
import asyncio
import time


class TestDjangoAsync(IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.client = AsyncClient()

    async def request_sleep_for_given_seconds(self, sleep_in_seconds):
        start_time = time.time()
        task = asyncio.create_task(self.client.get(
            reverse("sleep_for_given_seconds", kwargs={"seconds": sleep_in_seconds}),
        ))
        response = await task
        return time.time() - start_time, response

    # test django when testing handles request one at a time
    async def test_django_will_wait_for_request_to_finish_before_processing_other(self):
        longest_running = 10
        run_other_after = 5
        shortest_running = 1

        # a request that will take at list 10 seconds
        sleep_request_longest = asyncio.create_task(self.request_sleep_for_given_seconds(longest_running))

        # sleep for 5 second
        await asyncio.sleep(run_other_after)

        # then request api that will take less time (1 sec)
        sleep_request_shortest = asyncio.create_task(self.request_sleep_for_given_seconds(shortest_running))

        sleep_request_shortest_run_time, sleep_request_shortest_response = await sleep_request_shortest
        sleep_request_longest_run_time, sleep_request_longest_response = await sleep_request_longest

        # assert the shortest request will take more than longest_running - run_other_ofter always
        self.assertTrue(int(sleep_request_shortest_run_time) > longest_running - run_other_after)

        self.assertTrue(sleep_request_longest_run_time > sleep_request_shortest_run_time)
        self.assertEqual(sleep_request_shortest_response.status_code, 200)
        self.assertEqual(sleep_request_longest_response.status_code, 200)
