import signal

import psutil

def find_procs_by_name(name):
    "Return a list of processes matching 'name'."
    ls = []
    for p in psutil.process_iter(attrs=['name']):
        if name in p.info['name']:
            ls.append(p)
    return ls

if __name__ == '__main__':
    print('boot running ...')

    # print('PIDs : ', psutil.pids())

    pids = find_procs_by_name('fcserver')
    print(pids)

    # TODO : This should be a loop running through them all 
    if len(pids) != 0:
        pids[0].send_signal(signal.SIGTERM)

    pids = find_procs_by_name('fcserver')
    print(pids)

    print('Done!')
