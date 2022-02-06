from tarfile import TarFile


def extract_file_to(tar: TarFile, member_path: str, to: str):
    obj = tar.extractfile(member_path)
    with obj as member:
        with open(to, 'wb') as f:
            f.write(member.read())
