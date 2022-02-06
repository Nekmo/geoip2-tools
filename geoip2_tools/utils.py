from tarfile import TarFile
from typing import BinaryIO


def extract_file_to(tar: TarFile, member_path: str, to: BinaryIO):
    obj = tar.extractfile(member_path)
    with obj as member:
        to.write(member.read())
