from pkg_resources import iter_entry_points
from threading import Thread
from Queue import Queue

ENTRY_POINT_GROUP = "weather.sources"

def _make_thread_func(ep, location, out_queue):
    def _nop():
        func = ep.load()
        for report in func(location):
            report['source'] = ep.name
            out_queue.put(report)
    return _nop

def reports_by_location(location):
    queue = Queue()
    threads = []
    for ep in iter_entry_points(ENTRY_POINT_GROUP):
        func = _make_thread_func(ep, location, queue)
        t = Thread(target=func)
        t.daemon = True
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    reports = []
    while True:
        if queue.empty():
            break
        reports.append(queue.get())
    return sorted(reports, key=lambda x: x.get('time_from'))

def cmdline():
    import pprint
    import sys
    pprint.pprint(reports_by_location(" ".join(sys.argv[1:])))
