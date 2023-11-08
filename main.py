import random


class MCTask:

    def __init__(self, T_HI, T_LO, C, mode):
        self.T_HI = int(T_HI)
        self.T_LO = int(T_LO)
        self.C = int(C)
        self.mode = mode

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
            if task.mode == "HI":
                u_hi = task.C / task.T_HI
                u_hihi += u_hi
            elif task.mode == "LO":
                u_lo = task.C / task.T_LO
                u_lolo += u_lo

        return u_lolo + u_hihi

    def gen_random_task(self, mode):
        if mode == "HI":
            t_hi = random.randint(self.min_T_HI, self.max_T_HI)
            t_lo = t_hi * 2
            c = int(t_lo * self.c)
        else:
            t_lo = random.randint(self.min_T_HI, self.max_T_HI)
            t_hi = t_lo * 2
            c = int(t_lo * self.c)

        if c == 0:
            c = 1

        return MCTask(t_hi, t_lo, c, mode)

    def gen_random_taskset(self):
        t1 = self.gen_random_task("HI")
        t2 = self.gen_random_task("HI")
        t3 = self.gen_random_task("LO")
        t4 = self.gen_random_task("LO")
        t5 = self.gen_random_task("HI")
        t6 = self.gen_random_task("HI")

        return [t1, t2, t3, t4, t5, t6]

    def main(self):
        while True:
            tasks = self.gen_random_taskset()
            u = self.calc_utilization(tasks)

            if 1.4 > u > 1.0:
                print(u, tasks)


app = MCTaskSet()
app.main()
