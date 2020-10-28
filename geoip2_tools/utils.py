import sys


def extract_file_to(tar, member_path, to):
    obj = tar.extractfile(member_path)
    if sys.version_info >= (3, 3):
        with obj as member:
            with open(to, 'wb') as f:
                f.write(member.read())
    else:
        with open(to, 'wb') as f:
            f.write(obj.read())
            obj.close()
