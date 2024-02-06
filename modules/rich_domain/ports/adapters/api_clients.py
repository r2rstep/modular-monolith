import injector

from commons.message_bus.message_bus import MessageBus
from modules.crud.interface import GetCrudData
from modules.rich_domain.ports.api_clients import CrudApiClient, CrudData


class MessageBusCrudApiClient(CrudApiClient):
    @injector.inject
    def __init__(self, message_bus: MessageBus):
        self._message_bus = message_bus

    async def get_crud_data(self) -> CrudData:
        data: GetCrudData.Result = await self._message_bus.query(GetCrudData())
        return CrudData(str(data.a))
