from mycroft import MycroftSkill, intent_file_handler


class IssTracker(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('tracker.iss.intent')
    def handle_tracker_iss(self, message):
        self.speak_dialog('tracker.iss')


def create_skill():
    return IssTracker()

