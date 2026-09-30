import unittest
from unittest.mock import MagicMock

from castervoice.lib.merge.state.stack import ContextStack
from castervoice.lib.merge.state.stackitems import (
    StackItemRegisteredAction,
    StackItemAsynchronous,
    StackItemSeeker,
)


class MockStackItem:
    def __init__(self, item_id, complete=True, item_type=StackItemRegisteredAction.TYPE):
        self.id = item_id
        self.type = item_type
        self.complete = complete
        self.consumed = False
        self.back = None
        mock_context_level = MagicMock()
        mock_context_level.result.consume = False
        self.forward = [mock_context_level]
        self.cleaned = False
        self.rspec = f"spec_{item_id}"
        self.preserved = []

    def preserve(self):
        pass

    def put_time_action(self):
        pass

    def execute(self, *args, **kwargs):
        pass

    def clean(self):
        self.cleaned = True

    def begin(self):
        pass

    def get_index_of_next_unsatisfied_level(self):
        return -1 if self.complete else 0

    def satisfy_level(self, level_index, is_back, stack_item):
        pass

    def get_parameters(self, level, stack_item):
        pass


class TestContextStack(unittest.TestCase):
    def setUp(self):
        self.mock_state = MagicMock()
        self.stack = ContextStack(self.mock_state)

    def test_normal_eviction_fifo_order(self):
        """Completed items are evicted in FIFO order when exceeding max_list_size."""
        total_items = 35
        for i in range(total_items):
            item = MockStackItem(item_id=i, complete=True)
            self.stack.add(item)

        self.assertEqual(len(self.stack.list), self.stack.max_list_size)
        expected_ids = list(range(total_items - self.stack.max_list_size, total_items))
        actual_ids = [item.id for item in self.stack.list]
        self.assertEqual(actual_ids, expected_ids)

    def test_incomplete_item_preservation(self):
        """When an incomplete item is in the stack and completed items exceed max_list_size,
        the incomplete item is not evicted and remains in get_incomplete_seekers()."""
        incomplete_item = MockStackItem(
            item_id="async_action",
            complete=False,
            item_type=StackItemAsynchronous.TYPE,
        )
        self.stack.add(incomplete_item)

        total_completed = 35
        for i in range(total_completed):
            item = MockStackItem(item_id=i, complete=True)
            self.stack.add(item)

        self.assertEqual(len(self.stack.list), self.stack.max_list_size)
        self.assertIn(incomplete_item, self.stack.list)
        incomplete_seekers = self.stack.get_incomplete_seekers()
        self.assertIn(incomplete_item, incomplete_seekers)
        self.assertEqual(len(incomplete_seekers), 1)

        # Incomplete item should still be at index 0 of the list
        self.assertEqual(self.stack.list[0], incomplete_item)
        # Completed items should have evicted the oldest completed items (0 to 5)
        # leaving completed items 6 to 34 (29 items) + 1 incomplete item = 30 items
        expected_completed_ids = list(range(total_completed - (self.stack.max_list_size - 1), total_completed))
        actual_completed_ids = [item.id for item in self.stack.list[1:]]
        self.assertEqual(actual_completed_ids, expected_completed_ids)

    def test_all_incomplete_fallback_cleans_evicted_item(self):
        """When all items in the stack are incomplete, eviction falls back to evicting
        the oldest item and calls clean() on it."""
        items = []
        for i in range(self.stack.max_list_size + 1):
            item = MockStackItem(
                item_id=i,
                complete=False,
                item_type=StackItemAsynchronous.TYPE,
            )
            items.append(item)
            self.stack.add(item)

        self.assertEqual(len(self.stack.list), self.stack.max_list_size)
        # Oldest incomplete item (index 0) must be evicted
        self.assertNotIn(items[0], self.stack.list)
        self.assertTrue(items[0].cleaned)

        # Remaining items (1 to max_list_size) should be in the stack and not cleaned
        expected_remaining = items[1:]
        self.assertEqual(self.stack.list, expected_remaining)
        for item in expected_remaining:
            self.assertFalse(item.cleaned)

    def test_all_incomplete_fallback_without_clean_method(self):
        """Fallback eviction handles items without a clean() method gracefully."""
        class ItemWithoutClean:
            def __init__(self, item_id):
                self.id = item_id
                self.type = StackItemSeeker.TYPE
                self.complete = False
                self.consumed = False
                self.back = None
                self.forward = None
                self.rspec = f"spec_{item_id}"

            def preserve(self):
                pass

            def put_time_action(self):
                pass

            def execute(self, *args, **kwargs):
                pass

            def get_index_of_next_unsatisfied_level(self):
                return -1

            def satisfy_level(self, level_index, is_back, stack_item):
                pass

        for i in range(self.stack.max_list_size + 1):
            item = ItemWithoutClean(item_id=i)
            self.stack.add(item)

        self.assertEqual(len(self.stack.list), self.stack.max_list_size)
        self.assertEqual(self.stack.list[0].id, 1)
