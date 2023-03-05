#-------------------------------------------------------------------------------
# ChatGTPforNuke by Jiacheng Xu
# A chatbot using openai module
# 2023
#-------------------------------------------------------------------------------


from PySide2 import QtWidgets, QtCore, QtGui
import openai
import getpass

# Set up the OpenAI API client
icon_path = "C:/Users/" + getpass.getuser() + "/.nuke/"

class ChatGPT(QtWidgets.QWidget):
    def __init__(self):
        super(ChatGPT, self).__init__()

        # Set up the OpenAI API client
        openai.api_key = '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'
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
                                     border-radius: 5px; padding: 1px;")
        clear_button.clicked.connect(self.clear_messages)


        # Create close button
        close_button = QtWidgets.QPushButton('Close')
        close_button.setFixedHeight(25)
        close_button.setStyleSheet(f"background: {gradient}; color: #c8c8c8; border: 1px solid #1f1f1f; \
                                     border-radius: 5px; padding: 1px;")
        close_button.clicked.connect(self.close)

        # Create layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.response_output, 80)
        layout.addWidget(self.message_input, 20)
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(send_button)
        button_layout.addWidget(clear_button)
        button_layout.addWidget(close_button)
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

    # Send a message to ChatGPT and return the response

    def get_chat_response(self, message):
        #print(self.conversation)
        #print(f"Received message: {message}")

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
                    model = "gpt-3.5-turbo",
                    messages = self.conversation,
                    temperature = 0,
                    max_tokens = 2048,
                    top_p = 1
                )
                self.conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
                return response['choices'][0]['message']['content']

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






