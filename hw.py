import pjsua2 as pj
import time

from environs import Env


class Account(pj.Account):
    def onRegState(self, prm):
        print('***OnRegState: ' + prm.reason)


def pjsua2_test(
    username: str,
    password: str,
    domain: str,
    port: int,
):
    ep_cfg = pj.EpConfig()
    ep_cfg.uaConfig.threadCount = 0
    ep_cfg.logConfig.level = 5
    ep_cfg.uaConfig.maxCalls = 4

    ep = pj.Endpoint()
    ep.libCreate()
    ep.libInit(ep_cfg)

    t_cfg = pj.TransportConfig()
    t_cfg.port = port
    ep.transportCreate(pj.PJSIP_TRANSPORT_UDP, t_cfg)

    ep.libStart()

    acc_cfg = pj.AccountConfig()
    acc_cfg.idUri = f'I-{username} <sip:{username}@{domain}>'
    acc_cfg.regConfig.registrarUri = f'sip:{domain}'
    cred = pj.AuthCredInfo('digest', '*', username, 0, password)
    acc_cfg.sipConfig.authCreds.append(cred)

    acc = Account()
    acc.create(acc_cfg)

    time.sleep(100)

    ep.libDestroy()
    del ep, acc


if __name__ == '__main__':
    env = Env()
    env.read_env()
    sip_domain = env.str('SIP_DOMAIN')
    sip_port = env.int('SIP_PORT')
    sip_username = env.str('SIP_USERNAME')
    sip_password = env.str('SIP_PASSWORD')
    called_number = env.str('CALL_NUMBER')

    pjsua2_test(
        username=sip_username,
        password=sip_password,
        domain=sip_domain,
        port=sip_port,
    )

