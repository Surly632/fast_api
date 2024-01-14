from prisma import Prisma

class prisma_connection:
    def __init__(self):
        self.prisma=Prisma()
    
    async def connect(self):
        await self.prisma.connect()
        print(f'Database is connected')
    
    async def disconnect(self):
        await self.prisma.disconnect()
        print(f'database is disconnected')

prima_connection = prisma_connection()
    