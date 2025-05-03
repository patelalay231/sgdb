import gdb
import subprocess
import ast
import time

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
                "python3", "explain_ai.py",
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
        # Get the user's question (if provided)
        question = arg
        history = []
        executed_commands = []
        total_input_tokens = 0
        total_output_tokens = 0
        start_time = time.time()  # start timing
        print("========Running AI analysis========\n")
        try:
            history.append({
                'role': 'user',
                'content': question
            })
            total_input_tokens += len(str(history))
            system_instruction = open('utils/system_instruction.txt', "r").read()
            root_cause_found = False
            ai_response = None
            while root_cause_found == False:
                ai_response = subprocess.check_output([
                    "python3", "ask_ai.py",
                    str(history),
                    system_instruction,
                ], stderr=subprocess.STDOUT)
                total_output_tokens += len(ai_response)
                ai_response = ast.literal_eval(ai_response.decode('utf-8'))

                history.append({
                    'role': 'model',
                    'content': ai_response
                })
                root_cause_found = ai_response.get('root_cause_found', False)
                follow_up_command = ai_response.get('follow_up_command', None)
                if follow_up_command and follow_up_command not in executed_commands:
                    executed_commands.append(follow_up_command)
                    print(f"Executing follow-up command: {follow_up_command}")

                    # Check if the program is running
                    program_info = gdb.execute("info program", to_string=True)
                    if "not being run" in program_info or "has exited" in program_info:
                        print("Program is not running. Re-run it...\n")
                        return
                    try:
                        command_response = gdb.execute(follow_up_command, to_string=True)
                        print(command_response)
                    except gdb.error as e:
                        print(f"Error executing follow-up command: {e}")
                        command_response = f"Command failed: {e}"

                history.append({
                    'role': 'user',
                    'content': command_response
                })
            
            print("========Root cause found========\n", ai_response.get('root_cause_analysis', 'No analysis provided'))
            print("========Suggested fix========\n", ai_response.get('code_fix_suggestion', 'No fix provided'))
            total_cost = cost = (total_input_tokens / 1000000) * 0.075 + (total_output_tokens / 1000000) * 0.30
            print("cost: $",total_cost)
            end_time = time.time()    # end timing
            elapsed_time = end_time - start_time
            print(f"Time taken: {elapsed_time:.2f} seconds")
            print(f"total commands executed: {len(executed_commands)}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing AI script: {e.output.decode('utf-8')}")
        except Exception as ex:
            print(f"Unexpected error: {ex}")

Ask()

