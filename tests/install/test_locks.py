#!/usr/bin/python3

import multiprocessing as mp
import threading

import pytest

import solcxir


class ThreadWrap:
    def __init__(self, fn, *args, **kwargs):
        self.exc = None
        self.t = threading.Thread(target=self.wrap, args=(fn,) + args, kwargs=kwargs)
        self.t.start()

    def wrap(self, fn, *args, **kwargs):
        try:
            fn(*args, **kwargs)
        except Exception as e:
            self.exc = e

    def join(self):
        self.t.join()
        if self.exc is not None:
            raise self.exc


@pytest.mark.skipif("'--no-install' in sys.argv")
def test_threadlock(nosolc):
    threads = [ThreadWrap(solcxir.install_solc, "0.6.9") for i in range(4)]
    for t in threads:
        t.join()


@pytest.mark.skipif("'--no-install' in sys.argv")
def test_processlock(nosolc):
    # have to use a context here to prevent a conflict with tqdm
    ctx = mp.get_context("spawn")
    threads = [ctx.Process(target=solcxir.install_solc, args=("0.6.9",)) for i in range(4)]
    for t in threads:
        t.start()
    solcxir.install_solc("0.6.9")
    for t in threads:
        t.join()
        assert t.exitcode == 0
