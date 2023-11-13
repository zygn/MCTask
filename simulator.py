import math
import copy
from typing import Optional
from mcTasks import MCTask, MCTaskSet


class MCTaskSimulator:

    def __init__(self):
        self.current_mode = "LO"
        self.current_time = 0
        self.current_task = None
        self.job_queue = []


    def reset(self):
        self.current_mode = "LO"
        self.current_time = 0
        self.current_task = None
        self.job_queue = []

    def tasks_lcm(self, tasks):
        # calculate T_LOs LCM
        task: MCTask
        lcm = 1
        for task in tasks:
            lcm = lcm * task.T_LO // math.gcd(lcm, task.T_LO)
        return lcm

    def release_task(self, task: list) -> Optional[list]:

        if self.current_mode == "HI":
            task[1].deadline = self.current_time + task[1].T_HI
            if self.current_time == 0:
                return task
            elif self.current_time % task[1].T_HI == 0:
                return task

        elif self.current_mode == "LO":
            task[1].deadline = self.current_time + task[1].T_LO
            if self.current_time == 0:
                return task
            elif self.current_time % task[1].T_LO == 0:
                return task

        return None



    # def lowest_deadline(self, tasks) -> Optional[MCTask]:
    #     grab_task = []
    #
    #     for task in tasks:
    #         if task.X == self.current_mode:
    #             grab_task.append(task)
    #
    #     if len(grab_task) == 0:
    #         return None
    #
    #     if self.current_mode == "LO":
    #         grab_task.sort(key=lambda x: x.T_LO)
    #         #####
    #
    #     elif self.current_mode == "HI":
    #         pass
    #
    #     return None


    def simulate(self, tasks):

        lcm = self.tasks_lcm(tasks)
        u = MCTaskSet().calc_utilization(tasks)

        tasks = [[i+1, task] for i, task in enumerate(tasks)]

        mode_change = lcm // 2

        print("Scheduling tasks: \n\t" + "\n\t".join([f"{task}" for task in tasks]))
        print("LCM: " + str(lcm))
        print("Utilization: " + str(u))
        print("")
        print("Start simulation...")
        print("Current time: " + str(self.current_time))
        while self.current_time < lcm:

            if self.current_time >= mode_change:
                self.current_mode = "HI"

            for task in tasks:
                released_task = self.release_task(task)
                t = copy.deepcopy(released_task)
                if t is not None:
                    self.job_queue.append(t)
                    print(f"\t\t{t[0]} Task released {t[1]}")

            self.current_time += 1
            print("Current time: " + str(self.current_time))

            for i in range(len(self.job_queue)):
                task = self.job_queue[i]

                if task[1].deadline < self.current_time:
                    print(f"\t\t{task[0]} Task missed {task[1]}")
                    raise Exception("Task missed deadline")

                task[1].C -= 1
                if task[1].C == 0:
                    self.job_queue.remove(task)
                    print(f"\t\t{task[0]} Task finished {task[1]}")
                break

            # print(self.job_queue)


if __name__ == "__main__":
    app = MCTaskSimulator()
    taskset = MCTaskSet(
        max_T_HI=5,
        min_T_HI=2,
        max_T_LO=10,
        min_T_LO=7,
        c=0.2
    )

    # tasks = taskset.create_taskset(n=1, hi=2, lo=4)
    tasks = taskset.import_taskset("taskset_1699800316.pkl")

    for task in tasks:
        app.simulate(task)
        app.reset()
