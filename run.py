from app.main import create_app
import asyncio

app = create_app()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.run(debug=True))
