import pytest

from commons.messagebox.infrastructure.messagebox import Inbox, Messagebox, MessageDTO, MessageTopic


@pytest.mark.asyncio()
class TestMessageBox:
    async def test_add_and_get_message(self):
        # given empty message_box
        message_box = Messagebox("test")

        # when adding a message
        await message_box.add(MessageTopic("test_message"), {"field_a": "value_a", "field_b": "value_b"})
        # and getting the message
        message = await message_box.get_next()

        # then message's name and payload are correct
        assert message == MessageDTO(MessageTopic("test_message"), {"field_a": "value_a", "field_b": "value_b"})
        # and message_box is empty
        assert await message_box.get_next() is None

    async def test_add_and_get_multiple_messages_in_order(self):
        # given empty message_box
        message_box = Messagebox("test")

        # when adding multiple messages
        messages_names = ["test_message_1", "test_message_2", "test_message_3"]
        for message_name in messages_names:
            await message_box.add(MessageTopic(message_name), {})

        # and getting all the messages
        messages = []
        while message := await message_box.get_next():
            messages.append(message)

        # then messages are returned in the same order as they were added
        assert [msg.topic for msg in messages] == [MessageTopic(m_name) for m_name in messages_names]


@pytest.mark.asyncio()
async def test_inbox_add_and_get_idempotent():
    # given inbox with a stored message
    inbox = Inbox("test")
    await inbox.add_idempotent(MessageTopic("test_message_1"), {}, "test_idempotent_id")

    # when adding a message with the same idempotent_id
    await inbox.add_idempotent(MessageTopic("test_message_2"), {}, "test_idempotent_id")

    # then message is not added
    messages = []
    while message := await inbox.get_next():
        messages.append(message)
    assert messages == [MessageDTO(MessageTopic("test_message_1"), {})]
