from os_daemon import OsDaemon
from eval_util import EvalResult, eval_case


@eval_case('sleep test 01 with 100 which should success')
def sleep_test_01(osd: OsDaemon) -> EvalResult:
    text = '100'
    res = osd.exec(f'sleep {text}', 5)

    if 1 <= res.time_spent <= 1.5:
        return EvalResult(True)

    return EvalResult(False, f'mismatch with {res.stdout}')


@eval_case('sleep test 02 with 5678 which should success')
def sleep_test_02(osd: OsDaemon) -> EvalResult:
    res = osd.exec(f'sleep', 1)
    if not res.time_spent:
        return EvalResult(False, 'Timeout')

    if len(res.stdout) != 0:
        return EvalResult(True)

    return EvalResult(False, f'Output mismatch')


@eval_case('pingpong test 01 which should success')
def pingpong_test_01(osd: OsDaemon) -> EvalResult:
    res = osd.exec(f'pingpong', 5)
    if not res.time_spent:
        return EvalResult(False, 'Timeout')
    if len(res.stdout) == 2 and res.stdout[0].find('ping') != 1 and res.stdout[1].find('pong') != -1:
        return EvalResult(True)

    return EvalResult(False, f'Output mismatch {res.stdout}')


@eval_case('find test 01 which should success')
def find_test_01(osd: OsDaemon) -> EvalResult:
    text = '. grep'
    res = osd.exec(f'find {text}', 2)
    if not res.time_spent:
        return EvalResult(False, 'Timeout')
    if len(res.stdout) != 0:
        for line in res.stdout:
            if 'grep' not in line:
                return EvalResult(False, f'Output mismatch {res.stdout}')

    return EvalResult(True)


@eval_case('find test 02 which should success')
def find_test_02(osd: OsDaemon) -> EvalResult:
    text = '. .'
    res = osd.exec(f'find {text}', 2)
    if not res.time_spent:
        return EvalResult(False, 'Timeout')
    if len(res.stdout) != 0:
        return EvalResult(False, f'Output mismatch {res.stdout}')

    return EvalResult(True)


@eval_case('xargs test 01 which should success')
def xargs_test_01(osd: OsDaemon) -> EvalResult:
    res = osd.exec(f'echo hello | xargs echo bye', 2)
    if not res.time_spent:
        return EvalResult(False, 'Timeout')
    if len(res.stdout) != 1 or res.stdout[0] != 'bye hello':
        return EvalResult(False, f'Output mismatch {res.stdout}')

    return EvalResult(True)


@eval_case('xargs test 02 which should success')
def xargs_test_02(osd: OsDaemon) -> EvalResult:
    res = osd.exec(f'echo grep | xargs find .', 2)
    if not res.time_spent:
        return EvalResult(False, 'Timeout')
    if len(res.stdout) != 1 or res.stdout[0] != './grep':
        return EvalResult(False, f'Output mismatch {res.stdout}')

    return EvalResult(True)
