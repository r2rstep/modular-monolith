from contextlib import suppress

import pytest

from commons.messagebox.infrastructure.messagebox import Inbox, Messagebox, MessageDict, MessageTopic


def _excluding_created_at(message: MessageDict) -> MessageDict:
    return {k: v for k, v in message.items() if k != "created_at"}


@pytest.mark.asyncio()
class TestMessageBox:
    async def test_needs_to_be_opened_to_add_or_get(self):
        # given empty messagebox
        messagebox = Messagebox("test")

        # when adding a message without opening the messagebox
        # then an exception is raised
        with pytest.raises(RuntimeError, match="Messagebox needs to be opened"):
            await messagebox.add(MessageTopic("test_message"), {"a": 1})

        # and getting a message without opening the messagebox
        # then an exception is raised
        with pytest.raises(RuntimeError, match="Messagebox needs to be opened"):
            await messagebox.get_next_pending()

    async def test_add_and_get_message(self):
        # given empty messagebox
        messagebox = Messagebox("test")

        # when adding a message
        with messagebox.open():
            await messagebox.add(MessageTopic("test_message"), {"field_a": "value_a", "field_b": "value_b"})
            # and getting the message
            message = await messagebox.get_next_pending()

        # then message's name and payload are correct
        assert _excluding_created_at(message) == {
            "topic": MessageTopic("test_message"),
            "payload": {"field_a": "value_a", "field_b": "value_b"},
            "status": "pending",
        }

    async def test_get_next_pending(self):
        # given empty messagebox with a message
        messagebox = Messagebox("test")
        with messagebox.open():
            await messagebox.add(MessageTopic("test_message_1"), {"a": 1})
            await messagebox.add(MessageTopic("test_message_1"), {"a": 2})

            # when the message is processed
            message = await messagebox.get_next_pending()
            message["status"] = "processed"

            # and getting next pending message
            next_message = await messagebox.get_next_pending()

        # then next message is the pending one
        assert _excluding_created_at(next_message) == {
            "topic": MessageTopic("test_message_1"),
            "payload": {"a": 2},
            "status": "pending",
        }

        # when the message is processed
        next_message["status"] = "processed"
        # and getting next pending message
        with messagebox.open():
            next_message = await messagebox.get_next_pending()

        # then the next message is None
        assert next_message is None

    async def test_get_next_not_locked(self):
        # given messagebox with messages
        messagebox = Messagebox("test")
        with messagebox.open():
            await messagebox.add(MessageTopic("test_message_1"), {"a": 1})
            await messagebox.add(MessageTopic("test_message_1"), {"a": 2})

            # when getting next pending message
            message = await messagebox.get_next_pending()

            # then when getting next pending message again
            next_message = await messagebox.get_next_pending()

            # then the next message is different from the first one
            assert message != next_message

            # when getting next pending message again
            next_message = await messagebox.get_next_pending()

            # then the message is none
            assert next_message is None

    async def test_messages_still_in_messagebox_when_exception_occurs(self):
        # given messagebox with some messages
        messagebox = Messagebox("test")
        with messagebox.open():
            for i in range(3):
                await messagebox.add(MessageTopic("test"), {"a": i})

        # when locking messages and getting them
        # and exception is raised within the context
        with suppress(RuntimeError), messagebox.open():
            for _ in range(3):
                await messagebox.get_next_pending()
            raise RuntimeError

        # then messages are still possible to be retrieved from the messagebox in the original order
        messages = []
        with messagebox.open():
            while message := await messagebox.get_next_pending():
                messages.append(message)
        assert [msg["payload"] for msg in messages] == [{"a": 0}, {"a": 1}, {"a": 2}]

    async def test_add_and_get_multiple_messages_in_order(self):
        # given empty messagebox
        messagebox = Messagebox("test")

        # when adding multiple messages
        with messagebox.open():
            messages_topics = ["test_message_1", "test_message_2", "test_message_3"]
            for message_topic in messages_topics:
                await messagebox.add(MessageTopic(message_topic), {})

            # and getting all the messages
            messages = []
            while message := await messagebox.get_next_pending():
                messages.append(message)

        # then messages are returned in the same order as they were added
        assert [msg["topic"] for msg in messages] == [MessageTopic(m_name) for m_name in messages_topics]


@pytest.mark.asyncio()
async def test_inbox_add_and_get_idempotent():
    # given inbox with a stored message
    inbox = Inbox("test")
    with inbox.open():
        await inbox.add_idempotent(MessageTopic("test_message_1"), {}, "test_idempotent_id")

        # when adding a message with the same idempotent_id
        await inbox.add_idempotent(MessageTopic("test_message_2"), {}, "test_idempotent_id")

        # then message is not added
        messages = []
        while message := await inbox.get_next_pending():
            messages.append(message)
        assert [_excluding_created_at(msg) for msg in messages] == [
            {"topic": MessageTopic("test_message_1"), "payload": {}, "status": "pending"}
        ]
