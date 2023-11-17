import random
import pickle
import time
from tqdm import tqdm
import math 


class MCTask:

    def __init__(self, T_HI, T_LO, C, X):
        self.T_HI = int(T_HI)
        self.T_LO = int(T_LO)
        self.C = int(C)
        self.X = X
        self.deadline = 0
        self.released_mode = "LO"


    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, self.__dict__)


class MCTaskSet:

    def __init__(self, max_u=1.2, min_u=1.0, max_T_HI=15, min_T_HI=1, max_T_LO=30, min_T_LO=15, c=0.2, max_lcm=10000):
        self.max_utilization = max_u
        self.min_utilization = min_u
        self.max_T_HI = max_T_HI
        self.min_T_HI = min_T_HI
        self.max_T_LO = max_T_LO
        self.min_T_LO = min_T_LO
        self.c = c
        self.max_lcm = max_lcm
        self.taskset = []
        self.not_hit = 0

    def calc_utilization(self, tasks):
        task: MCTask
        u_lolo = 0
        u_lohi = 0
        u_hihi = 0
        u_hilo = 0

        for task in tasks:
            if task.X == "HI":
                u_hi = task.C / task.T_HI
                u_lo = task.C / task.T_LO
                u_lohi += u_lo
                u_hihi += u_hi
            elif task.X == "LO":
                u_lo = task.C / task.T_LO
                u_hi = task.C / task.T_HI
                u_hilo += u_hi
                u_lolo += u_lo

        return [u_lolo + u_lohi, u_lohi + u_hihi, u_lolo + u_hihi]

    def gen_random_task(self, mode):
        if mode == "HI":
            t_hi = random.randint(self.min_T_HI, self.max_T_HI)
            t_lo = t_hi * 2
            c = int(t_lo * self.c)
        else:
            t_lo = random.randint(self.min_T_LO, self.max_T_LO)
            t_hi = t_lo * 2
            c = int(t_lo * self.c)

        if c == 0:
            c = 1

        return MCTask(t_hi, t_lo, c, mode)

    def gen_random_taskset(self, hi=3, lo=3):
        tasks = []
        hi_count = 0
        lo_count = 0
        for _ in range(int(hi+lo)):
            if hi_count < hi:
                tasks.append(self.gen_random_task("HI"))
                hi_count += 1
                continue

            if lo_count < lo:
                tasks.append(self.gen_random_task("LO"))
                lo_count += 1
                continue

        return tasks
    
    def tasks_lcm(self, tasks):
        # calculate T_LOs LCM
        task: MCTask
        lcm = 1
        for task in tasks:
            lcm = lcm * task.T_LO // math.gcd(lcm, task.T_LO)
        return lcm

    def create_taskset(self, n=100, hi=3, lo=3):
        pbar = tqdm(total=n)
        memory = []
        while True:
            if self.not_hit > 100:
                self.c -= 0.01
                self.not_hit = 0
            
            if self.c <= 0.0:
                self.c = 1.0

            tasks = self.gen_random_taskset(hi, lo)
            
            u = self.calc_utilization(tasks)
            # print(u)
            if self.tasks_lcm(tasks) > self.max_lcm:
                continue

            # check same tasks
            if (self.max_utilization >= u[2] >= self.min_utilization) and u[0] <= 1 and u[1] <= 1:
                if tasks in memory:
                    continue
                else:
                    memory.append(tasks)
                    self.not_hit = 0
                    pbar.update(1)
                    # print(u, tasks)
            else:
                self.not_hit += 1

            if len(memory) == n:
                pbar.close()
                break

        self.taskset = memory
        return memory

    def export_taskset(self, name):
        with open(f"taskset_{name}.pkl", "wb") as f:
            pickle.dump(self.taskset, f)

    def import_taskset(self, filename):
        with open(filename, "rb") as f:
            return pickle.load(f)



if __name__ == "__main__":
    app = MCTaskSet(
        max_T_HI=10,
        min_T_HI=5,
        max_T_LO=30,
        min_T_LO=20,
        min_u=1.2,
        max_u=1.3,
        c=0.17
    )
    mem = app.create_taskset(100, 3, 5)
    app.export_taskset("u1.2-1.3")
    # mem = app.import_taskset("/home/yundo/Workspace/MCTask/taskset_u1.3-1.4.pkl")
    
    for i in mem:
        print(i)

