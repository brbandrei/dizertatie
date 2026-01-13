import random

import spade
from spade.behaviour import PeriodicBehaviour, CyclicBehaviour
from spade.message import Message
import asyncio

from core.communication import CommunicationManager


class Sender(spade.agent.Agent):
    class Send(CyclicBehaviour):
        async def on_start(self):
            self.comm = CommunicationManager(self)
        async def run(self):
            tool = input("Introdu o cerere pentru agent: ")
            msg = await self.comm.query(
                protocol='SPADE',
                target_id='simple_agent@localhost',
                query_data=tool,
                performative='request',
                timeout=45,
                wait_for_response=False
            )
            if msg:
                print(f'Mesaj trimis: {tool}')

    async def setup(self):
        print('Agentul a pornit')
        await asyncio.sleep(2)
        b = self.Send()
        self.add_behaviour(b)


async def main():
    sender = Sender("client@localhost", "pass")
    await sender.start(auto_register=True)
    await spade.wait_until_finished(sender)
    print("Agentul Client s-a oprit.")

if __name__ == "__main__":
    asyncio.run(main())