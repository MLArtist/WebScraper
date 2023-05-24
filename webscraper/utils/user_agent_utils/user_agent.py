import json
import os
import random
import config


class UserAgent:
    def __init__(self):
        self.user_agents = self.load(file=os.path.join(config.HOME_DIR, "utils/user_agent_utils/user_agent_list.json"))

    @staticmethod
    def load(file):
        """loads the data  from supplied json file"""
        with open(file) as fp:
            data = json.load(fp)
        if not data:
            print("Empty {} file".format(file))
            raise
        return data['browsers']

    def user_agent(self):
        """returns an user agent selected randomly from the  provided data"""
        browser = random.choice([*self.user_agents])
        return random.choice(self.user_agents[browser])


if __name__ == '__main__':
    pro = UserAgent()
    print(pro.user_agent())