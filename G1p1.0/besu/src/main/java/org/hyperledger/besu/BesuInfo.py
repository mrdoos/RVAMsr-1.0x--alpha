imimport platform


class BesuInfo:
    CLIENT = "besu"
    VERSION = "1.0.0"  # Replace with the actual version
    OS = platform.system()
    VM = platform.python_implementation()

    @staticmethod
    def version():
        return f"{BesuInfo.CLIENT}/v{BesuInfo.VERSION}/{BesuInfo.OS}/{BesuInfo.VM}"

    @staticmethod
    def nodeName(maybeIdentity):
        if maybeIdentity:
            return f"{BesuInfo.CLIENT}/{maybeIdentity}/v{BesuInfo.VERSION}/{BesuInfo.OS}/{BesuInfo.VM}"
        else:
            return BesuInfo.version()


# Example usage
print(BesuInfo.version())
print(BesuInfo.nodeName("myIdentity"))
print(BesuInfo.nodeName(None))
