"""
This module is responsible for managing the commands to be executed
"""

import json
import subprocess


class CommandControl:
    """
    Class to manage the commands to be executed
    """

    COMMANDS_FILE = "config.json"

    def __init__(self, commands_file=None) -> None:
        self.active_actions = set()

        if commands_file is None:
            commands_file = self.COMMANDS_FILE

        with open(commands_file, encoding="utf-8") as f:
            self.settings = json.load(f)

        self.commands = self.settings["commands"]

    def _check_process_is_running(self, process, running=False):
        """
        Check if a process is running or not
        """
        command_to_send = f"ps -a | grep {process}"
        with subprocess.Popen(
            command_to_send, shell=True, stdout=subprocess.PIPE
        ) as ps:
            output = ps.stdout.read()
            return len(output.decode()) > 0 if running else len(output.decode()) == 0

    def _check_constraints(self, constraints):
        """
        Check if all constraints are met
        """
        for constraint in constraints:
            if not self._check_process_is_running(
                constraint["process"], constraint["status"] == "running"
            ):
                return False
        return True

    def _run_command(self, joystick, command_to_run):
        """
        Run a command based on the buttons pressed
        """

        # Check if all required buttons for the command are pressed
        buttons_pressed = all(
            joystick.get_button(button) for button in command_to_run["buttons"]
        )

        # Manage actions based on button states
        action = command_to_run["action"]
        if not buttons_pressed and action in self.active_actions:
            self.active_actions.remove(action)
            return

        if not (buttons_pressed and action not in self.active_actions):
            return

        if not self._check_constraints(command_to_run["constraints"]):
            return

        # Happy path
        print(f"Executing action: {action}")
        self.active_actions.add(action)
        subprocess.Popen(command_to_run["action"], shell=True)

    def _debug(self, joystick):
        for i in range(0, joystick.get_numbuttons()):
            if joystick.get_button(i):
                print(f"Button {i} pressed")

    def run_commands(self, joystick):
        """
        Run all commands based on the buttons pressed
        """
        if self.settings["debug"]:
            self._debug(joystick)
            return

        for command in self.commands:
            self._run_command(joystick, command)
