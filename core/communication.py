import uuid
import asyncio
from spade.message import Message
from spade.template import Template


class CommunicationManager:
    def __init__(self, behaviour):
        self.behaviour = behaviour
        self.agent = behaviour.agent

    async def query(self, target_id, query_data, protocol="SPADE", timeout=30, wait_for_response=True, performative='query'):
        conv_id = str(uuid.uuid4())
        if protocol.upper() == "SPADE":
            await self._send_spade(target_id, query_data, conv_id, performative)
            if wait_for_response:
                response_task = self._receive_spade(conv_id, timeout)

        elif protocol.upper() == "SPADELLM":
            await self._send_spade_llm(target_id, query_data, conv_id)
            if wait_for_response:
                response_task = self._receive_spade(conv_id, timeout)

        return await response_task if wait_for_response else conv_id

    async def _send_spade(self, to_jid, body, conv_id, performative):
        """Trimite un mesaj SPADE standard."""
        msg = Message(to=str(to_jid))
        msg.body = body
        msg.thread = conv_id
        msg.set_metadata("performative", performative)
        await self.behaviour.send(msg)

    async def _send_spade_llm(self, to_jid, body, conv_id):
        """Trimite un mesaj SPADE special pentru LLM."""
        msg = Message(to=str(to_jid))
        msg.body = body
        msg.thread = conv_id
        msg.set_metadata("message_type", "llm")
        msg.set_metadata("performative", "request")
        await self.behaviour.send(msg)

    async def _receive_spade(self, conv_id, timeout):
        """Primeste un mesaj SPADE cu un anumit thread (conv_id)."""
        template = Template()
        template.thread = conv_id
        self.behaviour.set_template(template)
        msg = await self.behaviour.receive(timeout=timeout)

        return msg.body if msg else None