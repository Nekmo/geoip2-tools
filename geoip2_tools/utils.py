import sys


def extract_file_to(tar, member_path, to):
    obj = tar.extractfile(member_path)
    if not hasattr(to, 'write'):
        to = open(to, 'w')

    try:
        if sys.version_info >= (3, 3):
            with obj as member:
                to.write(member.read())
        else:
            to.write(obj.read())
            obj.close()

    finally:
        to.close()
