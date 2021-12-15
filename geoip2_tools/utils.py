import sys


def extract_file_to(tar, member_path, to):
    opened, obj = False, tar.extractfile(member_path)
    if not hasattr(to, 'write'):
        opened = True
        to = open(to, 'wb')

    try:
        if sys.version_info >= (3, 3):
            with obj as member:
                to.write(member.read())
        else:
            to.write(obj.read())
            obj.close()

    finally:
        if opened:
            to.close()
