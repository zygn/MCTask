from simulator import MCTaskSimulator, multi_main
from mcTasks import MCTaskSet
from matplotlib import pyplot as plt 

class Runner:

    def __init__(self, N=100, HI_N=4, LO_N=4, C=0.2, max_u=1.2, min_u=1.0, max_T_HI=15, min_T_HI=1, max_T_LO=30, min_T_LO=15,  max_lcm=10000):
        self.max_utilization = max_u
        self.min_utilization = min_u
        self.max_T_HI = max_T_HI
        self.min_T_HI = min_T_HI
        self.max_T_LO = max_T_LO
        self.min_T_LO = min_T_LO
        self.c = C
        self.max_lcm = max_lcm
        self.N = N
        self.HI_N = HI_N
        self.LO_N = LO_N

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, self.__dict__)


def main(info: [], scheduler="edf"):
    run: Runner
    for run in info:

        taskset = MCTaskSet(
            run.max_utilization,
            run.min_utilization,
            run.max_T_HI,
            run.min_T_HI,
            run.max_T_LO,
            run.min_T_LO,
            run.c,
            scheduler=scheduler
        )
        tasks = taskset.create_taskset(run.N, run.HI_N, run.LO_N)
        if len(tasks) == run.N:
            passed, failed = multi_main(obj=tasks, scheduler=scheduler)
            print(run, passed, failed)
        else:
            print(run, "taskset creation failed")



if __name__ == "__main__":

    run_edf = [
        Runner(HI_N=1, LO_N=1, max_u=1.2, min_u=1.0, max_T_HI=10, min_T_HI=5, max_T_LO=30, min_T_LO=20),
        Runner(HI_N=2, LO_N=2, max_u=1.2, min_u=1.0, max_T_HI=10, min_T_HI=5, max_T_LO=30, min_T_LO=20),
        Runner(HI_N=3, LO_N=3, max_u=1.2, min_u=1.0, max_T_HI=10, min_T_HI=5, max_T_LO=30, min_T_LO=20),
        Runner(HI_N=4, LO_N=4, max_u=1.2, min_u=1.0, max_T_HI=10, min_T_HI=5, max_T_LO=30, min_T_LO=20),
        Runner(HI_N=5, LO_N=5, max_u=1.2, min_u=1.0, max_T_HI=10, min_T_HI=5, max_T_LO=30, min_T_LO=20),

        Runner(HI_N=1, LO_N=2, max_u=1.2, min_u=1.0, max_T_HI=10, min_T_HI=5, max_T_LO=30, min_T_LO=20),
        Runner(HI_N=2, LO_N=4, max_u=1.2, min_u=1.0, max_T_HI=10, min_T_HI=5, max_T_LO=30, min_T_LO=20),
        Runner(HI_N=3, LO_N=6, max_u=1.2, min_u=1.0, max_T_HI=10, min_T_HI=5, max_T_LO=30, min_T_LO=20),
        Runner(HI_N=4, LO_N=8, max_u=1.2, min_u=1.0, max_T_HI=10, min_T_HI=5, max_T_LO=30, min_T_LO=20),
        Runner(HI_N=5, LO_N=10, max_u=1.2, min_u=1.0, max_T_HI=10, min_T_HI=5, max_T_LO=30, min_T_LO=20),

        Runner(HI_N=1, LO_N=3, max_u=1.2, min_u=1.0, max_T_HI=10, min_T_HI=5, max_T_LO=30, min_T_LO=20),
        Runner(HI_N=2, LO_N=6, max_u=1.2, min_u=1.0, max_T_HI=10, min_T_HI=5, max_T_LO=30, min_T_LO=20),
        Runner(HI_N=3, LO_N=9, max_u=1.2, min_u=1.0, max_T_HI=10, min_T_HI=5, max_T_LO=30, min_T_LO=20),
        Runner(HI_N=4, LO_N=12, max_u=1.2, min_u=1.0, max_T_HI=10, min_T_HI=5, max_T_LO=30, min_T_LO=20),
        Runner(HI_N=5, LO_N=15, max_u=1.2, min_u=1.0, max_T_HI=10, min_T_HI=5, max_T_LO=30, min_T_LO=20),



    ]

    run_rm = [
        Runner(HI_N=1, LO_N=1, max_u=0.9, min_u=0.8, max_T_HI=10, min_T_HI=5, max_T_LO=30, min_T_LO=20),
        Runner(HI_N=2, LO_N=2, max_u=0.9, min_u=0.8, max_T_HI=10, min_T_HI=5, max_T_LO=30, min_T_LO=20),
        Runner(HI_N=3, LO_N=3, max_u=0.9, min_u=0.8, max_T_HI=10, min_T_HI=5, max_T_LO=30, min_T_LO=20),
        Runner(HI_N=4, LO_N=4, max_u=0.9, min_u=0.8, max_T_HI=10, min_T_HI=5, max_T_LO=30, min_T_LO=20),
        Runner(HI_N=5, LO_N=5, max_u=0.9, min_u=0.8, max_T_HI=10, min_T_HI=5, max_T_LO=30, min_T_LO=20),
        Runner(HI_N=1, LO_N=2, max_u=0.9, min_u=0.8, max_T_HI=10, min_T_HI=5, max_T_LO=30, min_T_LO=20),
        Runner(HI_N=2, LO_N=4, max_u=0.9, min_u=0.8, max_T_HI=10, min_T_HI=5, max_T_LO=30, min_T_LO=20),
        Runner(HI_N=3, LO_N=6, max_u=0.9, min_u=0.8, max_T_HI=10, min_T_HI=5, max_T_LO=30, min_T_LO=20),
        Runner(HI_N=4, LO_N=8, max_u=0.9, min_u=0.8, max_T_HI=10, min_T_HI=5, max_T_LO=30, min_T_LO=20),
        Runner(HI_N=5, LO_N=10, max_u=0.9, min_u=0.8, max_T_HI=10, min_T_HI=5, max_T_LO=30, min_T_LO=20),
    ]
    run_rm = [
        Runner(HI_N=1, LO_N=3, max_u=0.9, min_u=0.8, max_T_HI=10, min_T_HI=5, max_T_LO=30, min_T_LO=20),
        Runner(HI_N=2, LO_N=6, max_u=0.9, min_u=0.8, max_T_HI=10, min_T_HI=5, max_T_LO=30, min_T_LO=20),
        Runner(HI_N=3, LO_N=9, max_u=0.9, min_u=0.8, max_T_HI=10, min_T_HI=5, max_T_LO=30, min_T_LO=20),
        Runner(HI_N=4, LO_N=12, max_u=0.9, min_u=0.8, max_T_HI=10, min_T_HI=5, max_T_LO=30, min_T_LO=20),
        Runner(HI_N=5, LO_N=15, max_u=0.9, min_u=0.8, max_T_HI=10, min_T_HI=5, max_T_LO=30, min_T_LO=20),

    ]

    main(run_rm, scheduler="rm")


    

