from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import getLogger
#from subprocess import call
import subprocess
import os

__author__ = 'megastruktur'

LOGGER = getLogger(__name__)


class UtilitiesSkill(MycroftSkill):

    # Init stuff.
    def __init__(self):
        
      super(UtilitiesSkill, self).__init__(name="UtilitiesSkill")

    @intent_handler(IntentBuilder("VPNStart").require("VPN")
                    .require("Start"))
    def handle_vpn_start(self, message):
        self.speak("Starting VPN")
        self.command_execute("nmcli con up Sensely")

    @intent_handler(IntentBuilder("VPNStop").require("VPN")
                    .require("Stop"))
    def handle_vpn_stop(self, message):
        self.speak("Stopping VPN")
        self.command_execute("nmcli con down Sensely")

    @intent_handler(IntentBuilder("FixCORS").require("CORS"))
    def handle_fix_cors(self, message):
        self.speak("Fixing KORS")
        self.command_execute("scp /home/megastruktur/sensely/sensely-web-app/builds/latest/.htaccess clinician:/var/www/prod")
        self.speak("KORS are fixed")
  
    @intent_handler(IntentBuilder("Suspend").require("Suspend"))
    def handle_suspend(self, message):
        self.speak("Suspending computer")
        self.command_execute("systemctl suspend")


    # Vagrant handler.
    # Code: environment
    def handle_vagrant_intent(self, message):

        print('----------VAGRANT------------')

        message_string = message.data.get('utterance').split()

        command = self._s(message_string[1])

        try:
            bucket = self._s(message_string[2])
        except IndexError:
            bucket = ""

        self.virtuals_starter("Vagrant", bucket, command)

        print('----------------------')


    # Docker handler.
    # Code: docker
    def handle_docker_intent(self, message):

        print('----------DOCKER------------')

        message_string = message.data.get('utterance').split()

        bucket = self._s(message_string[1])
        command = self._s(message_string[2])
        self.virtuals_starter("Docker", bucket, command)

        print('----------------------')

    # Method will process the Virtuals operations.
    def virtuals_starter(self, virtual_type, bucket, command):

        path = self.get_bucket_path(bucket)
        
        # Execute command only when path is defined.
        if path == False:
            self.speak("No Path")
            return False

        com = self.get_virtual_shell_command(virtual_type, bucket, command)

        if com == False:
            self.speak("No command")
            return False

        self.speak(command + "ing " + bucket + " " + virtual_type)
        self.command_in_path(path, com)
        self.speak(command + "ed " + bucket + " " + virtual_type)

    # Various PC commands.
    def handle_commands_intent(self, message):

        # Parse the message.
        message_string = self._s(message.data.get('utterance'))

    ########################################################################################
    ##################################### HELPERS ##########################################
    ########################################################################################
    # Get shell command which should be executed.
    def get_virtual_shell_command(self, virtual, bucket, command):

        shell_command = {
            "Vagrant" : {
                "start" : "vagrant up " + bucket,
                "stop" : "vagrant halt " + bucket,
            },
            "Docker" : {
                "start" : "docker-compose up -d",
                "stop" : "docker-compose down",
            }
        }
        if virtual in shell_command:
            if command in shell_command[virtual]:
                return shell_command[virtual][command]

        return False

    # Retrieve path by bucket.
    def get_bucket_path(self, bucket):

        path = {
            "apm" : "/home/megastruktur/Documents/Projects/apm/apm-lara",
            "clinician" : "/home/megastruktur/Documents/Projects/Sensely/src/sensely-web-app",
            "": "/home/megastruktur/Documents/Projects/Sensely/src/sensely-web-app"
        }

        if bucket in path:
            return path[bucket]

        return False

    # Execute command.
    def command_execute(self, command):
        subprocess.call(command, shell=True)

    # Execute command in Path.
    def command_in_path(self, path, command):
        wd = os.getcwd()
        os.chdir(path)
        self.command_execute(command)
        os.chdir(wd)

    def stop(self):
        pass
    
    # Get synonym
    def _s(self, phrase):

        synonyms = {
            "stop" : "stop",
            "halt" : "stop",
            "down" : "stop",
            "start" : "start",
            "up" : "start",
            "of" : "start",
            "op" : "start",
            "atm" : "apm",
            "adm" : "apm",
            "apm" : "apm",
            "suspend" : "suspend",
            "vpn start" : "vpn start",
            "vpn stop" : "vpn stop",
            "bpm start" : "vpn start",
            "bpm stop" : "vpn stop",
            "fix kors" : "fix_cors",
            "fix cars" : "fix_cors"
        }

        if phrase in synonyms:
            return synonyms[phrase]
        
        return phrase


def create_skill():
    return UtilitiesSkill()
