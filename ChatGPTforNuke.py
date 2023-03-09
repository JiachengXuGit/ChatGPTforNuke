# -------------------------------------------------------------------------------
# ChatGTPforNuke v1.1 by Jiacheng Xu
# A chatbot using openai module
# 2023
# -------------------------------------------------------------------------------


from PySide2 import QtWidgets, QtCore, QtGui
import openai
import getpass, re, traceback, nuke


icon_path = "C:/Users/" + getpass.getuser() + "/.nuke/"

class ChatGPT(QtWidgets.QWidget):
    def __init__(self):
        super(ChatGPT, self).__init__()
        # Set up the OpenAI API client
        self.code_blocks = ''
        openai.api_key = 'OPENAI_API_KEY'
        self.conversation = [{"role": "system",
                              "content": "helpful assistant. Will help Nuke(Foundry) related question, python, tcl, Nuke expression, BlinkScript."}]

        # Set window properties
        self.setWindowTitle('ChatGPT')
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.setMinimumSize(420, 600)
        self.setWindowIcon(QtGui.QIcon(icon_path + 'ChatGPT.png'))

        # Set background color and font
        self.setStyleSheet("background-color: #323232; sans-serif; font-size: 14px;")

        # Create message input
        self.message_input = QtWidgets.QTextEdit()
        self.message_input.setAcceptRichText(False)
        self.message_input.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.message_input.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.message_input.setStyleSheet("background-color: #3a3a3a; color: #ffffff; border: 1px solid #1f1f1f; \
                                           border-radius: 5px; padding: 10px;")

        # Create response output
        self.response_output = QtWidgets.QTextEdit()
        self.response_output.setReadOnly(True)
        self.response_output.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.response_output.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.response_output.setStyleSheet("background-color: #3a3a3a; color: #ffffff; border: 1px solid #1f1f1f; \
                                           border-radius: 5px; padding: 10px;")

        # Create send button
        send_button = QtWidgets.QPushButton('Send')
        send_button.setFixedHeight(25)
        gradient = "qlineargradient(x1:0, y1:1, x2:0, y2:0, stop:0 #464646, stop:1 #545454);"
        send_button.setStyleSheet(f"background: {gradient}; color: #c8c8c8; border: 1px solid #1f1f1f; \
                                     border-radius: 5px; padding: 1px;")
        send_button.clicked.connect(self.send_message)

        # Create clear button
        clear_button = QtWidgets.QPushButton('Clear')
        clear_button.setFixedHeight(25)
        clear_button.setStyleSheet(f"background: {gradient}; color: #c8c8c8; border: 1px solid #1f1f1f; \
                                     border-radius: 5px; padding: 1px; ")
        clear_button.clicked.connect(self.clear_messages)

        # Create run button
        run_button = QtWidgets.QPushButton('Run Script')

        run_button.setFixedHeight(25)
        run_button.setStyleSheet(f"background: {gradient}; color: #c8c8c8; border: 1px solid #1f1f1f; \
                                     border-radius: 5px; padding: 1px; ")

        icon = QtGui.QIcon(icon_path + 'runthecode.png')
        run_button.setIcon(icon)
        run_button.setIconSize(icon.actualSize(QtCore.QSize(15, 15)))
        run_button.setLayoutDirection(QtCore.Qt.RightToLeft)

        run_button.clicked.connect(self.run_script)

        # Create layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.response_output, 80)
        layout.addWidget(self.message_input, 20)
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(send_button)
        button_layout.addWidget(run_button)
        button_layout.addWidget(clear_button)
        layout.addLayout(button_layout)

        # Set layout
        self.setLayout(layout)

    # Send a message to ChatGPT and update the UI with the response
    def send_message(self):
        message = self.message_input.toPlainText()

        prompt = ""

        prompt += "You: " + message + "\nChatGPT:"
        response = self.get_chat_response(message)

        # Add icons before "you" and "chatgpt"
        cursor = self.response_output.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText('\n')
        image_format = QtGui.QTextImageFormat()
        image_format.setName(icon_path + 'nuke.png')
        image_format.setWidth(16)
        image_format.setHeight(16)
        cursor.insertImage(image_format)

        cursor.insertText(' ')
        cursor.insertHtml('You: ')
        cursor.insertText('\n')
        cursor.insertText(message)
        cursor.insertText('\n\n')
        image_format2 = QtGui.QTextImageFormat()
        image_format2.setName(icon_path + 'ChatGPT.png')
        image_format2.setWidth(16)
        image_format2.setHeight(16)
        cursor.insertImage(image_format2)

        cursor.insertText(' ')
        cursor.insertHtml('ChatGPT: ')
        cursor.insertText('\n')
        cursor.insertText(response)
        cursor.insertText('\n\n')
        self.response_output.ensureCursorVisible()

        self.message_input.clear()

    # Clear previous messages and responses
    def clear_messages(self):
        self.conversation = [{"role": "system",
                              "content": "helpful assistant. Will help Nuke(Foundry) related question, python, tcl, Nuke expression, BlinkScript."}]
        self.response_output.clear()
        self.code_blocks = ''

    # Send a message to ChatGPT and return the response

    def get_chat_response(self, message):

        self.conversation.append({"role": "user", "content": message})

        # Define custom prompts and responses as a dictionary
        custom_prompts = {
            "latest sequence cut": "Here are the latest sequence cut:\n/jobs/show/shots/se_seq/se_seq_cut.mov \n/jobs/show/shots/tb_seq/tb_seq_cut.mov\n/jobs/show/shots/op_seq/op_seq_cut.mov",
            "reference shots": "Here are the reference shows for each sequence:\n se_seq: se0010 se0145 se0212\n tb_seq: tb0240 tb0500 tb010 \n \nContact to your lead if you any"
                               " further questions: \n Jackie Chan jac@domain.com \n Jet Li jel@domain.com ",
            "element library": "Here is the element library: \n https://jiachengx.com/",
            # Add more custom prompts and responses here
        }
        # Handle custom prompts
        if message.lower() in custom_prompts:
            return custom_prompts[message]
        else:
            # Use OpenAI API to get response for other prompts
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=self.conversation,
                    temperature=0,
                    max_tokens=2048,
                    top_p=1
                )
                self.conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})

                response_text = response['choices'][0]['message']['content']

                # Define a regular expression pattern to match the code blocks
                pattern = r"```(?:\w+\n)?([\s\S]+?)```"


                # Find all occurrences of the pattern in the text
                matches = re.findall(pattern, response_text)
                if matches:
                    # Join all the extracted code blocks into a single string
                    self.code_blocks = "\n".join(matches)
                    #print(self.code_blocks)

                else:
                    print("No code blocks found.")

                return response_text

            except Exception as e:
                # display error message box pop-up
                app = QtWidgets.QApplication.instance()
                if app is None:
                    app = QtWidgets.QApplication([])
                msg_box = QtWidgets.QMessageBox()
                msg_box.setIcon(QtWidgets.QMessageBox.Critical)
                msg_box.setText(f"An error occurred: {str(e)}")
                msg_box.setWindowTitle("Error")
                msg_box.exec_()
                return "Please click the clear button"

    def run_script(self):


        try:

            script = self.code_blocks
            print(script)
            exec(script)



        except Exception as e:
            # capture the error message as a string
            error_str = ''.join(traceback.format_exception(type(e), e, e.__traceback__))

            # remove the second line from the error message
            error_str = error_str.split('\n', 2)[0] + '\n' + error_str.split('\n', 2)[2]

            # print the modified error message
            print(error_str)



