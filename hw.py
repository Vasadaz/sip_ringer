import time
import pjsua2 as pj
from environs import Env
from pjsua2 import Endpoint


class MyCall(pj.Call):
    def __init__(self, acc: pj.Account, call_id: int = -1):
        super().__init__(acc, call_id)

    def onCallMediaState(self, prm):
        ci = self.getInfo()
        for media in ci.media:
            if media.type == pj.PJMEDIA_TYPE_AUDIO:
                aud_med = pj.AudioMedia.typecastFromMedia(self.getMedia(media.index))
                ep.audDevManager().getCaptureDevMedia().startTransmit(aud_med)
                aud_med.startTransmit(ep.audDevManager().getPlaybackDevMedia())
                print("Аудио подключено.")


class MyAccount(pj.Account):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg

    def onRegState(self, prm):
        print(f"Статус регистрации: код {prm.code}, причина: {prm.reason}")


def main(username: str, password: str, domain: str, port: int, dest_uri: str):
    global ep

    ep = pj.Endpoint()
    ep.libCreate()

    ep_cfg = pj.EpConfig()
    ep.libInit(ep_cfg)

    t_cfg = pj.TransportConfig()
    t_cfg.port = port
    ep.transportCreate(pj.PJSIP_TRANSPORT_UDP, t_cfg)

    ep.libStart()

    ep.audDevManager().setNullDev()
    print("Конечная точка pjsua2 запущена без использования реального аудиоустройства.")

    acc_cfg = pj.AccountConfig()
    acc_cfg.idUri = f'sip:{username}@{domain}'

    acc_cfg.sipConfig.contactUri = f"sip:{username}@{domain}"
    acc_cfg.regConfig.registrarUri = f'sip:{domain}'
    cred = pj.AuthCredInfo("digest", "*", username, 0, password)
    acc_cfg.sipConfig.authCreds.append(cred)

    acc = MyAccount(acc_cfg)
    acc.create(acc_cfg)
    time.sleep(3)

    call = MyCall(acc)
    call_param = pj.CallOpParam(True)
    full_dest_uri = f'sip:{dest_uri}'
    print(f"Выполняется вызов на {full_dest_uri}...")

    try:
        call.makeCall(full_dest_uri, call_param)
    except pj.Error as e:
        print(f"Ошибка при вызове: {e}")
        return

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Завершение программы...")

    ep.libDestroy()


if __name__ == "__main__":
    env = Env()
    env.read_env()
    sip_domain = env.str('SIP_DOMAIN')
    sip_port = env.int('SIP_PORT')
    sip_username = env.str('SIP_USERNAME')
    sip_password = env.str('SIP_PASSWORD')
    called_number = env.str('CALL_NUMBER')
    main(
        username=sip_username,
        password=sip_password,
        domain=sip_domain,
        port=sip_port,
        dest_uri=called_number
    )

