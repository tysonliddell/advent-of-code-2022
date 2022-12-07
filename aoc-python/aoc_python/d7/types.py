from dataclasses import dataclass
from enum import Enum
from typing import Dict, Generator, List, Optional


class FileType(Enum):
    dir = 0
    file = 1


@dataclass
class File:
    type: FileType
    name: str
    size: int


@dataclass
class Command:
    cmd: str
    arg: Optional[str]


@dataclass
class CommandResult:
    command: Command
    result: Optional[List[File]]


@dataclass
class FileNode:
    file: File
    children: Optional[Dict[str, "FileNode"]]


class FileSystem:
    def __init__(self, cmd_results: List[CommandResult]):
        assert cmd_results[0].command == Command(cmd="cd", arg="/")
        curr_node = FileNode(file=File(type=FileType.dir, name="/", size=0), children={})
        self.root = curr_node

        for command_result in cmd_results[1:]:
            if command_result.command.cmd == "cd":
                assert curr_node.children is not None
                assert command_result.command.arg is not None
                curr_node = curr_node.children[command_result.command.arg]
            elif command_result.command.cmd == "ls":
                assert command_result.result is not None
                assert curr_node.children is not None
                for file in command_result.result:
                    n = FileNode(file=file, children={"..": curr_node} if file.type == FileType.dir else None)
                    curr_node.children[file.name] = n
        self._set_dir_sizes()

    def iter_dirs(self) -> Generator[File, None, None]:
        for node in self._iter_files_post_order():
            if node.file.type == FileType.dir:
                yield node.file

    def _set_dir_sizes(self):
        for node in self._iter_files_post_order():
            if node.file.type == FileType.dir:
                node.file.size = sum(node.file.size for name, node in node.children.items() if name != "..")

    def _iter_files_post_order(self) -> Generator[FileNode, None, None]:
        def traverse(node: FileNode) -> Generator[FileNode, None, None]:
            if node.file.type == FileType.dir:
                assert node.children is not None
                for child_name, child_node in node.children.items():
                    if child_name != "..":
                        yield from traverse(child_node)
            yield node

        return traverse(self.root)
