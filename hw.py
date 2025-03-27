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
  endpoint_cfg = pj.EpConfig()
  endpoint_cfg.uaConfig.threadCount = 0
  endpoint_cfg.logConfig.level = 5
  endpoint_cfg.uaConfig.maxCalls = 4


  endpoint = pj.Endpoint()
  endpoint.libCreate()
  endpoint.libInit(endpoint_cfg)

  sip_transport_cfg = pj.TransportConfig()
  sip_transport_cfg.port = port
  endpoint.transportCreate(pj.PJSIP_TRANSPORT_UDP, sip_transport_cfg)

  endpoint.libStart()

  account_cfg = pj.AccountConfig()

  account_cfg.idUri = f'I-{username} <sip:{username}@{domain}>'
  account_cfg.regConfig.registrarUri = f'sip:{username}@{domain}'
  cred = pj.AuthCredInfo('digest', '*', username, 0, password)
  account_cfg.sipConfig.authCreds.append(cred)

  account = Account()
  print('*' * 500)

  account.create(account_cfg)

  print('*' * 500)

  time.sleep(10)

  print('*' * 500)
  endpoint.libDestroy()
  del endpoint, account


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

