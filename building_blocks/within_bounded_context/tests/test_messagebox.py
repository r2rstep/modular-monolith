import pytest

from building_blocks.within_bounded_context.infrastructure.messagebox import (
    MessageBox,
    MessageDTO,
    MessageName,
)


@pytest.mark.asyncio()
class TestMessageBox:
    async def test_add_and_get_message(self):
        # given empty message_box
        message_box = MessageBox("test")

        # when adding a message
        await message_box.add(MessageName("test_message"), {"field_a": "value_a", "field_b": "value_b"})
        # and getting the message
        message = await message_box.get_next()

        # then message's name and payload are correct
        assert message == MessageDTO(MessageName("test_message"), {"field_a": "value_a", "field_b": "value_b"})
        # and message_box is empty
        assert await message_box.get_next() is None

    async def test_add_and_get_multiple_messages(self):
        # given empty message_box
        message_box = MessageBox("test")

        # when adding multiple messages
        messages_names = ["test_message_1", "test_message_2", "test_message_3"]
        for message_name in messages_names:
            await message_box.add(MessageName(message_name), {})

        # and getting all the messages
        messages = []
        while message := await message_box.get_next():
            messages.append(message)

        # then messages are returned in the same order as they were added
        assert [msg.name for msg in messages] == [MessageName(m_name) for m_name in messages_names]
