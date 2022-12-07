from typing import Generator, List, Optional

from aoc_python.common.utils import get_day_n_input
from aoc_python.d7.types import Command, CommandResult, File, FileSystem, FileType


def main():
    data = get_day_n_input(7)
    command_results = list(_iter_commands(data))
    file_system = FileSystem(command_results)

    # Part 1
    dirs_part1 = [file for file in file_system.iter_dirs() if file.type == FileType.dir and file.size <= 100000]
    print(sum(f.size for f in dirs_part1))

    # Part 2
    space_used = file_system.root.file.size
    space_free = 70000000 - space_used
    extra_space_needed = 30000000 - space_free

    candidate_dirs = [d for d in file_system.iter_dirs() if d.size >= extra_space_needed]
    candidate_dirs.sort(key=lambda f: f.size)
    print(candidate_dirs[0])


def _iter_commands(data: List[str]) -> Generator[CommandResult, None, None]:
    cmd_result = CommandResult(command=_parse_command(data[0]), result=[])

    for line in data[1:]:
        if line.startswith("$"):
            yield cmd_result
            cmd = _parse_command(line)
            result: Optional[List[File]] = None if cmd.cmd == "cd" else []
            cmd_result = CommandResult(command=cmd, result=result)
        else:
            assert cmd_result.result is not None
            cmd_result.result.append(_parse_result_line(line))
    yield cmd_result


def _parse_command(cmd_str: str) -> Command:
    cmd_tokens = cmd_str.split(" ")
    assert len(cmd_tokens) in [2, 3]
    if len(cmd_tokens) == 2:
        _, cmd_raw = cmd_tokens
        return Command(cmd=cmd_raw, arg=None)
    elif len(cmd_tokens) == 3:
        _, cmd_raw, arg = cmd_tokens
        return Command(cmd=cmd_raw, arg=arg)
    else:
        raise RuntimeError("Unexpected number of args in command")


def _parse_result_line(result_line: str) -> File:
    result_tokens = result_line.split(" ")
    assert len(result_tokens) == 2
    if result_tokens[0] == "dir":
        return File(type=FileType.dir, name=result_tokens[1], size=0)
    else:
        return File(type=FileType.file, name=result_tokens[1], size=int(result_tokens[0]))


main()
