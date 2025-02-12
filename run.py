import logging
from datetime import datetime, UTC

import asyncio

from environs import Env
from pathlib import Path, PurePath
from PySIP.sip_account import SipAccount, SipCall


async def call_out(called_number: str, account: SipAccount):
    await account.register()

    call = account.make_call(called_number)

    call_task = asyncio.create_task(call.start())

    await call_task
    await call.call_handler.hangup()
    await account.unregister()

def main():
    env = Env()
    env.read_env()
    sip_domain = env.str("SIP_DOMAIN")
    sip_server_port = env.int("SIP_SERVER_PORT")
    sip_username = env.str("SIP_USERNAME")
    sip_password = env.str("SIP_PASSWORD")
    called_number = env.str("CALL_NUMBER")

    account = SipAccount(
        username=sip_username,
        password=sip_password,
        hostname=sip_domain,
        connection_type='UDP',
    )

    asyncio.run(call_out(called_number, account))


if __name__ == '__main__':
    logs_dir = Path(f'logs')
    logs_dir.mkdir(parents=True, exist_ok=True)
    start_at = datetime.strftime(datetime.now(UTC), "%Y%m%d_%H%M%S_utc")

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'logs/{start_at}.log'),
        ]
    )

    main()


