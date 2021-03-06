from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG
from os.path import join, dirname, abspath

class CBTSkill(MycroftSkill):

    def __init__(self):
        super(CBTSkill, self).__init__(name="CBTSkill")
        
    def initialize(self):
        self.mood = True

        path = dirname(abspath(__file__))

        path_to_negative = join(path, 'vocab', self.lang, 'Negative.voc')
        self._negative_words = self._lines_from_path(path_to_negative)

        path_to_positive = join(path, 'vocab', self.lang, 'Positive.voc')
        self._positive_words = self._lines_from_path(path_to_positive)

        path_to_reasons = join(path, 'vocab', self.lang, 'Reasons.voc')
        self._reasons = self._lines_from_path(path_to_reasons)

    def _lines_from_path(self, path):
        with open(path, 'r') as file:
            lines = [line.strip().lower() for line in file]
            return lines

    # The "handle_xxxx_intent" function is triggered by Mycroft when the
    # skill's intent is matched.  The intent is defined by the IntentBuilder()
    # pieces, and is triggered when the user's utterance matches the pattern
    # defined by the keywords.  In this case, the match occurs when one word
    # is found from each of the files:
    #    vocab/en-us/Hello.voc
    #    vocab/en-us/World.voc
    @intent_handler(IntentBuilder("").require("Therapize"))
    def handle_therapize_intent(self, message):
        self.speak_dialog("hello")
        response = self.get_response("how.are.you")
        reason = ""
        affirm = ""

        if response in self._negative_words:
            self.mood = False
            reason = self.get_response("im.sorry", data={"followup": "Can you tell me what made your day tough?"})
        else:
            self.speak("Really?")
            return

        if reason in self._reasons:
            feel = self.get_response("how.do.you.feel")
            affirm = self.get_response("I understand feeling angry can be overwhelming. Wanna learn a trick?")

        if affirm == "yeah":
            self.speak_dialog("anger.exercise")        

    @intent_handler(IntentBuilder("").require("Negative"))
    def handle_negative_intent(self, message):
        self.mood = False
        self.speak_dialog("im.sorry", data={"followup": "Can you tell me what made your day tough?"})

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return CBTSkill()
