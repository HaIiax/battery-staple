class Security:
    def __init__(self, security_definition: str):
        self.security_definition = security_definition.replace(" ", "")
        self.security_dict = {}
        if self.security_definition is not None:
            for permitted_command_users in security_definition.split(";"):
                permitted_users = permitted_command_users.split(",")
                self.security_dict[permitted_users[0]] = permitted_users[1:]

    def isPermitted(self, command, user_id):
        if command not in self.security_dict:
            return True
        permitted_users = self.security_dict[command]
        if user_id in permitted_users:
            return True
        return False



