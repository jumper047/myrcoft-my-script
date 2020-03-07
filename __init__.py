from os.path import dirname

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
import subprocess


LOGGER = getLogger(__name__)

class myscriptskill(MycroftSkill):

    def __init__(self):
        super(myscriptskill, self).__init__(name="myscriptskill")
        if (not self.settings.get('lampaddr')):
           self.settings['lampaddr'] = '192.168.1.2'

    def shutdown(self):
        pass
    
    def initialize(self):
        self.__build_single_command()
        
    def __build_single_command(self):
        intent = IntentBuilder("mymqttIntent").require("CommandKeyword").require("ModuleKeyword").require("ActionKeyword").build()
        self.register_intent(intent, self.handle_single_command)
        
    def handle_single_command(self, message):
        cmd_name = message.data.get("CommandKeyword").replace(' ', '_')
        dev_name = message.data.get("ModuleKeyword").replace(' ', '_')
        act_name = message.data.get("ActionKeyword").replace(' ', '_').upper()
        
        try:
            LOGGER.info("Executing command:%s %s %s", cmd_name, dev_name, act_name)
            if dev_name == "light":
                subprocess.run(["wget", "-O", "-", "{ip}/cm?cmnd=Power%20{cmd}".format(ip=self.settings['lampaddr'], cmd=act_name)])
        except Exception as e:
            LOGGER.info("Exception raised while publishing command: %s", e)
            self.speak_dialog("not.found", {"command": cmd_name, "action": act_name, "module": dev_name})
    def stop(self):
        pass
        
def create_skill():
    return myscriptskill()
