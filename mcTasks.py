import random
import pickle
import time


class MCTask:

    def __init__(self, T_HI, T_LO, C, X):
        self.T_HI = int(T_HI)
        self.T_LO = int(T_LO)
        self.C = int(C)
        self.X = X
        self.deadline = 0


    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, self.__dict__)


class MCTaskSet:

    def __init__(self, max_u=1.2, min_u=1.0, max_T_HI=15, min_T_HI=1, max_T_LO=30, min_T_LO=15, c=0.2):
        self.max_utilization = max_u
        self.min_utilization = min_u
        self.max_T_HI = max_T_HI
        self.min_T_HI = min_T_HI
        self.max_T_LO = max_T_LO
        self.min_T_LO = min_T_LO
        self.c = c

    def calc_utilization(self, tasks):
        task: MCTask
        u_lolo = 0
        u_hihi = 0

        for task in tasks:
            if task.X == "HI":
                u_hi = task.C / task.T_HI
                u_hihi += u_hi
            elif task.X == "LO":
                u_lo = task.C / task.T_LO
                u_lolo += u_lo

        return u_lolo + u_hihi

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

    def create_taskset(self, n=100, hi=3, lo=3):
        memory = []
        while True:
            tasks = self.gen_random_taskset(hi, lo)
            u = self.calc_utilization(tasks)

            # check same tasks
            if self.max_utilization >= u >= self.min_utilization:
                if tasks in memory:
                    continue
                else:
                    memory.append(tasks)
                    print(u, tasks)

            if len(memory) == n:
                break
        return memory

    def export_taskset(self, tasks):
        with open("taskset_{}.pkl".format(round(time.time())), "wb") as f:
            pickle.dump(tasks, f)

    def import_taskset(self, filename):
        with open(filename, "rb") as f:
            return pickle.load(f)



if __name__ == "__main__":
    app = MCTaskSet(
        max_T_HI=5,
        min_T_HI=2,
        max_T_LO=10,
        min_T_LO=7,
        c=0.2
    )
    mem = app.create_taskset(1, 2, 3)
    app.export_taskset(mem)
    # mem = app.import_taskset("")
    print(mem)
