import gdb
import subprocess
import ast
import time
import os
import inspect

# Get absolute path to the src directory (where this file lives)
BASE_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
HISTORY_PATH = os.path.join(BASE_DIR,"history.txt")
EXPLAIN_SCRIPT = os.path.join(BASE_DIR, "explain_ai.py")
ASK_SCRIPT = os.path.join(BASE_DIR, "ask_ai.py")

class ExplainFault(gdb.Command):
    def __init__(self):
        super().__init__("explain", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        frame = gdb.selected_frame()
        sal = frame.find_sal()

        line_number = sal.line
        code = gdb.execute(f"list", to_string=True)
        signal = "Unknown"
        info = gdb.execute("info program", to_string=True)
        for line in info.splitlines():
            if "Program received signal" in line:
                signal = line.strip()

        print("\n Running AI Explanation...\n")
        try:
            output = subprocess.check_output([
                "python3", EXPLAIN_SCRIPT,
                signal, str(line_number), code
            ])
            print(output.decode('utf-8'))
        except subprocess.CalledProcessError as e:
            print(f"Error executing script: {e}")
            print(f"Output: {e.output.decode('utf-8')}")
        except Exception as ex:
            print(f"Unexpected error: {ex}")

ExplainFault()

class Ask(gdb.Command):
    def __init__(self):
        super().__init__("ask", gdb.COMMAND_USER)
    
    def invoke(self, arg, from_tty):
        question = arg
        history = ""
        history += f"User query :- {question}"
        total_input_tokens = len(str(history))
        total_output_tokens = 0
        start_time = time.time()
        executed_commands = []
        print("========Running AI analysis========\n")
        try:
            root_cause_found = False
            ai_response = None

            while not root_cause_found:
                ai_raw = subprocess.check_output([
                    "python3", ASK_SCRIPT,
                ], stderr=subprocess.STDOUT)

                total_output_tokens += len(ai_raw)
                ai_response = ast.literal_eval(ai_raw.decode('utf-8'))
                root_cause_found = ai_response.get('root_cause_found', False)
                follow_up_command = ai_response.get('follow_up_command')
                history += f"\nCommand to run :- {follow_up_command}"

                if follow_up_command:
                    print(f"Executing follow-up command: {follow_up_command}")
                    executed_commands.append(follow_up_command)
                    try:
                        command_response = gdb.execute(follow_up_command, to_string=True)
                        print(command_response)
                    except gdb.error as e:
                        print(f"Error executing follow-up command: {e}")
                        command_response = f"Command failed: {e}"

                    if(len(command_response) <= 200):
                        history += f"\n{follow_up_command} command response :- {command_response}"
                
                with open(HISTORY_PATH,"w") as f:
                    f.write(history)

            print("\n========Root cause found========\n", ai_response.get('root_cause_analysis', 'No analysis provided'))
            print("========Suggested fix========\n", ai_response.get('code_fix_suggestion', 'No fix provided'))
            total_cost = (total_input_tokens / 1_000_000) * 0.075 + (total_output_tokens / 1_000_000) * 0.30
            print(f"\ncost: ${total_cost:.6f}")
            print(f"Time taken: {time.time() - start_time:.2f} seconds")
            print(f"Total commands executed: {len(executed_commands)}")
            with open(HISTORY_PATH,"w") as f:
                f.write("")

        except subprocess.CalledProcessError as e:
            print(f"Error executing AI script: {e.output.decode('utf-8')}")
        except Exception as ex:
            print(f"Unexpected error: {ex}")

Ask()