from dns_resolver.dns_resolver import DNSResolver
from python_utils.thread_pool import ThreadPool

from datetime import datetime

import gevent
import paramiko


def _get_latency_of_ssh_tunnel(ip, port, print_error=False):
    try:
        with gevent.Timeout(10):
            trans = paramiko.Transport((ip, port))
            trans.close()
        return ip, datetime.now()
    except gevent.timeout.Timeout:
        if print_error:
            print(f'Timeout to establish connection with {ip}:{port}')
    except paramiko.ssh_exception.SSHException:
        raise RuntimeError('SSH server is down, please check !!!')
    return ip, None


def get_accessible_ssh_tunnels(host, port, print_info=False, print_error=False, only_best=False):
    host, port = str(host), int(port)
    pool = ThreadPool(total_thread_number=50, exit_for_any_exception=True)

    ips = DNSResolver().get_ip_list_of_host(host)

    start_time = datetime.now()

    for ip in ips:
        pool.apply_async(_get_latency_of_ssh_tunnel, args=(ip, port), kwds=dict(print_error=print_error))

    if not only_best:
        results = pool.get_results_order_by_time(raise_exception=True)

        accessible_ssh_tunnels = []

        for res in results:
            ip, end_time = res
            if end_time is not None:
                accessible_ssh_tunnels.append(ip)
                if print_info:
                    print(f'{ip} | {(end_time - start_time).total_seconds()}s')
            else:
                if print_error:
                    print(f'{ip} | timeout')

        return accessible_ssh_tunnels
    else:
        results = pool.get_results_order_by_time(raise_exception=True)
        for res in results:
            pool.stop_all()
            ip, end_time = res
            if end_time is not None:
                if print_info:
                    print(f'{ip} | {(end_time - start_time).total_seconds()}s')
                return ip
            else:
                if print_error:
                    print(f'{ip} | timeout')
                return None


if __name__ == '__main__':
    accessible_ssh_tunnels = get_accessible_ssh_tunnels('0.tcp.ngrok.io', 19492, only_best=True)
    print(accessible_ssh_tunnels)
