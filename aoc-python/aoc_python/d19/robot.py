from collections import Counter
from dataclasses import dataclass, field
from math import inf
from typing import Dict, List

Material = str
Robot = Material
Cost = Counter[Material]


@dataclass
class Blueprint:
    id: int
    costs: Dict[Material, Cost] = field(default_factory=dict)

    def materials(self):
        return self.costs.keys()

    def get_max_material_production(
        self,
        target_material: Material,
        time_remaining: int,
        robot_count: Counter[Robot],
        material_count: Counter[Material],
        build_order: List[Robot],
        curr_max: int,
    ):
        if material_count[target_material] > curr_max:
            # self.follow_build(build_order)
            # print("Build order:", build_order)
            # print("Material count:", material_count)
            # print("Robots:", robot_count)
            return material_count[target_material]
        elif time_remaining == 0:
            return curr_max

        for robot in self.get_next_materials(target_material, robot_count, build_order):
            time_to_build = self.get_time_to_build_robot(robot, material_count, robot_count)
            if time_to_build >= time_remaining:
                continue
            new_material_count = material_count.copy()
            for r, count in robot_count.items():
                new_material_count[r] += time_to_build * count
            for r, cost in self.costs[robot].items():
                new_material_count[r] -= cost
            best = self.get_max_material_production(
                target_material,
                time_remaining - time_to_build,
                robot_count + Counter({robot: 1}),
                new_material_count,
                build_order + [robot],
                curr_max,
            )
            curr_max = max(best, curr_max)

        # path where we don't build anymore robots
        new_material_count = material_count.copy()
        for r, count in robot_count.items():
            new_material_count[r] += time_remaining * count
        best = self.get_max_material_production(
            target_material, 0, robot_count, new_material_count, build_order, curr_max
        )
        curr_max = max(best, curr_max)
        return curr_max

    def get_next_materials(self, target_material: Material, robot_count: Counter[Robot], build_order: List[Material]):
        # These `if` statements were a YOLO heuristic that happened to work!
        # My idea was that an optimal build order will look almost like a progression
        # from basic ore to the final geode with possibly a small region of overlap
        # when transitioning between robot types. I can't prove that this is correct though.
        overlap = 5
        if len(build_order) < overlap or build_order[-overlap] == "ore":
            to_build = set(self.materials())
        elif build_order[-overlap] == "clay":
            to_build = set(self.materials()) - {"ore"}
        elif build_order[-overlap] == "obsidian":
            to_build = set(self.materials()) - {"ore", "clay"}
        else:
            to_build = set(self.materials()) - {"ore", "clay", "obsidian"}

        for material in self.materials():
            max_needed = max([x[material] for x in self.costs.values() if x != "ore"])
            if robot_count[material] >= max_needed and material in to_build:
                to_build.remove(material)
        to_build.add(target_material)
        return to_build

    def debug_follow_build(self, build_order: List[Material], time_left: int = 24):
        robot_count = Counter({"ore": 1})
        material_count: Counter[Material] = Counter()
        for robot in build_order:
            time_to_build = self.get_time_to_build_robot(robot, material_count, robot_count)
            print("Build order:", build_order)
            print("Materials:", material_count)
            print("Robots:", robot_count)
            print(f"Considering {robot} for next robot")
            print("Time left:", time_left)
            print("Time to build:", time_to_build)
            breakpoint()
            for r, c in robot_count.items():
                material_count[r] += time_to_build * c
            for r, price in self.costs[robot].items():
                material_count[r] -= price
            robot_count[robot] += 1
            time_left -= time_to_build
        print("Build order:", build_order)
        print("Materials:", material_count)
        print("Robots:", robot_count)
        print("Time left:", time_left)
        breakpoint()

    def get_time_to_build_robot(self, robot: Robot, material_count: Counter[Material], robot_count: Counter[Robot]):
        build_time = 1
        materials = material_count.copy()
        if any(robot_count[r] <= 0 for r in self.get_robot_deps(robot)):
            # robot will never build without all dependencies
            return inf
        while not self.can_afford_robot(robot, materials):
            build_time += 1
            materials += robot_count
        return build_time

    def get_robot_deps(self, robot):
        if robot == "ore":
            return {"ore"}
        if robot == "clay":
            return {"ore"}
        if robot == "obsidian":
            return {"ore", "clay"}
        if robot == "geode":
            return {"ore", "obsidian"}

        raise ValueError(f"Unknown robot {robot}")

    def get_max_material(self, target_material: Material, start_robots: Counter[Robot], time_mins: int):
        return self.get_max_material_production(target_material, time_mins, start_robots, Counter(), [], 0)

    def can_afford_robot(self, robot: Robot, material_count: Counter[Material]):
        return all(material_count[material] >= cost for material, cost in self.costs[robot].items())
