import psutil

def find_procs_by_name(name):
    "Return a list of processes matching 'name'."
    ls = []
    for p in psutil.process_iter(attrs=['name']):
        if p.info['name'] == name:
            ls.append(p)
    return ls

if __name__ == '__main__':
    print('boot running ...')

    # print('PIDs : ', psutil.pids())

    print(find_procs_by_name('python'))

    print('Done!')