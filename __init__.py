from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
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

    # Functionality init.
    def initialize(self):

        # Intents.
        vagrant_intent = IntentBuilder("VagrantIntent"). \
            require("Vagrant").build()
        self.register_intent(vagrant_intent, self.handle_vagrant_intent)

        docker_intent = IntentBuilder("DockerIntent"). \
            require("Docker").build()
        self.register_intent(docker_intent, self.handle_docker_intent)


    # Vagrant handler.
    # Code: environment
    def handle_vagrant_intent(self, message):

        print('----------VAGRANT------------')

        message_string = message.data.get('utterance').split()

        command = self._s(message_string[1])
        bucket = self._s(message_string[2])
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

    def stop(self):
        pass

    # Execute command in Path.
    def command_in_path(self, path, command):
        wd = os.getcwd()
        os.chdir(path)
        subprocess.call(command, shell=True)
        os.chdir(wd)

    
    # Get synonym
    def _s(self, phrase):

        synonyms = {
            "stop" : "stop",
            "halt" : "stop",
            "down" : "stop",
            "start" : "start",
            "up" : "start",
            "of" : "start",
            "atm" : "apm",
            "adm" : "apm",
            "apm" : "apm",
            "claymation" : "clinician"
        }

        if phrase in synonyms:
            return synonyms[phrase]
        
        return phrase

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
            "clinician" : "/home/megastruktur/Documents/Projects/Sensely/src/sensely-chef"
        }

        if bucket in path:
            return path[bucket]

        return False


def create_skill():
    return UtilitiesSkill()