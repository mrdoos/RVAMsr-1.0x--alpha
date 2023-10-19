class GoQuorumOptions:
    GOQUORUM_COMPATIBILITY_MODE_DEFAULT_VALUE = False
    goQuorumCompatibilityMode = None

    @staticmethod
    def set_go_quorum_compatibility_mode(go_quorum_compatibility_mode):
        if GoQuorumOptions.goQuorumCompatibilityMode is None:
            GoQuorumOptions.goQuorumCompatibilityMode = go_quorum_compatibility_mode
        else:
            raise RuntimeError("goQuorumCompatibilityMode can not be changed after having been assigned")

    @staticmethod
    def get_go_quorum_compatibility_mode():
        if GoQuorumOptions.goQuorumCompatibilityMode is None:
            # If the quorum mode has never been set, we default it
            # here. This allows running individual unit tests that
            # query the quorum mode without having to include a
            # setGoQuorumCompatibilityMode call in their setup
            # procedure. For production use, this case is not
            # triggered as we set the quorum mode very early during
            # startup.
            GoQuorumOptions.goQuorumCompatibilityMode = GoQuorumOptions.GOQUORUM_COMPATIBILITY_MODE_DEFAULT_VALUE
        return GoQuorumOptions.goQuorumCompatibilityMode
