import asyncio
import json

from spade import wait_until_finished
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.agent import Agent
from spade.template import Template
from spade.message import Message

from core.communication import CommunicationManager

class ReceiverAgent(Agent):
    class RecvBehav(CyclicBehaviour):
        async def on_start(self):
            self.comm = CommunicationManager(self)
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                print(f'Mesaj primit: {msg.body}')
                msg_type = msg.metadata.get("performative")
                if msg_type == 'request':
                    raspuns_llm = await self.comm.query(
                        protocol = 'SPADELLM',
                        target_id = 'llm_agent@localhost',
                        query_data = msg.body,
                        timeout=45
                    )
                    if raspuns_llm:
                        print(f'Raspuns LLM primit: {raspuns_llm}')
                        raspuns_llm = json.loads(raspuns_llm)
                        tool_call = await self.comm.query(
                            protocol = 'MCP',
                            tool_name = raspuns_llm['tool_name'],
                            parameters = raspuns_llm['parameters'],
                            base_url = 'http://localhost:8000'
                        )
                        print(f'Rezultat apel tool: {tool_call}')
            else:
                print(f"Niciun mesaj primit in ultimele 10 de secunde.")

    async def setup(self):
        print(f"Agentul Receiver {self.jid} porneste.")
        self.add_behaviour(self.RecvBehav())

async def main():
    receiver = ReceiverAgent("simple_agent@localhost", "pass")
    await receiver.start(auto_register=True)
    print("Agentul Receiver este pornit")
    await wait_until_finished(receiver)


if __name__ == "__main__":
    asyncio.run(main())