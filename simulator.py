import math
import copy
import time
from tqdm import tqdm
from collections import deque
from typing import Optional
from mcTasks import MCTask, MCTaskSet

class ModeSchedule:

    def __init__(self, time, mode):
        self.time = time
        self.mode = mode


class MCTaskSimulator:

    def __init__(self):
        self.current_mode = "LO"
        self.current_time = 0
        self.current_task = None
        self.job_queue = []
        self.mode_schedule = deque()

    def reset(self):
        self.current_mode = "LO"
        self.current_time = 0
        self.current_task = None
        self.job_queue = []
        self.mode_schedule = deque()

    def tasks_lcm(self, tasks):
        # calculate T_LOs LCM
        task: MCTask
        lcm = 1
        for task in tasks:
            lcm = lcm * task.T_LO // math.gcd(lcm, task.T_LO)
        return lcm

    def release_task(self, task: list) -> Optional[list]:

        if self.current_mode == "HI":
            if self.current_time == 0:
                task[1].deadline = self.current_time + task[1].T_HI
                return task
            elif self.current_time % task[1].T_HI == 0:
                task[1].deadline = self.current_time + task[1].T_HI
                return task

        elif self.current_mode == "LO":
            if self.current_time == 0:
                task[1].deadline = self.current_time + task[1].T_LO
                return task
            elif self.current_time % task[1].T_LO == 0:
                task[1].deadline = self.current_time + task[1].T_LO
                return task

        return None

    def set_mode_change(self, schedule: ModeSchedule):
        self.mode_schedule.append(schedule)

    def mode_change(self):
        if len(self.mode_schedule) == 0:
            return

        if self.mode_schedule[0].time <= self.current_time:
            mc = self.mode_schedule.popleft()
            # print("Mode Changed {}->{} when {}".format(self.current_mode, mc.mode, self.current_time))
            self.current_mode = mc.mode

        return

    def simulate(self, tasks):
        t0 = time.time()
        lcm = self.tasks_lcm(tasks)
        u = MCTaskSet().calc_utilization(tasks)

        tasks = [[i + 1, task] for i, task in enumerate(tasks)]
        # print("Scheduling tasks: \n\t" + "\n\t".join([f"{task}" for task in tasks]))
        # print("LCM: " + str(lcm))
        # print("Utilization: " + str(u))
        # print("Start simulation...")
        # print("Current time: " + str(self.current_time) + " Mode: " + self.current_mode)

        while self.current_time < lcm:

            # task release
            for task in tasks:
                t = copy.deepcopy(task)
                released_task = self.release_task(t)

                if released_task is not None:
                    self.job_queue.append(t)
                    # print(f"\t\t{t[0]} Task released {t[1]}")

            # 1sec spend
            self.current_time += 1
            # check scheduled mode change
            self.mode_change()

            # print("Current time: " + str(self.current_time) + " Mode: " + self.current_mode)

            # early deadline first
            self.job_queue = sorted(self.job_queue, key=lambda x: x[1].deadline)
            for i in range(len(self.job_queue)):
                task = self.job_queue[i]

                # deadline missed
                if task[1].deadline < self.current_time:
                    print()
                    print(f"\t\tTask {task[0]} missed {task[1]}")

                    print("Scheduling tasks: \n\t" + "\n\t".join([f"{pt}" for pt in tasks]))
                    print("Jobs: \n\t" + "\n\t".join([f"{pj}" for pj in self.job_queue]))
                    print("LCM: " + str(lcm))
                    print("Utilization: " + str(u))
                    print("Current time: " + str(self.current_time) + " Mode: " + self.current_mode)

                    raise Exception(f"Task missed deadline when time {self.current_time}")
                # task 1sec spend
                task[1].C -= 1
                if task[1].C == 0:
                    self.job_queue.remove(task)
                    # print(f"\t\t{task[0]} Task finished {task[1]}")
                break

        # print("Task scheduled successfully ({:.3f}s)".format(time.time()-t0))
        # print("----------------------------------------------")

if __name__ == "__main__":
    app = MCTaskSimulator()
    taskset = MCTaskSet(
        max_T_HI=5,
        min_T_HI=2,
        max_T_LO=10,
        min_T_LO=7,
        max_u=1.15,
        c=0.2
    )

    tasks = taskset.create_taskset(n=1000, hi=2, lo=4)
    # taskset.export_taskset(tasks)
    # tasks = taskset.import_taskset("taskset_1699859989.pkl")

    fail_count = 0

    pass_count = 0
    for task in tqdm(tasks):
        for t in task:
            if t.X == "HI":
                app.current_mode = "LO"
                app.set_mode_change(ModeSchedule(t.T_HI, "HI"))
            else:
                app.current_mode = "HI"
                app.set_mode_change(ModeSchedule(t.T_HI, "LO"))
            try:
                app.simulate(task)
                pass_count += 1
            except Exception as e:
                fail_count += 1
                print(e)
            app.reset()


    print()
    print("Total:", pass_count+fail_count , "Fail:", fail_count, "Success:", pass_count, "Ratio:", pass_count/(pass_count+fail_count))
